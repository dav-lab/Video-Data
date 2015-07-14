from pymongo import MongoClient
import json
import os

#creates a MongoClient to the running mongod instance
client = MongoClient()
#creates a database called data
data = client.data
#creates a collection called raw in data database
raw = data.raw

def insertRawData(dirName):
    students=os.listdir(dirName)
    for student in students:
        data = json.load(open(dirName+'/'+student))
        raw.insert_many(data)