# URL Shortener


## Description

This application is a URL shortener with ReactJS on the frontend, FastAPI on the backend and PostgreSQL as the database.


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
