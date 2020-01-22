from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "ex4"))


def show_character_name(tx):
    for record in tx.run("match (c:Character) return c"):
        print(f"[Character]  name: {record['c']['name']}")


def show_characters_that_interacted_with(tx, name):
    for record in tx.run(
        "match (c:Character {name : '"
        + name
        + "'}) - [:INTERACTS] - (b:Character) return b.name , c.name",
        name=name,
    ):
        print(f"{record['b.name']} interacts with {record['c.name']}")


def count_connections(tx):
    for record in tx.run(
        "match (c:Character) - [:INTERACTS] - (:Character) with c.name as name, count(*) as number_of_connections return name, number_of_connections"
    ):
        print(
            f"[Number of connections] char name: {record['name']}, number_of_connections: {record['number_of_connections']}"
        )


def shortest_path(tx):
    for record in tx.run("MATCH (garth:Character {name:'Garth-Tyrell'}), (catelyn:Character {name:'Catelyn-Stark'}) MATCH p=shortestPath((garth)-[:INTERACTS*]-(catelyn)) RETURN p"):
        nodes = [node["name"] for node in record["p"].nodes]
        print(f"Shortest Path between Garth-Tyrell and Catelyn Stark: {nodes}")


def top_10_charecters_connections(tx):
    for record in tx.run(
        "match (c:Character) - [:INTERACTS] - (:Character) with c.name as name, count(*) as number_of_connections return name, number_of_connections order by number_of_connections desc limit 10"
    ):
        print(
            f"[Number of connections] char name: {record['name']}, number_of_connections: {record['number_of_connections']}"
        )

def length_of_paths_between_starks_and_martells(tx):
    for record in tx.run("match p=shortestPath((a:Character)-[*]-(b:Character)) where a.name ends With 'Stark' and b.name ends with 'Martell' return a.name as Stark, b.name as Martell, length(p) as length"):
        print(f"Length of path between [Stark] {record['Stark']} and [Martell] {record['Martell']}: {record['length']}")

def size_of_house_targaryen(tx):
    for record in tx.run("match (a:Character) where a.name ends with 'Targaryen' return length(collect(a.name)) as size"):
        print(
            f"House Targaryen has {record['size']} elements registered."
        )

def top_10_page_rank(tx):
    for record in tx.run("match (char:Character) with collect(char) as nodes call apoc.algo.pageRankWithConfig(nodes, {types:'INTERACTS'}) yield node, score return node.name as character, score order by score desc limit 10"):
        print(f"Character: {record['character']} || Score: {record['score']}")

def most_far_character(tx, name):
    for record in tx.run("match p=shortestPath((a:Character)-[*]-(b:Character { name:'" + name + "'})) WHERE  a.name <> b.name RETURN a.name as name, length(p) as length ORDER BY length(p) DESC LIMIT 1"):
        print(f"Character: {record['name']} || Length: {record['length']}")

def biggest_distance(tx):
    for record in tx.run("match p=shortestPath((a:Character)-[*]-(b:Character)) where a.name <> b.name return a.name, b.name, length(p) ORDER BY length(p) DESC LIMIT 1"):
        print(f"(Character: {record['a.name']} , Character: {record['b.name']}) | length: {record['length(p)']}")
"""
def most_reviews(tx):
    for record in tx.run("MATCH (u:User)-[w:WROTE]->(r:Review) return u,count(w) as total ORDER BY total DESC LIMIT 1"):
        print(f"Who wrote the most reviews: user id-> {record['u']['user_id']}, total -> {record['total']}")

def avg_listing_price(tx):
    for record in tx.run("MATCH (u:Host)-[t:HOSTS]->(l:Listing) return u,avg(l.price) as avg"):
        print(f"Average price of listings for host: host id-> {record['u']['host_id']}, average price -> {record['avg']}")

def listing_price(tx,name):
    for record in tx.run("MATCH (l:Listing {name: {name} }) return l ORDER BY l.price ASC LIMIT 10",name=name):
        print(f"Listing {name} price: id-> {record['l']['name']}, price-> {record['l']['price']}")

def count_reviews(tx,):
    for record in tx.run("MATCH (n:Review)-[t:REVIEWS]->(l:Listing) return l,count(t) as total"):
        print(f"Number of reviews for listing : id-> {record['l']['listing_id']}, total-> {record['total']}")"""


with driver.session() as session:
    session.read_transaction(show_character_name)
    print()
    session.read_transaction(show_characters_that_interacted_with, "Arya-Stark")
    print()
    session.read_transaction(count_connections)
    print()    
    session.read_transaction(shortest_path)
    print()
    session.read_transaction(top_10_charecters_connections)
    print()
    session.read_transaction(length_of_paths_between_starks_and_martells)
    print()
    session.read_transaction(size_of_house_targaryen)
    print()
    session.read_transaction(top_10_page_rank)
    print()
    session.read_transaction(most_far_character, "Varys")
    print()
    session.read_transaction(biggest_distance)


driver.close()

