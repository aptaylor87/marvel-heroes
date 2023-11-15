## What goal will your website be designed to achieve?

This website will allow users to quickly find Marvel comics based on a search of two of their favorite characters.  This could be a search for two heroes working together or a showdown between a specific hero and a villain. Users will also be able to keep a reading list of comics they’re interested in and ones they’ve completed. 

## What kind of users will visit your site?

Fans of Marvel comics will visit the site, whether it is someone interested in finding a good place to start with comics or a seasoned reader who is looking for the next spot to go with their catalog. 


## What data do you plan on using?

I plan on using the Marvel API. It is a large catalog with information and images related to the heroes and individual issues for all Marvel Comics. 

Tables will need to be stored for users, characters, comics, as well as a table to track details about a reading list for each user.

https://developer.marvel.com/ 

## Approach Outline

### What does your database schema look like?

https://docs.google.com/spreadsheets/d/1-ng2zPcjF1_ODzZJdi6T0KHZL5TKiw-jYd8HkRSJLQI/edit#gid=0  

### What kind of issues might you run into with your API?

The API does not have a strong search function, characters need an exact name match or there is an option for a “starts with” queries but that is it. There also seem to be individual records for different variations on characters, like “Spider-Man” as well as “Spider-Man(Ultimate)”

Responses are also limited to 20 results with the need to run an offset call to get more results. 


### Is there any sensitive information you need to secure?

Passwords will need to be hashed and stored. Otherwise I will minimize use of user info.

### What functionality will your app include?

The app will include functionality to create an account, including sign-in. Users will be able to run a search for comics based on a selection of up to two characters. Users will also be able to save the results into a reading list of comics that will display information about which characters they were searching for when they added that comic, whether or not they’ve read the comic, and the date it was marked read. 

### What will the user flow look like?

Users will arrive at the application on a page that will prompt them to run a search or create an account. Running a search will involve picking two (or just one) characters that the user would like to find comics for. A list of results will appear. If a user has an account and is signed in, they will be able to select comics to add to their reading list.  

### What features make your site more than crud?

The ability to cross-reference comics based on two different characters takes this site more that a simple crud application. It will also include links to Marvel's wiki pages for the characters and comic issues. 

	
