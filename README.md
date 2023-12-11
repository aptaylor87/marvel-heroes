# Marvel Team Up

See it here: [https://marvel-team-up.onrender.com/](https://marvel-team-up.onrender.com/)

Github: [https://github.com/aptaylor87/marvel-heroes](https://github.com/aptaylor87/marvel-heroes)


## Description

This website works with Marvel's comic book API to allow users to search for comics that include shared appearances from two of their favorite characters. 

### Key Features

- Direct search using data from the Marvel API to get up to date lists of comics. This was chosen as a way to integrate a third-party API with the application.

- Create an account and manage a reading list of comics to save for later. This was chosen as a way to feature hashing/authentication and to add more depth to the user experience in the application. 

- There are also paginated search results. Marvel's API only returns 20 results for each request and requires follow-up requests with an offset parameter to get more results. This was worked into the comic results search with "previous" and "next" links showing 20 comics at a time.  

### Standard User Flow

Users land on the search page which includes a short description of how the application functions. They can enter the names of two character from Marvel Comics and start a search right away. 

In the search results users will see a list of comics with their title, descriptions and cover art, along with a link back to the pages on Marvel's website for the specific comic issue. If a user is not logged in each result will include a link with a call to action asking that the user sign up so they can manage their own reading list. If a user is logged in they'll either see a button to add the comic to their reading list, or a message stating that the item was added to the reading list already. 

There are forms to sign up or log in to your account. Users who are not logged in will see links to these pages in the top right of the website's navigation. After logging in, these links are replaced with links to view your reading list, or log out.

## API

https://developer.marvel.com/ 

There are several factors that may arise while working with the Marvel API that users should be aware of. 

- It has a very strict authentication system that requires a parameter be included with each request. The parameter is a combination of an always unique variable, such as a timestamp, the public API key Marvel issues you, and also a hashed combination of the timestamp and private API key Marvel issues you. Working with this authentication process in Python is laid out ver well in [this post from Stack Overflow](https://stackoverflow.com/questions/53356636/invalid-hash-timestamp-and-key-combination-in-marvel-api-call)

- Access to the API is limited to 3000 calls a day.

- The api has been unsupported since 2014.

- Making calls to the API to get results based on a character name is very picky. Captilization counts and spaces aren't tolerated. This makes it difficult to search for characters unless you know exactly own their names are spelt and capitalized in this system, which is particularly tricky with the names of superheroes. 

- The API will only serve 20 results in the resposne to each request. A combination of this and the 3000 daily call limit lead to righting the function used in the seed.py file to populate the characters table in the database with looped requests so this list wouldn't need to be called each time a search was run. It takes ~75 requests to get the full list of ~1550 characters. 

## Technology Stack


-Python
-Flask
-SQL Alchemy
-WTForms
-PostgreSql
-Javscript/jQuery
-CSS
-HTML




API

## DB Schema Diagram


https://app.quickdatabasediagrams.com/#/d/6FJbjZ
