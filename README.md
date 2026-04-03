git clone https://github.com/Asiliya/test-assessment---Travel-Planner.git
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
