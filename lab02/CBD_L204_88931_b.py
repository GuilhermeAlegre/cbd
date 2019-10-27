import pymongo
from datetime import datetime

client = pymongo.MongoClient(
    "mongodb://localhost:27017")
db = client.cbd  # we have selected the "cbd" database
rest = db.rest  # we have selected the "rest" collection

rest.create_index("localidade", name='localidade')
rest.create_index("gastronomia", name='gastronomia')
rest.create_index([("nome", pymongo.TEXT)], name='nome')


print(rest.index_information()) # checking existing indexes

