# Описание проекта:

### Foodgram - площадка для размещения своих рецептов.
Доменный адрес https://foodlist.sytes.net/

Каждый зарегистрированный пользователь может разместить свои рецепты с фотографиями и необходимыми ингредиентами, также для авторизованных пользователей предоставляется такой функционал, как:
1. Добавление рецепта в избранное
2. Добавление рецепта в список покупок
3. Подписка на пользователя
4. Скачивание списка рецепта с учетом повторяющихся ингредиентов
5. Создание рецепта

# Запуск проекта на этапе разработки:
Форкнуть репозиторий с гита:
```
https://github.com/Ray-Not/foodgram-project-react.git
```
Клонировать репозиторий и перейти в него в командной строке:
```
git clone ggit@github.com:<your_login>/foodgram-project-react.git
```
Прописать свои данные в файле .env (примеры есть в env.example).

После изменений загрузить репозиторий
```
git add ...
git commit ...
git push
```
После автоматических тестов, проект сам развернется на сервере, можно переходить к запуску проекта в продакшене

# Запуск проекта в продакшн:

Скопировать файл docker-compose.production.yml в нужную директорию

Запустить docker-compose:
```
sudo docker compose -f docker-compose.production.yml up -d
```
### Заметки:
* Для работы необходимо настроить nginx ```/etc/nginx/sites-enabled/default```:
```json
location / {
        proxy_pass http://127.0.0.1:8000;
    }

```
* Обязательно открыть порты, чтобы nginx работал

# Примеры запросов uri:
```/admin/``` - админка сайта

```/api/``` - взаимодействие с API

```/api/recipes/``` - взаимодействие с рецептами через API

```/api/users/``` - взаимодействие с пользовтелями через API

```/signin/``` - регистрация

# Об авторе:
### gmail:
```2sinsincuba@gmail.com```

![GitHub Streak](https://github-readme-streak-stats.herokuapp.com/?user=Ray-Not)

![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=Ray-Not&layout=compact)

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/docker%20-%230db7ed.svg?&style=for-the-badge&logo=docker&logoColor=white)
![JS](https://img.shields.io/badge/javascript%20-%23323330.svg?&style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Nginx](https://img.shields.io/badge/nginx%20-%23009639.svg?&style=for-the-badge&logo=nginx&logoColor=white)
