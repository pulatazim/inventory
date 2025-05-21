# Warehouse Inventory API

Bu loyiha ishlab chiqarish uchun xomashyolarni hisoblaydigan API tizim.

## Texnologiyalar

- Python
- Django
- Django REST Framework
- SQLite3
- Postman

## Ishga tushirish

```bash
git clone https://github.com/pulatazim/inventory
cd project-folder
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
