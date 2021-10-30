# django-rest-crud

1. docker-compose run -d --build
2. docker-compose exec web python manage.py migrate

Для доступа к закрытым методам, авторизуемся через swagger или добавляем в заголовок запроса "Authorization: token <token>"
Токен генерируется при регистрации пользователя. Для его получения вызывается метод /user/api-token-auth/

