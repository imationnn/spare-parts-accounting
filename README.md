# Spare parts accounting

### ⚠️ <ins>Внимание: проект в стадии разработки</ins> ⚠️

## Описание

Backend часть приложения по учету, подбору, заказу и продаже автозапчастей. 

### Используемый стек технологий (на данный момент):

* Python 3.12
* FastAPI
* PostgreSQL(asyncpg)
* SQLAlchemy
* Alembic
* Pytest(pytest-asyncio)
* Redis
* Uvicorn
* Git

### Директории и файлы проекта:

* app - директория приложения
* app/api - директория с routers и endpoints 
* app/config - директория с настройками приложения, баз данных и получение сессии базы данных
* app/exceptions - классы исключений
* app/migrations - директория alembic для миграций
* app/models - классы моделей SqlAlchemy
* app/repositories - repository для SqlAlchemy
* app/schemas - классы Pydantic
* app/services - классы сервисов с бизнес-логикой и взаимодействием с repository
* tests - директория с тестами
* .env.example - пример файла .env
* main.py - файл для запуска
* pyproject.toml - файл зависимостей для poetry
* requirements.txt - файл зависимостей для pip

### Что реализовано на данный момент:

* добавление администратора при первом запуске
* аутентификация сотрудника по логину и паролю
* обновление access токена по refresh токену
* смена магазина (для просмотра заказов, чеков, поступлений в разных магазинах)
* добавление нового сотрудника
* просмотр информации о сотруднике по логину и id / просмотр всех сотрудников
* изменение информации о сотруднике
* проверка ролей сотрудников
* получение бренда по названию и id
* добавление / изменение бренда
* просмотр / изменение наценок
* получение информации о детали по номеру и id
* добавление новой детали / изменение существующей

## Как запустить:

⚠️ Необходимы уже установленный и запущенный сервер postgres и redis

* Клонируйте репозиторий и перейдите в него:
```
git clone https://github.com/imationnn/spare-parts-accounting
```
* Создайте и активируйте виртуальное окружение:
```
python3 -m venv venv
```
* для macOS/Linux:
```
source venv/bin/activate
```
* для Windows:
```
venv\Scripts\activate
```
* Установите зависимости:
* с poetry:
> poetry install
* c pip:
> pip install -r requirements.txt
* Измените название файла .env.example на .env

### Настройка:

Обновите конфигурацию файла .env  
Если на локальных БД вы не используете пароли, то можете оставить эти поля пустыми.  
При первом запуске будет создан пользователь с ролью admin. 
Измените значения в полях на свои
* `FIRST_EMPLOYEE_LOGIN`
* `FIRST_EMPLOYEE_PASSWORD`
* `FIRST_EMPLOYEE_FULLNAME`

по умолчанию login=admin, password=admin, fullname=first user.  
Если хотите добавить в БД тестовые данные, измените поле ```ADD_TEST_DATA``` на True.  
Для выпуска токенов авторизации нужен секретный ключ. Добавьте секретный ключ в поле 
* `SECRET_KEY`

Для генерации ключа можно воспользоваться командой:
> python -c "import secrets; print(secrets.token_urlsafe(64))"

### Запустите проект командой:
> uvicorn main:app
> 
или
> python3 main.py