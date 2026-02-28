from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (
    ListView, DetailView, CreateView,
    UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Count
from django.http import Http404
from django.conf import settings
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm, ProfileEditForm

User = get_user_model()


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user.username])


class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return post.author == self.request.user

    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.kwargs['post_id'])


class CommentAuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        comment = get_object_or_404(Comment, id=self.kwargs['comment_id'])
        return comment.author == self.request.user

    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.kwargs['post_id'])


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = settings.POSTS_PER_PAGE

    def get_queryset(self):
        return Post.objects.filter(
            pub_date__lte=timezone.now(),
            category__is_published=True,
            is_published=True
        ).select_related(
            'author', 'category', 'location'
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def get_object(self):
        post = get_object_or_404(
            Post.objects.select_related('author', 'category', 'location'),
            id=self.kwargs['post_id']
        )
        if (post.author != self.request.user
                and (post.pub_date > timezone.now()
                     or not post.is_published
                     or not post.category.is_published)):
            raise Http404
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related(
            'author'
        ).order_by('created_at')
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user.username])


class PostUpdateView(AuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['post_id']])


class PostDeleteView(AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/delete.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        return context

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user.username])


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, id=self.kwargs['post_id'])
        return context

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['post_id']])


class CommentUpdateView(CommentAuthorRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, id=self.kwargs['post_id'])
        return context

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['post_id']])


class CommentDeleteView(CommentAuthorRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_delete.html'
    pk_url_kwarg = 'comment_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.get_object()
        if 'form' in context:
            del context['form']
        return context

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['post_id']])


class ProfileView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    context_object_name = 'post_list'
    paginate_by = settings.POSTS_PER_PAGE

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        posts = Post.objects.filter(author=self.author)

        if self.request.user != self.author:
            posts = posts.filter(
                pub_date__lte=timezone.now(),
                category__is_published=True,
                is_published=True
            )

        return posts.select_related(
            'author', 'category', 'location'
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.author
        return context


class CategoryListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'post_list'
    paginate_by = settings.POSTS_PER_PAGE

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return Post.objects.filter(
            category=self.category,
            pub_date__lte=timezone.now(),
            is_published=True
        ).select_related(
            'author', 'location'
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
