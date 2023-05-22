# Import some necessary modules
# pip install kafka-python
# pip install pymongo
# pip install "pymongo[srv]"
from kafka import KafkaConsumer
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json
import subprocess



# replace here with your mongodb url 
uri = "mongodb+srv://adsoft:adsoft-sito@cluster0.kzghgph.mongodb.net/?retryWrites=true&w=majority"


# Create a new client and connect to the server
#client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection

#try:
#    client.admin.command('ping')
#    print("Pinged your deployment. You successfully connected to MongoDB!")
#except Exception as e:
#    print(e)

# Connect to MongoDB and pizza_data database

try:
    client = MongoClient(uri, server_api=ServerApi('1'))
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    db = client.memes
    print("MongoDB Connected successfully!")
except:
    print("Could not connect to MongoDB")

consumer = KafkaConsumer('test',bootstrap_servers=[
     'my-kafka-0.my-kafka-headless.kafka-adsoftsito.svc.cluster.local:9092'
    ])
# Parse received data from Kafka
for msg in consumer:
    record = json.loads(msg.value)
    print(record)
    name = record['name']

    # Create dictionary and ingest data into MongoDB
    try:
       meme_rec = {'name':name }
       print (meme_rec)
       meme_id = db.memes_info.insert_one(meme_rec)
       print("Data inserted with record ids", meme_id)

       #subprocess.call(['sh', './test.sh'])

    except:
       print("Could not insert into MongoDB")
    
    

    # Create dictionary and ingest data into MongoDB
    try:
       agg_result= db.memes_info.aggregate(
       [{
         "$group" : 
         {  "name" : "$name", 
            "n"    : {"$sum" : 1}
         }}
       ])

       for i in agg_result:
         print(i)

    except Exception as e:
       print(f'group by caught {type(e)}: ')
       print(e)
    
