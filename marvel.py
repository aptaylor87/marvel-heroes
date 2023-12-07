# https://stackoverflow.com/questions/53356636/invalid-hash-timestamp-and-key-combination-in-marvel-api-call

# import dependencies
import hashlib  #This is needed for the hashing library
import time   #This is needed to produce a time stamp
import requests #This is used to request information from the API
from secret import API_PRIVATE_KEY_BYTES, API_PUBLIC_KEY_BYTES, API_PUBLIC_KEY
from models import db, Character, Comic

#Constructing the Hash
m = hashlib.md5()   #This assigns the method to the variable m.  Marvel 
    #requires md5 hashing for authentication in their API.
ts = str(time.time())   #This creates the time stamp as a string.
ts_byte = bytes(ts, 'utf-8')  #This converts the timestamp into a byte 
m.update(ts_byte)  # This adds the timestamp (in byte format) to the hash
m.update(API_PRIVATE_KEY_BYTES) #This the private key to 
    #the hash. The private key is stored in the secret.py file and needs to be stored in this variable in byte format
m.update(API_PUBLIC_KEY_BYTES) #This adds the public key to 
    #the hash which is set up the same way as the private key.
hasht = m.hexdigest()    #Marvel requires the string to be in hex, even those this isn't noted in their documentation.

#constructing the base query
base_url = "http://gateway.marvel.com/v1/public/"  #provided in Marvel API documentation
api_key = API_PUBLIC_KEY #This is not a duplication. It is the public key saved to a variable in non-byte format which needs to be included in the authentication parameter for queries.



def get_character_info(charactername):
    """This function will take the text name of a charcter and return a dict with their name, description, image url and url for a link to the marvel sit."""
    query = f"characters?name={charactername}"
    query_url = base_url + query + "&ts=" + ts + "&apikey=" + api_key + "&hash=" + hasht
    print(query_url)
    data = requests.get(query_url).json()['data']['results'][0]
    
    heroname = data['name']
    description = data['description'] 
    image = data['thumbnail']['path'] + '/portrait_xlarge.' + data['thumbnail']['extension']
    wiki = data['urls'][2]['url']
    hero = {"name": heroname, "description": description, "image": image, "wiki": wiki }
    return(hero)

# This is used in the seed.py file to seed the characters table
def get_all_characters():
    """This funciton is used in the seed.py file to populate the characters table with all 1563 characters in the API."""
    offset = 0
    while offset <= 1560:
        query = f"characters?offset={offset}"
        query_url = base_url + query + "&ts=" + ts + "&apikey=" + api_key + "&hash=" + hasht
        data = requests.get(query_url).json()['data']['results']
        characters = []
        for i in range(len(data)):
            id = data[i]['id']
            name = data[i]['name']
            description = data[i]['description']
            marvel_url = data[i]['urls'][0]['url']
            image_url = data[i]['thumbnail']['path']
            image_type = data[i]['thumbnail']['extension']   
            characters.append(Character(id=id,name=name,description=description, marvel_url=marvel_url,image_url=image_url,image_type=image_type))
            offset += 1
        db.session.add_all(characters)
        db.session.commit()
    print(f"Added {offset} records")


def get_shared_appearances(character_one, character_two, offset = 0):
    query = f"characters/{character_one}/comics?sharedAppearances={character_two}&offset={offset}"
    query_url = base_url + query + "&ts=" + ts + "&apikey=" + api_key + "&hash=" + hasht
    data = requests.get(query_url).json()['data']
    results = data['results']
    comics = []
    for i in range(len(results)):
        id = results[i]['id']
        title = results[i]['title']
        description = results[i]['description']
        marvel_url = results[i]['urls'][0]['url']
        image_url = results[i]['thumbnail']['path']
        image_type = results[i]['thumbnail']['extension']
        comics.append({"id":id,"title": title, "description": description, "marvel_url": marvel_url, "image_url": image_url, "image_type":image_type})
        total_results = data['total']
    return comics, total_results


def get_comic(id):
    query = f"comics/{id}?"
    query_url = base_url + query + "&ts=" + ts + "&apikey=" + api_key + "&hash=" + hasht
    data = requests.get(query_url).json()['data']['results'][0]
    comic = Comic(id=data['id'],title=data['title'],description=data['description'], image_url=data['thumbnail']['path'], image_type=data['thumbnail']['extension'], marvel_url=data['urls'][0]['url'])

    return comic
