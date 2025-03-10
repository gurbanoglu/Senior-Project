Navigate to the appropriate directory:
cd SeniorProject/src/django_project/

Activate the virtual environment:
source ./venv/bin/activate

Install all of the dependencies:
pip install -r requirements.txt

Launch the local development server:
python manage.py runserver

Specifying exact versions in the requirements.txt file
is considered best practice because it ranges prevents
the installation of newer versions of dependencies that
might introduce incompatibility issues.

Include the following in .gitignore this way files
containing a .pyc extension are not pushed to GitHub.
*.pyc
__pycache__/
