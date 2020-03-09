# HPotter-API

A graphene-sqlalchemy api to request data from the HPotter database

## Set Up
* `cd hpotter_api`
* `pip3 install -r requirements.txt`
* Update `dbUrl` in `config.yaml` to point to a database the SQLAlchemy can connect to
  * Current URL points to a dabase named `db.sqlite3` in the `hpotter_api/` dir
  * At test DB may be created using 
    * `cd .. # return to the directory containing hpotter_api`
    * `python3 -m hpotter_api.test`
    * `mv hpotter_api/test/db.sqlite3 hpotter_api/db.sqlite3`
* `python3 -m hpotter_api`
* The application will now be listening to localhost on the port listed in `config.yaml` (8080 default)
* You may now POST GraphQL queries to `localhost:<PORT>`

## Background
* Database tables are reflected and no schema configuration is required.
* A connection field for each table is made available to query.
* Each table has a query field named `all<table name>` with the first letter of the table name capitalized (e.g. allCredentials).
* Each of these fields is of type Connection and allows for pagination or simply requesting the entire table
* Connection types implement the [Connections Specification](https://facebook.github.io/relay/graphql/connections.htm). Connection type names have the format <table>GqlConnection (e.g. CredentialsGqlConnection)

## Querying
* Once the API is being served, queries can be made via HTTP POST requests to `localhost:<PORT>` using any convenient front end such as Postman or JavaScript.
* POSTs must include the `Content-Type: application/json` header
* POSTEed data must be valid JSON
* POSTed JSON must be valid GraphQL syntax
* See GraphQL resources for GraphQL syntax

Querying can be done from any convenient tool that can send HTTP POST requests, for example curl, Postman, or JavaScript.

Here is an example with `curl`

    `curl localhost:8080 --header Content-Type:application/json --data \
    '{"query":"{allCredentials{edges{node{username\n password\n connections{destIP\n destPort}}}}}"}'`

## Sample Query Bodies

* Get all credentials and their related entries in the connections table
  * Raw JSON

    `{"query":"{allCredentials{edges{node{username\n password\n connections{destIP\n destPort}}}}}"}`

  * Pretty JSON

    ```
    {
        allCredentials {
            edges {
                node {
                    username
                    password
                    connections {
                        destIP
                        destPort
                    }
                }
            }
        }
    }
    ```