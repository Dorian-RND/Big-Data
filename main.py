import json
from pymongo import MongoClient
if __name__ == '__main__':

    # Making Connection
    myclient = MongoClient("mongodb+srv://bigData:comptedevfac72@cluster0.ot9fmac.mongodb.net/?retryWrites=true&w=majority")

    # database
    db = myclient["BIGDATA"]

    # Created or Switched to collection
    # names: GeeksForGeeks
    Collection = db["data"]

    # Loading or Opening the json file
    with open('data.json') as file:
        file_data = json.load(file)

    # Inserting the loaded data in the Collection
    # if JSON contains data more than one entry
    # insert_many is used else insert_one is used
    if isinstance(file_data, list):
        Collection.insert_many(file_data)
    else:
        Collection.insert_one(file_data)
