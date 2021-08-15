Инструкция по развертыванию приложения:

    1. Клонируйте репозиторий 
    2. Перейдите в соответствующию директорию 
    3. Создайте виртуальное окружение 
    4. Установите зависимости: 
        Linux: pip3 install -r requirements.txt 
        Windows: pip install -r requirements.txt
    5. Проведите миграцию БД:
        python3 manage.py makemigrations
        python3 manage.py migrate
    6. Создайте суперпользователя:
        python3 manage.py createsuperuser
        (следуйте инструкциям в консоли) 
    7. Запустите приложение
        python3 manage.py runserver

Инструкция по авторизации:

    1. Пройдите по адресу token/
    Передайте в качестве параметров username, password
    2. В качестве ответа будут получены:
        access_token
        refresh_token
    3. access_token должен передаваться в заголовке Authorization
        в формате: "Bearer <access_token>"
    
API routes:

    1. Список активных опросов:
        /poll_app/active_polls
    2. Добавление опросов (параметры - name, end_date, description)
        /poll_app/polls/
    3. Изменение, удаление опросов 
        /poll_app/polls/<poll_id>
    4. Добавление вопросов к опросу (параметры - text, type, poll)
    5. Изменение, удаление вопросов 
        /poll_app/polls/<poll_id>/questions/<question_id>
    6. Варианты ответов к вопросам 
        /poll_app/polls/<poll_id>/questions/<question_id>/answer_options
    7. Пройти опрос:
        /poll_app/polls/<poll_id>/questions/<question_id>/answers
    8. Пройденные пользователем опросы:
        /poll_app/my_polls
