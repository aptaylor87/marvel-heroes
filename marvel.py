# import dependencies
import hashlib  #this is needed for the hashing library
import time   #this is needed to produce a time stamp
import json   #Marvel provides its information in json format
import requests #This is used to request information from the API

#Constructing the Hash
m = hashlib.md5()   #I'm assigning the method to the variable m.  Marvel 
    #requires md5 hashing, but I could also use SHA256 or others for APIS other 
    #than Marvel's 

ts = str(time.time())   #This creates the time stamp as a string
ts_byte = bytes(ts, 'utf-8')  #This converts the timestamp into a byte 
m.update(ts_byte)  # I add the timestamp (in byte format) to the hash
m.update(b"acf95fb90a0b3f733f802f5321656d6f51d1f6c7") #I add the private key to 
    #the hash.Notice I added the b in front of the string to convert it to byte 
    #format, which is required for md5
m.update(b"3c53fc3b517b663bf6aabdf7db6177f5") #And now I add my public key to 
    #the hash
hasht = m.hexdigest()    #Marvel requires the string to be in hex; they 
    #don't say this in their API documentation, unfortunately.

#constructing the query
base_url = "https://gateway.marvel.com"  #provided in Marvel API documentation
api_key = "3c53fc3b517b663bf6aabdf7db6177f5" #My public key
query = "/v1/public/characters" +"?"  #My query is for all the events in Marvel Uni

#Building the actual query from the information above
query_url = base_url + query +"ts=" + ts+ "&apikey=" + api_key + "&hash=" + hasht
print(query_url) #I like to look at the query before I make the request to 
    #ensure that it's accurate.

#Making the API request and receiving info back as a json
data = requests.get(query_url).json()
print(data)  #I like to view the data to make sure I received it correctly