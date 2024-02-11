# stakewolle_test – Тестовое задние

Сервис, позволяющий пользвователю регистрироватся с использоварием реферальных кодов и создавать свои.
* Стек:
  * FastApi
  * Python 3.11
  * Alembic
  * PostgreSQL
  * SQLAlchemy
  * alembic
  * fastapi-users
  * fastapi-cache2
  * redis

## Клонирование проекта
```git clone git@github.com:deepxshine/stakewolle_test.git```

## Установка зависисостей
```pip install -r requriments.txt```

## Перед запуском прокта
Создать и заполнить .end
```nano .env```
Пример заполения .env
```DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres
SECRET=secret
```

## Для запуска проекта
Выполните командды:
```bash
  alembic revision --autogenerate -m "Inital"
  alembic upgrade head
  cd scr/
  uvicorn main:app --reload    
```


## Для авторизованных пользователей:
Доступно 4 эндпоинта:
### 1) /referal/register_referal/{referal_code}
   По данному эндпоинту вы можете зарегестрироваться как реферал. Эндпоинт доступен толко для авторизованных пользователей.
   
### 2) /referal/create_referal_code
  По данному эндпоинту вы можете создать реферальный код, задав ему дату, когда он перестанет дейтсвовать.Эндпоинт доступен толко для авторизованных пользователей.
  
### 3) /referal/referal
   По данному эндпоинту вы можете получить реферальный код по email адресу реферера
   
### 4) /referal/referers
  По данному эндпоинту вы можете получить информацию о рефералах по id реферера
