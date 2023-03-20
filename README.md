# OneNineAIAppSP23

To get started, after cloning the github. Open up a terminal and go to the AI directory in there you can type:
`python manage.py runserver` 
and it'll launch a local django server on port 8000. For now most of our work will probably be on here http://127.0.0.1:8000/transform/.

## Argon dashboard quick set up
```
git clone  https://github.com/J-Mojica/OneNineAIAppSP23.git
cd argon-dashboard-django

# Virtualenv modules installation (Unix based systems)
virtualenv env
source env/bin/activate

# Virtualenv modules installation (Windows based systems)
# virtualenv env
# .\env\Scripts\activate

# Install modules - SQLite Storage
pip3 install -r requirements.txt

# Create tables
python manage.py makemigrations
python manage.py migrate

# Start the application (development mode)
python manage.py runserver # default port 8000

# Start the app - custom port
# python manage.py runserver 0.0.0.0:<your_port>

# Access the web app in browser: http://127.0.0.1:8000/
```