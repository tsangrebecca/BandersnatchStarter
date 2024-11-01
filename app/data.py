# Run this file in terminal to generate monsters_data.html in the same working directory
# if not already exists

from os import getenv
from certifi import where
from dotenv import load_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient

# load environment variables from the .env file
#   with the MONGO URI, username and password (go to database access and 
#   do a one-time autogenerate pswd). Click Connect, and copy & paste connection string
#   with username and password onto .env
load_dotenv()

class Database:
    # write the constructor for the new object, initialize the class's attributes
    def __init__(self) -> None:
        # Fetch the MongoDB connection URL from environment variables in .env file
        self.mongo_url = getenv('MONGO_URL')

        # Set up MongoDB client to connect to a MongoDB database, takes the URL and establish secure connection
        #   with a certificate authority (CA) file
        self.client = MongoClient(self.mongo_url, tlsCAFile=where())

        # specify a particular database we want to work with
        self.db = self.client['monster_db']

        # and a specific collection
        self.collection = self.db['monsters']

    def seed(self, amount):
        '''Generate and insert 'amount' number of monsters into the collection.'''
        # Create a list of monster dictionaries: Monster() generates a random monster
        #   .to_dict() converts it into a dict format to store in database
        #   [... for _ in range(amount)] repeats this process 'amount' of times
        monsters = [Monster().to_dict() for _ in range(amount)]

        # Insert the list of monster dictionaries into the MongoDB collection in one go using pymongo method
        self.collection.insert_many(monsters)

        print(f"Seeded {amount} monsters to the database.")

    def reset(self):
        '''Delete all documents in the collection.'''
        self.collection.delete_many({}) 
        # ({}) not specifying any filter, so every document is deleted with a pymongo method
        print("Collection reset: all monsters deleted.")

    def count(self) -> int:
        '''Return the number of documents in the collection.'''
        return self.collection.count_documents({})
    
    def dataframe(self) -> DataFrame:
        '''Generate a pandas Dataframe from the collection's documents.'''
        # Retrieve all docs in the collection as a cursor, like a pointer to the data, but not the actual data
        #   (lazy loading - fetching docs in batches)
        cursor = self.collection.find()
        
        # Convert all docs in the cursor to a list, loading all docs into memory at once
        data = list(cursor)
        return DataFrame(data)

    def html_table(self) -> str:
        '''Generate an HTML table rep of the collection's docs to display on webpage.'''
        df = self.dataframe() # referring to the method within the class, so we need .self
        return df.to_html()


'''The following code block will run when script is executed as standalone program, 
a way to showcase the functionality of the Database class.'''
if __name__ == '__main__':

    # Set my current sprint value
    SPRINT = 1

    # Put the class I just created into good use
    db = Database()
   
    # print(db.mongo_url)

    # Seed the database with 1000 monsters
    db.seed(1000)

    # Get the number of docs in the collection
    print(f"Number of monsters in the collection: {db.count()}")

    # Generate and display the HTML table representation
    print(db.html_table())

    # Reset the collection aka delete all docs
    #db.reset()
    print("Collection has been reset. All monsters are deleted.")

    # Generate, write and save the HTML table representation to working directory
    html_output = db.html_table()
    with open("monsters_data.html", "w") as f:
        f.write(html_output)
    print("HTML table saved to monsters_data.html.")

# Use Git Bash to push code to Github instead of the VSCode terminal