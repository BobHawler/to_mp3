# Задача 2

Сервис позволяет конвертировать пользовательские wav-файлы в mp3.

## Скачивание проекта и подготовка файлов:

### Создайте папку:
```bash
mkdir task_2
```

### Перейдите в папку:
```bash
cd task_2
```
### Скачайте репозиторий:
```bash
git clone git@github.com:BobHawler/to_mp3.git
```

### Перейдите в папку проекта:
```bash
cd to_mp3
```

### Создйте .env файл:
```bash
touch .env
```

### В .env файле укажите данные своей базы данных.
Пример наполнения можно увидеть в файле .env_example:
```bash
POSTGRES_DB=converters_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

## Создание и запуск контейнера:

### Сборка образов и запуск котейнеров:

```bash
docker-compose up -d --build
```
### Остановка контейнеров:
```bash
docker-compose stop
```
### Повторный запуск контейнеров:
```bash
docker-compose up
```
Данные БД хранятся в volumes

## Инициализация БД (выполняется внутри контейнера):
```bash
docker-compose exec app bash
```
```bash
flask db init
flask db migrate
flask db upgrade
```
## Пример работы сервиса:

### Перейдите на страницу:
```
http://localhost:5000/users
```
### Введите желаемое имя пользователя.
В ответ вы получите свой уникальный идентификатор и токен:
```
{"uid":"8fddaa96","token":"02371a613bb340fe9e88c253c0015b1b"}
```
### Перейдте на страницу:
```
http://localhost:5000/recordings
```

### Введите свой уникальный идентификатор и токен, укажите файл, который желаете конвертировать (поддерживается только конвертация из wav в mp3)

В ответ вы получите ссылку на скачивание вашего конвертированного файла:
```
{"url":"http://localhost:5000/record?id=676ade572e934a4e8ef723e1dc7bac7c&user=8fddaa96"}
```
### Перейдите по ссылке и файл будет загружен в вашу стандартную папку с загрузками.

### Как подключиться к БД:
```bash
docker-compose exec db psql questions_db -U postgres
```
### Примеры запросов к БД:
```bash
SELECT * FROM questions_db;

SELECT question FROM questions_db;
```

## Автор:
Анатолий Коновалов (BobHawler)
