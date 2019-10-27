import pymongo
from datetime import datetime

client = pymongo.MongoClient(
    "mongodb://localhost:27017")
db = client.cbd  # we have selected the "cbd" database
rest = db.rest  # we have selected the "rest" collection


def insert_restaurant(restaurant):
    """
    Method that allows to inser a Restaurant object to rest collection.
    It also prints que inserted restaurant id

    @param restaurant: Restaurant object to be inserted
    @param nome:
    """
    inserted_restaurant = rest.insert_one(restaurant)
    print(inserted_restaurant.inserted_id)


def search_restaurant(localidade=None, nome=None):
    """
    Method that allows to search the collection of restaurnts for "localidade" and "nome"

    @param localidade:
    @param nome:
    """
    if localidade is not None and nome is not None:
        for entry in rest.find({"localidade": localidade, "nome": nome}):
            print(entry)

    elif localidade is not None:
        for entry in rest.find({"localidade": localidade}):
            print(entry)

    elif nome is not None:
        for entry in rest.find({"nome": nome}):
            print(entry)


def main():
    # Search all Restaurants in Manhattan
    search_restaurant(localidade="Manhattan")

    # Insert 3 restaurants
    insert_restaurant({"address": {"building": "3906", "coord": [-73.9851356, 40.7676919], "rua": "Avenida Afonso Costa", "zipcode": "10466"}, "localidade": "Lisbon", "gastronomia": "Portuguese", "grades": [{"date": datetime(2014, 5, 12, 0, 0), "grade": "A", "score": 9}, {"date": datetime(
        2013, 10, 7, 0, 0), "grade": "A", "score": 6}, {"date": datetime(2012, 10, 4, 0, 0), "grade": "A", "score": 10}, {"date": datetime(2011, 10, 5, 0, 0), "grade": "A", "score": 9}, {"date": datetime(2011, 6, 30, 0, 0), "grade": "A", "score": 7}], "nome": "Galo", "restaurant_id": "40899178"})

    insert_restaurant({"address": {"building": "3906", "coord": [-73.9851356, 40.7676919], "rua": "Avenida Afonso Costa", "zipcode": "10466"}, "localidade": "Lisbon", "gastronomia": "Portuguese", "grades": [{"date": datetime(2014, 5, 12, 0, 0), "grade": "A", "score": 9}, {"date": datetime(
        2013, 10, 7, 0, 0), "grade": "A", "score": 6}, {"date": datetime(2012, 10, 4, 0, 0), "grade": "A", "score": 10}, {"date": datetime(2011, 10, 5, 0, 0), "grade": "A", "score": 9}, {"date": datetime(2011, 6, 30, 0, 0), "grade": "A", "score": 7}], "nome": "Galo", "restaurant_id": "40899178"})

    insert_restaurant({"address": {"building": "3906", "coord": [-73.9851356, 40.7676919], "rua": "Avenida Afonso Costa", "zipcode": "10466"}, "localidade": "Lisbon", "gastronomia": "Portuguese", "grades": [{"date": datetime(2014, 5, 12, 0, 0), "grade": "A", "score": 9}, {"date": datetime(
        2013, 10, 7, 0, 0), "grade": "A", "score": 6}, {"date": datetime(2012, 10, 4, 0, 0), "grade": "A", "score": 10}, {"date": datetime(2011, 10, 5, 0, 0), "grade": "A", "score": 9}, {"date": datetime(2011, 6, 30, 0, 0), "grade": "A", "score": 7}], "nome": "Galo", "restaurant_id": "40899178"})

    # Insert a Restaurant located in Porto
    insert_restaurant({"address": {"building": "3906", "coord": [-73.9851356, 40.7676919], "rua": "Avenida Afonso Costa", "zipcode": "10466"}, "localidade": "Porto", "gastronomia": "Portuguese", "grades": [{"date": datetime(2014, 5, 12, 0, 0), "grade": "A", "score": 9}, {"date": datetime(
        2013, 10, 7, 0, 0), "grade": "A", "score": 6}, {"date": datetime(2012, 10, 4, 0, 0), "grade": "A", "score": 10}, {"date": datetime(2011, 10, 5, 0, 0), "grade": "A", "score": 9}, {"date": datetime(2011, 6, 30, 0, 0), "grade": "A", "score": 7}], "nome": "Galo", "restaurant_id": "40899178"})

    # Search all Restaurants located in Lisbon
    search_restaurant(localidade="Lisbon")

    # Set localidade to Aveiro to all Restaurants that are located in Lisbon
    update_query = {"localidade": "Porto"}
    new_values = {"$set": {"localidade": "Aveiro"}}

    update_result = rest.update_many(update_query, new_values)
    print(update_result.modified_count, "documents updated!")

    # Search all Restaurants in Aveiro
    search_restaurant(localidade="Aveiro")


if __name__ == "__main__":
    main()
