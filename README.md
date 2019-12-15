# assignment

## this assignment implements the following functionalities
1. on create or update of a entity in database it throws a signal and stores the message regarding changed values of fields
2. on update of file content automatically updates the encrypted content stored in the database

## how to use the system
to use the system run the server and go to home page.
the create link there helps you create an entity of MyModel in database
the links of the entities apearing below it aloow you update corresponding entity

#### note: dont use django admin site for adding or updating to database as admin site works on different functions as a superuser so the result might not be as expected
eg: it will not update the value of encrypted field.

#### note: the python module cryptography is used for encryption purpose make sure it is installed in the system

## ThankYou!
