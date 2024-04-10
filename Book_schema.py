from pymongo import MongoClient


def connect_to_mongodb(url):
    client = MongoClient(url)
    return client

client_url = 'mongodb://localhost:27017/'
client = connect_to_mongodb(client_url)

book_structure = {
    "title": "string",
    "author": "string",
    "genre": "string",
    "copies_available":"integer" ,
    "total_copies": "integer"
}

borrower_structure = {
    "book_id":"string",
    "user_id":"string",
    "allotted_on": "datetime",
    "returned_on": "datetime"
}

user_structure = {
    "name":"String",
    "email":" string",
    "phone_number":"string"
}

def data_collection_creator(url, dbName):
    client = MongoClient(url)
    db = client["Book"]
    collection = db[dbName]
    return collection

def insert_data_to_db(collection, data):
    result = collection.insert_one(data)
    return result.inserted_id

def create_data_from_structure(structure):
    data = {}
    for key, value in structure.items():
        if isinstance(value, dict):
            data[key] = create_data_from_structure(value)
        else:
            data[key] = value() if callable(value) else value
    return data

book_collection = data_collection_creator(client_url, 'Books')
borrower_collection = data_collection_creator(client_url, 'Borrowers')
user_collection = data_collection_creator(client_url, 'Users')

book_data = create_data_from_structure(book_structure)
borrower_data = create_data_from_structure(borrower_structure)
user_data = create_data_from_structure(user_structure)

book_id = insert_data_to_db(book_collection, book_data)
borrower_data['book_id'] = book_id

user_id = insert_data_to_db(user_collection, user_data)
borrower_data['user_id'] = user_id

borrower_id = insert_data_to_db(borrower_collection, borrower_data)

client.close()
