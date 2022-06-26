# URL Shortener


## Description

This application is a URL shortener with ReactJS on the frontend, FastAPI on the backend and PostgreSQL as the database.

The shortened URL is generated by creating a UUID and shortening it to 10 characters. The chances of a collision (other URL with the same hash) is very low but we do have a retry mechanism which tries to generate a unique URL until it reaches the retry limit.

The shortened URL is a GET endpoint which redirects to the original website by retrieving the information from the database.

If a URL has already generated a shortened URL, the endpoint will provide back the previously generated shortened URL.

### How to run application
1. Install docker
2. Run `docker-compose up`
3. Visit http://localhost:3000 to view the webpage
4. Visit http://localhost:8080/docs/ to view the endpoints available on the backend


### Useful commands
To run the backend service without the frontend:

`docker-compose run --service-ports backend`


To run pytest on backend:

`docker-compose run --service-ports backend pytest .`

To run black on backend:

`docker-compose run --service-ports backend black .`

To run prettier on frontend:

`docker-compose run --service-ports frontend prettier --write .`

To run all services but force recreate and build images:

`docker-compose up --force-recreate --build`
