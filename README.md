Navigate to the appropriate directory:
cd SeniorProject/src/django_project/

Activate the virtual environment:
source ./venv/bin/activate

Install all of the dependencies:
pip install -r requirements.txt

Launch the local development server:
python manage.py runserver

Include the following in .gitignore this way files
containing a .pyc extension are not pushed to GitHub.
*.pyc
__pycache__/
