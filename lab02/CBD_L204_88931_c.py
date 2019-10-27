import pymongo
from datetime import datetime

client = pymongo.MongoClient(
    "mongodb://localhost:27017")
db = client.cbd  # we have selected the "cbd" database
rest = db.rest  # we have selected the "rest" collection


def count_localidades():
    """
    Method that counts the number of distinct localidades throughout all restaurants int the collection
    
    @rtype: int
    @returns: the number of distinct localidades
    """
    query = rest.aggregate(
        [{"$group": {"_id": "$localidade", "total": {"$sum": 1}}}])
    return len(list(query))


def count_rest_by_localidade():
    """
    Method that counts the number of restaurants that exist in each distinct localidade
    
    @rtype: list of tuple with (localidade, number_of_restaurants)
    @returns: A list with the number of restaurants for each localidade
    """
    query = rest.aggregate(
        [{"$group": {"_id": "$localidade", "total": {"$sum": 1}}}])

    return [(entry["_id"], entry["total"]) for entry in list(query)]


def count_rest_by_localidade_by_gastronomia():
    """
    Method that counts the number of restaurants that exist in each distinct (localidade and gastronomia)
    
    @rtype: list of tuple with (localidade | gastronomia, number_of_restaurants)
    @returns: A list with the number of restaurants for each (localidade and gastronomia)
    """
    query = rest.aggregate(
        [{"$group": {"_id": {"localidade": "$localidade", "gastronomia": "$gastronomia"}, "total": {"$sum": 1}}}])

    return [(f"{entry['_id']['localidade']} | {entry['_id']['gastronomia']}", entry["total"]) for entry in list(query)]


def get_rest_with_name_closer_to(name):
    """
    Method that returns the restaurants that have _name_ in it's name
    
    @rtype: list
    @returns: A list with the restaurants that have _name_ in it's name
    """
    query = rest.find({"nome": {"$regex": name}})

    return [entry["nome"] for entry in list(query)]


def main():
    # get the number of distinct localidades
    print(f"Número de localidades distintas: {count_localidades()}")

    # get the number of restaurants per localidade
    print("\nNúmero de localidades distintas:")
    for count in count_rest_by_localidade():
        print(f"  -> {count[0]}: {count[1]}")

    # get the number of restaurants per localidade and gastronomy
    print("\nNúmero de restaurantes por localidade e gastronomia:")
    for count in count_rest_by_localidade_by_gastronomia():
        print(f"  -> {count[0]}: {count[1]}")

    # get the restaurants that have 'Park' in the name
    print("\nNome de restaurantes que têm 'Park' no nome: ")
    for rest in get_rest_with_name_closer_to("Park"):
        print(f"  -> {rest}")


if __name__ == "__main__":
    main()
