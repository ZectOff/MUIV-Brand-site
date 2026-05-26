# MUIV Brand Site: локальное развертывание

Инструкция для Windows + PowerShell (аналогично работает и на Linux/macOS с адаптацией команд активации venv и установки PostgreSQL).

## 1) Требования

- Python 3.12+ (проверено на Python 3.14)
- PostgreSQL 15+ (проверено на PostgreSQL 18)
- Git

## 2) Клонирование репозитория

```powershell
git clone https://github.com/ZectOff/MUIV-Brand-site.git
cd MUIV-Brand-site
```

## 3) Создание и активация виртуального окружения

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Если PowerShell блокирует запуск скриптов:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## 4) Установка зависимостей

```powershell
pip install -r requirements.txt
```

## 5) Настройка PostgreSQL

Проект использует параметры подключения из `muivbrnd/muivbrnd/settings.py`:

- DB name: `muivbrand`
- User: `zect`
- Password: `root`
- Host: `localhost`
- Port: `5432`

Создайте пользователя и базу (из `psql` под суперпользователем `postgres`):

```sql
CREATE ROLE zect WITH LOGIN PASSWORD 'root' CREATEDB;
CREATE DATABASE muivbrand OWNER zect;
```

Если роль уже существует, создайте только БД:

```sql
CREATE DATABASE muivbrand OWNER zect;
```

## 6) Применение миграций

```powershell
cd .\muivbrnd
python manage.py migrate
```

## 7) Загрузка стартовых данных

```powershell
python manage.py loaddata fixtures/goods/categories.json fixtures/goods/products.json
```

## 8) Создание тестового администратора

```powershell
python manage.py seed_superuser
```

После команды будет создан/обновлен пользователь:

- Логин: `admin`
- Пароль: `root`

## 9) (Опционально) Генерация тестовых данных

```powershell
python manage.py seed_test_orders
python manage.py seed_product_reviews
```

## 10) Запуск сервера

```powershell
python manage.py runserver 127.0.0.1:8000
```

Открыть в браузере:

- Главная: <http://127.0.0.1:8000/>
- Каталог: <http://127.0.0.1:8000/catalog/vse-tovary/>
- Админка: <http://127.0.0.1:8000/admin/>

## 11) Частые проблемы

### Нет модуля Django / Pillow / psycopg2

Повторите установку:

```powershell
pip install -r ..\requirements.txt
```

### Ошибка подключения к PostgreSQL

Проверьте:

- запущен ли сервис PostgreSQL;
- существуют ли роль `zect` и БД `muivbrand`;
- совпадают ли логин/пароль в `settings.py`.

### У товара нет фото

Это ожидаемо: для товаров без загруженных изображений показываются иконки категорий и подпись «У товара еще нет фото».
