![workflow](https://github.com/sakovdmitry/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
адрес для доступа:
http://51.250.96.231/

# Описание проекта
Сайт Foodgram, «Продуктовый помощник».
Foodgram - это онлайн-сервис с помощью которого пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

# Шаблон наполнения .env файла

	DB_ENGINE=django.db.backends.postgresql
	DB_NAME=postgres
	POSTGRES_USER=postgres
	POSTGRES_PASSWORD=postgres
	DB_HOST=db
	DB_PORT=5432
	SECRET_KEY = 'your secret key'

## Запуск проекта
Для начала склонируйте репозиторий с github
```
git clone git@github.com:sakovdmitry/foodgram-project-react.git
```
Комманда git push является триггером workflow (foodgram_workflow.yml).
При выполнении команды git push запускается набор блоков следующих команд:
1. Тестирование проекта (flake8).
2. Сборка и публикация образа.
3. Автоматический деплой.
4. Отправка уведомления в персональный чат telegram.

В дальнейшем необходимо установить соединение с сервером и выполнить следующие команды:

- Выполнить миграции
```
sudo docker-compose exec web python manage.py migrate
```
- Создать суперпользователя
```
sudo docker-compose exec web python manage.py createsuperuser
```
- Сформируйте STATIC файлы:
```
sudo docker-compose exec web python manage.py collectstatic --no-input
```
### API ресурсы:
- **USERS**: Прекрасные пользователи сайта.
- **TAGS**: Теги к создаваемым рецептам.
- **RECEPIES**: Рецепты вкуснейших блюд.
- **FAVORITES**: Добавить рецепт в избранное - запросто!
- **SUBSCRIPTIONS**: Этот рецепт действительно хорош, подпишусь ка на автора!
- **INGREDIENTS**: Отличные ингредиенты к рецептам

### Примеры запросов:

Пример GET запроса:
```
GET http://51.250.96.231/api/users/
```
Ответ:
```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/users/?page=4",
  "previous": "http://foodgram.example.org/api/users/?page=2",
  "results": [
    {
      "email": "user@example.com",
      "id": 0,
      "username": "string",
      "first_name": "Вася",
      "last_name": "Пупкин",
      "is_subscribed": true
    }
  ]
}
```
Пример POST запроса:
```
POST http://51.250.96.231/api/recipes/
```
Содержимое запроса:
```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```
Ответ:
```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": true
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```

### Автор:
Sakov Dmitry
