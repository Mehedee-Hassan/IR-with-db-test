from pymongo import MongoClient
import pymongo

if __name__=='__main__':

    client = MongoClient('localhost',27017)

    mydb = client['cricket']


    print(mydb.players.find())