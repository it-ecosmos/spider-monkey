import re
from faker import Faker
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["Dictionary"]
collections = db["Dictionary"]

fake = Faker()

STRING_DICTIONARY = {"location", "name", "city", "town", "address", "email", "phone_number", "zipcode", "country", "state", "street", "username", "password", "description", "title", "company", "department", "job_title", "website", "libraryname", "bookname"}

def generate_fake_details():
    fake_details = {}
    for field in STRING_DICTIONARY:
        if re.search(r'name', field):
            fake_details[field] = fake.name()
        elif re.search(r'title',field):
            fake_details[field]=fake.sentence()
        else:
            fake_method = getattr(fake, field, None)
            if fake_method:
                fake_details[field] = fake_method()
    return fake_details

fake_details = generate_fake_details()
print(fake_details)
collections.insert_one(fake_details)
