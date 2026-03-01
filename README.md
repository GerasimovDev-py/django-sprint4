django_sprint4
Блогикум

Блогикум — это социальная платформа для публикации и обсуждения записей. Пользователи могут создавать посты, оставлять комментарии, редактировать свои профили и взаимодействовать с контентом других авторов.

Ссылка на работающий сайт
Проект доступен по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000) (локальный сервер)

Автор 
GitHub: [GerasimovDev-py](https://github.com/GerasimovDev-py)
GitHub: [Rishat-Ver Rishik](https://github.com/Rishat-Ver Rishik)
GitHub: [yandex-praktikum](https://github.com/yandex-praktikum)
GitHub: [evi1ghost Andrey Dubinchik](https://github.com/evi1ghost)


Техно-стек
- Python 3.10+
- Django 5.1.1
- SQLite3
- HTML/CSS (Bootstrap 5)
- Git

В проекте настроен GitHub Actions для автоматического тестирования при пушах в main ветку.
Команды локального развертывания с Докером
Клонирование репозитория
git clone https://github.com/GerasimovDev-py/django-sprint4.git
cd django-sprint4

Создание файла .env (пример в example.env)
cp example.env .env
Отредактируйте .env под свои нужды

Запуск контейнеров
docker-compose up -d

Подготовка базы данных
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py loaddata db.json

Сборка статики
docker-compose exec web python manage.py collectstatic --noinput

Сервер уже запущен на http://127.0.0.1:8000


Клонирование репозитория
git clone https://github.com/GerasimovDev-py/django-sprint4.git
cd django-sprint4

Переход в папку проекта
cd blogicum

Настройка виртуального окружения
python -m venv venv
Активация (Windows)
venv\Scripts\activate
Активация (Linux/Mac)
source venv/bin/activate

Установка зависимостей
pip install -r requirements.txt

Создание файла .env
cp ../example.env .env
Или создайте вручную:
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

Миграция базы данных и создание суперпользователя
python manage.py migrate
python manage.py createsuperuser

Импорт фикстур
python manage.py loaddata ../db.json
Запуск сервера
python manage.py runserver

Сервер доступен по адресу:
http://127.0.0.1:8000