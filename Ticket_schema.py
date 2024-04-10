import pymongo
from faker import Faker
from datetime import datetime

MONGO_CLIENT = "mongodb://localhost:27017/"
DB_NAME = "cricket"
COLLECTION = "tickets"

core_structure = {
    "date":"datetime",
    "venue":"geolocation",
    "rate":"float"
}

structure = {
    "core":core_structure,
    "title": "string"
}

fake = Faker()

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_CLIENT)
database = client[DB_NAME]
collection = database[COLLECTION]

# Generate random ticket type
ticket_types = ["diamond", "silver", "general"]
ask = fake.random_element(ticket_types)

# Generate random number of tickets sold
tickets_sold = fake.random_int(min=1, max=1000)


def create_data_event(total, sold_count):
    diamond = int(0.05 * total)
    silver = int(0.25 * total)
    general = int(0.7 * total)

    if ask == "diamond":
        diamond = max(0, 250)
    elif ask == "silver":
        silver = max(0, 1250)
    else:
        general = max(0, 3500)

    tickets = {
        "total": total,
        "diamond": diamond,
        "silver": silver,
        "general": general,
        "sold": sold_count,
        "created_at": datetime.now()
    }
    # Creates a dictionary tickets containing information about ticket types, total tickets, tickets sold, and remaining tickets.
    document_id = collection.insert_one(tickets).inserted_id
    return document_id
    # Inserts the tickets dictionary into the MongoDB collection named "tickets" and returns the ID of the inserted document.


def sold(n, document_id):
    # Find the current ticket document
    current = collection.find_one({"_id": document_id})

    # Update the "sold" field for the specific ticket type
    ticket_type = ask
    current[ticket_type] -= n

    if current[ticket_type] < 0:
        print(f"All {ticket_type} tickets have been sold.")
        return 0

    # Update the document in the collection
    collection.update_one({"_id": document_id}, {"$set": {ticket_type: current[ticket_type]}})

    # Log the sales event
    log_sale_event(document_id, n)

    # Calculate remaining tickets for the specific ticket type
    remaining = current[ticket_type]

    return max(remaining, 0)
# Function to log sales event
def log_sale_event(document_id, sold_count):
    event = {
        "ticket_id": document_id,
        "sold tickets": sold_count,
        "timestamp": datetime.now()
    }
    # Insert the sales event into a separate collection named "sales_events"
    database["sales_events"].insert_one(event)


# Function to get remaining tickets
def remaining(document_id):
    current = collection.find_one({"_id": document_id})
    remaining = current["total"] - current["sold"]

    return max(remaining, 0)


document_id = create_data_event(5000, tickets_sold)
remaining = sold(tickets_sold, document_id)

print(f"{tickets_sold} {ask} tickets sold. Remaining tickets: {remaining}.")
