Navigate to the appropriate directory:
cd SeniorProject/src/django_project/

Activate the virtual environment:
source ./venv/bin/activate

Generate the requirements.txt file:
pip freeze > requirements.txt

Install all of the dependencies:
pip install -r requirements.txt

Launch the local development server:
python manage.py runserver

Create a super user:
python manage.py createsuperuser

You will be prompted to input the following
credentials:
Username: 
Email address: 
Password: 
Password (again):

Keep in mind that you can input your email
address for both username and email address.


Specifying exact versions in the requirements.txt file
is considered best practice because it ranges prevents
the installation of newer versions of dependencies that
might introduce incompatibility issues.

Make sure that dependencies in the requirements.txt
file contain underscores rather than hypens.

Include the following in .gitignore this way files
containing a .pyc extension are not pushed to GitHub.
*.pyc
__pycache__/

Virtual environments shouldn't be pushed to GitHub
due to their large size which can make cloning slower.

Database files mustn't be pushed to GitHub because
they may contain sensitive/confidential data.

Command for listing all of the dependencies
and their respective version specifiers:
pip freeze > requirements.txt

Version specifiers were included for the
dependencies in the requirements.txt file
because installing the latest versions may
generate bugs.

Execute the following commands in the
Senior_Project/django_project directory
to generate multiple blog posts.

Include all spaces and new lines:
python manage.py shell

import json
from blog.models import Post
with open('posts.json') as file:
  posts_json = json.load(file)

for post in posts_json:
  post = Post(m_title=post['title'], m_content=post['content'], m_author_id=post['user_id'])
  post.save()

exit()