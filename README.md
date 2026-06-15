#  Итоговый проект Django | Веб-портал "Блог"

**Курс:** Программирование 2 курс  
**Технология:** Django 3.2 (с патчем legacy-cgi для Python 3.14)

##  Выполненные требования:
- Логическое разделение на 3 приложения (`accounts`, `blog`, `interactions`)
- Кастомная модель пользователя с ролями
- Полное соответствие PEP 8

##  Инструкция по запуску:
1. Убедиться, что виртуальное окружение активировано.
2. Установить зависимости: 
   ```bash
python -m venv .venv

.venv\Scripts\Activate.ps1

pip install -r requirements.txt

python manage.py migrate


python manage.py createsuperuser


python manage.py runserver