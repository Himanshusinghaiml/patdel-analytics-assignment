

# schema desgin
+---------------------+     1    +-----------------------+
|      Account        |----------|     Destination        |
+---------------------+          +-----------------------+
| email (PK)          |          | url                   |
| account_id (PK)     |          | http_method           |
| account_name        |          | headers               |
| app_secret_token    |          | destination_id (PK)   |
| website             |          | account_id (FK)       |
+---------------------+          +-----------------------+
# Relationships
Account to Destination
Relationship Type: One-to-Many
Description: An account can have multiple destinations. Each destination is associated with exactly one account.


# Explanation
Account: This entity has a unique account_id which is the primary key. It also includes an app_secret_token used for authentication.

Destination: Each destination is identified by a unique destination_id. It has a foreign key account_id that links it to the Account entity. The headers attribute stores the headers in JSON format.

Relationship: The relationship between Account and Destination is one-to-many, meaning one account can have multiple destinations.



 
# Account Endpoints:

/account: Create an account.
/account/{account_id}: Get,  
Destination Endpoints:

/destination/{account_id}: Create a new destination for an account.
/destinations/{account_id}: Get all destinations for an account.
/destination/{account_id}/{destination_id}: Update or delete a specific destination.

Data Handling Endpoint:
/server/incoming_data: Accept JSON data, validate the app secret token, and forward the data to specified destinations.


 