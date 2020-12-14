# Django-ToDoApp
It is a basic To-Do App project with basic Django skills.

## Quick Start
- Open your terminal in base folder and install the requirements by typing "pip install -r requirements.txt"
- Type "python manage.py makemigrations"
- Type "python manage.py migrate"
- Type "python manage.py createsuperuser" and fill in the blanks.
- You can check the database by login to localhost:8000/admin with your superuser infos.
- Start the project by typing "python manage.py runserver".
- You ready to go.

General features are;
- User registration
- User login
- To-Do list creation (Each user will be able to have multiple To-Do lists. Each To-Do list have a name.)
- List of To-Do lists
- Delete To-Do list
- Add To-Do item to existing To-Do list
- Each To-Do item should have a name, description, deadline, and status
- Mark To-Do item as "Complete"
- Filter To-Do items (status complete or not, expired) on a To-Do list
- Order To-Do items on a To-Do list by create date, deadline, or name.
- Delete To-Do item from To-Do list.
