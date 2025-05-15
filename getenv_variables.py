from dotenv import load_dotenv
import os

load_dotenv()

GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_PASS = os.getenv('GMAIL_PASS')
CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
API_KEY = os.getenv('CLOUDINARY_API_KEY')
API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

print("GMAIL_USER:", GMAIL_USER)
print("GMAIL_PASS:", GMAIL_PASS)
print("CLOUD_NAME:", CLOUD_NAME)
print("API_KEY:", API_KEY)
print("API_SECRET:", API_SECRET)