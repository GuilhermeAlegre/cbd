# MongoDB Cheat Sheet

## Installation

 1. `wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -`
 2. `echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list`
 3. `echo "mongodb-org hold" | sudo dpkg --set-selections
echo "mongodb-org-server hold" | sudo dpkg --set-selections
echo "mongodb-org-shell hold" | sudo dpkg --set-selections
echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
echo "mongodb-org-tools hold" | sudo dpkg --set-selections`
 4. `sudo systemctl unmask mongodb`
 5. `sudo service mongodb start`
 6. `sudo service mongod stop`
 7. `sudo service mongod restart`
 8. `mongo`

## Advantages of MongoDB over RDBMS

-   **Schema less**  − MongoDB is a document database in which one collection holds different documents. Number of fields, content and size of the document can differ from one document to another.
-   Structure of a single object is clear.
-   No complex joins.
-   Deep query-ability. MongoDB supports dynamic queries on documents using a document-based query language that's nearly as powerful as SQL.
-   Tuning.
-   **Ease of scale-out**  − MongoDB is easy to scale.
-   Conversion/mapping of application objects to database objects not needed.
-   Uses internal memory for storing the (windowed) working set, enabling faster access of data.

## Why Use MongoDB?

-   **Document Oriented Storage**  − Data is stored in the form of JSON style documents.
-   Index on any attribute
-   Replication and high availability
-   Auto-sharding
-   Rich queries
-   Fast in-place updates 
-   Professional support by MongoDB
    

## Where to Use MongoDB?
-   Big Data
-   Content Management and Delivery
-   Mobile and Social Infrastructure
-   User Data Management
-   Data Hub


## Tutorial

### Create Database

- Execute the command: `use <DBNAME>`.  If the specified db does noy exist, it will be created. Otherwise, it is returned.

- To check your currently selected database, use the command : `db`
- If you want to check your databases list, use the command `show dbs`.
- If the database does not have any data, it is not displayed in the previous command.

### Drop Database

- Execute the command: `db.dropDatabase()`
- This will delete the selected database.
- If you have not selected any database, then it will delete default 'test' database.

### Create Collection

- Collections are created automatically when you insert a new document but if you want to create one this is the command: `db.createCollection(name,options)`
- Examples:
	- `db.createCollection("mycollection")`
	- `db.createCollection("mycol",  { capped :  true, autoIndexId :  true, size :  6142800, max :  10000  }  )`

- Simple Usage:

| Parameter | Type | Description |
|--|--|--|
| Name | String | Name of the collection to be created |
| Options | Document | (Optional) Specify options about memory size and indexing |

- Option Parameters:

| Field | Type | Description |
|--|--|--
| capped | Boolean | (Optional) If true, enables a capped collection. Capped collection is a fixed size collection that automatically overwrites its oldest entries when it reaches its maximum size.  **If you specify true, you need to specify size parameter also.** |
| autoIndexId | Boolean | (Optional) If true, automatically create index on _id field.s Default value is false. |
|size | number | (Optional) Specifies a maximum size in bytes for a capped collection.  **If capped is true, then you need to specify this field also.** |
| max | number | (Optional) Specifies the maximum number of documents allowed in the capped collection. |

### Drop Collection

- Execute the command: `db.COLLECTION_NAME.drop()`
- `drop()` method will return **true**, if the selected collection is dropped successfully, otherwise it will return false.

### Insert Document
- To insert data into MongoDB collection, you need to use MongoDB's **insert()** or **save()** method.
- The basic syntax of  **insert()**  command is as follows: `db.COLLECTION_NAME.insert(document)`
- Example:
	```
	 db.mycol.insert({
		 title:  'MongoDB Overview',
		 description:  'MongoDB is no sql database', 
		 by:  'tutorials point',
		 url:  'http://www.tutorialspoint.com',
		 tags:  ['mongodb',  'database',  'NoSQL'],
		 likes:  100 
	})
	```

	```
	db.mycol.insert([
		{
			title:  'MongoDB Overview',
			description:  'MongoDB is no sql database',
			by:  'tutorials point', 
			url:  'http://www.tutorialspoint.com', 
			tags:  ['mongodb',  'database',  'NoSQL'], 
			likes:  100  
		},
		
		{
			title:  'NoSQL Database', 
			description:  "NoSQL database doesn't have tables",  
			by:  'tutorials point', 
			url:  'http://www.tutorialspoint.com', 
			tags:  ['mongodb',  'database',  'NoSQL'], 
			likes:  20,
			comments:  [
				{
					user:'user1',
					message:  'My first comment',
					dateCreated:  new  Date(2013,11,10,2,35),
					like:  0 
				}  
			] 
		} 
	])
	```

### Query Document

- The basic syntax of  **find()**  method is as follows: `db.COLLECTION_NAME.find()`
- To display the results in a formatted way, you can use **pretty()** method: `db.mycol.find().pretty()`

| Operation | Example | RDBMS Equivalent |
|--|--|--|
| Equality | `db.mycol.find({"by":"tutorials point"}).pretty()` | where by = 'tutorials point' |
| Less Than | `db.mycol.find({"likes":{$lt:50}}).pretty()` | where likes < 50 | 
| Less Than Equals | `db.mycol.find({"likes":{$lte:50}}).pretty()` |where likes <= 50 |
| Greater Than | `db.mycol.find({"likes":{$gt:50}}).pretty()` | where likes > 50 |
| Greater Than Equals | `db.mycol.find({"likes":{$gte:50}}).pretty()` | where likes >= 50 |
| Not Equals | `db.mycol.find({"likes":{$ne:50}}).pretty()` | where likes != 50 |
| And | `db.getCollection('mycol').find({$and:[{"likes":{$ne:50}},{"title": "MongoDB Overview"}]}).pretty()` | |
 | Or | `db.getCollection('mycoll').find({"likes":  {$gt:10},$or:[{"likes":{$ne:50}},{"title": "MongoDB Overview"}]}).pretty()` | |

#### Update Document

- The basic syntax of  **update()**  method is as follows: `db.COLLECTION_NAME.update(SELECTION_CRITERIA, UPDATED_DATA)`
- Example: `db.mycol.update({'title':'MongoDB Overview'},{$set:{'title':'New MongoDB Overview'}})`

####
