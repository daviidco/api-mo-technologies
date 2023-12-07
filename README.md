# api-mo-technologies
Api technical assessment

The IT project includes a technical assessment for MO Technologies. It is a REST API built with Django Rest Framework

## Prerequisites

- Docker
- Docker Compose


## Instructions

1. Once configured your SSH key with open-ssh and configured your key at github setting (More info: https://docs.github.com/es/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account):
```bash
git clone git@github.com:daviidco/api-mo-technologies.git
```
2. Navigate to the cloned repository directory:

```bash
cd techinical_test
```

3. Build and run the services with Docker Compose:

```bash
docker-compose up --build
```

Once the services are running, you can access the React application at http://localhost and the Flask API at http://localhost/api. The Flask API communicates with the PostgreSQL database. Nginx is responsible for routing the requests from the React application to the Flask API.

4. Stop and remove the services and volumes

To stop and remove the services, volumes, and networks created by Docker Compose, run the following command:

```bash
docker-compose down --volumes
```