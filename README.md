### 🚀 Installation & Setup

Follow these steps in an ordered manner to initialize the **Aqua Marine Intelligence** system:

1. **Virtual Environment**: 
   Create and activate a isolated environment to prevent library conflicts.
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install django
   python manage.py makemigrations ocean_data
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
