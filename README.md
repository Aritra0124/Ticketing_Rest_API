# Ticketing_Rest_API

# Getting-Started
To begin using this project, follow the steps below to configure the sensor simulation and monitoring environment.
## Prerequisites
1. To ensure proper functionality, it is required to use Docker Compose version 2.0 or a more recent version.
2. Add all required credentials in ```.env``` file.

## Installation and Running

Before you start, ensure you have Docker and Docker Compose installed on your system. If not, you can install them by following the official Docker documentation:

- [Docker Installation Guide](https://docs.docker.com/get-docker/)
- [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Aritra0124/TODO_APP
cd your-repo
```

### Step 2: Setup .env file

```text
MYSQL_ROOT_PASSWORD=your-root-password
MYSQL_DATABASE=your-database-name
MYSQL_USER=your-username
MYSQL_PASSWORD=your-password
MYSQL_HOST= database-name
MYSQL_PORT=3306
```
### Step 3: Build and Run the Services

```bash
docker-compose up --build
```


## Project Structure

```
.gitignore
README.md
Ticket_Project
   |-- Ticket_Project
   |   |-- __init__.py
   |   |-- asgi.py
   |   |-- settings.py
   |   |-- urls.py
   |   |-- wsgi.py
   |-- manage.py
   |-- ticket_app
   |   |-- __init__.py
   |   |-- admin.py
   |   |-- apps.py
   |   |-- migrations
   |   |   |-- 0001_initial.py
   |   |   |-- 0002_alter_location_name.py
   |   |   |-- 0003_ticket_uuid.py
   |   |   |-- __init__.py
   |   |-- models.py
   |   |-- serializers.py
   |   |-- tests.py
   |   |-- urls.py
   |   |-- views.py
docker-compose.yml
docker
   |-- Dockerfile
   |-- entrypoint.sh
   |-- requirements.txt

```

## Docker Compose file Description

### Docker Compose Services

### `django_ticket_project` Service

The `django_ticket_project` service is responsible for running the Django ToDo application. It is configured as follows:

- **Container Name**: `django_ticket_project`
- **Build**: Builds the Docker image using the Dockerfile located in the `docker` directory.
- **Volumes**: Mounts the local `Ticket_Project` directory into the container at `/var/www/html`. This allows real-time code changes without rebuilding the container.
- **Environment Variables**: Reads environment variables from the `.env` file.
- **Working Directory**: Sets the working directory inside the container to `/var/www/html`.
- **Command**: Executes the `/entrypoint.sh` script inside the container.
- **Ports**: Maps port `8900` on the host to port `8000` inside the container.
- **Dependencies**: Depends on the `ticket_db` service.

### `ticket_db` Service

The `ticket_db` service runs a MySQL database for the Django ToDo application. It is configured as follows:

- **Container Name**: `ticket_db`
- **Image**: Uses the official MySQL image (`mysql:8.1`).
- **Restart Policy**: Restarts the container automatically unless stopped.
- **TTY**: Allocates a pseudo-TTY to the container.
- **Environment Variables**:
  - `MYSQL_ROOT_PASSWORD`: Password for the MySQL root user.
  - `MYSQL_DATABASE`: Name of the MySQL database.
  - `MYSQL_USER`: Username for accessing the MySQL database.
  - `MYSQL_PASSWORD`: Password for the MySQL user.
- **Ports**: Maps port `3310` on the host to port `3306` inside the container.
- **Volumes**: Mounts the `./db-data/local` directory into the container at `/var/lib/mysql` for persistent data storage.
- **Health Check**: Checks if the container is healthy by running `exit 0` as the health test.

### Networks

- **`ticket-network`**: Custom bridge network for communication between the `django_ticket_project` and `todo_db` services. Configured with the IP subnet `172.16.250.0/24` for internal container communication.

This configuration allows the Django ToDo application to run in one container and the MySQL database in another, ensuring modularity and separation of concerns.


### To Test the module use following command 
```shell
python manage.py test ticket_app.tests --settings=Ticket_Project.test_settings
```

## API Endpoints 

- **Register**:
    - Endpoint ``POST /api/register/``
    - Body ```{
      "username": "admin",
      "password": "Hello@1234"
    }```
- **Login**:
    - Endpoint ``POST /api/login/``
    - Body ```{
      "username": "admin",
      "password": "Hello@1234"
    }```
    - Response ```{"token": "1ad6b92d2bb866f130e6943ba2ab818ce01be1b8" }```
- **Logout**:
    - Endpoint ``POST /api/logout/``
    - Header ```{ "Authorization" : Token 1ad6b92d2bb866f130e6943ba2ab818ce01be1b8 }```
    - Response ```{"message": "Logout successful" }```
- **Location**:
  - Add new location
    - Endpoint ``POST /api/location/``
    - Header ```{ "Authorization" : Token 1ad6b92d2bb866f130e6943ba2ab818ce01be1b8 }```
    - Body ```{"name": "Pune}```
    - Response ```{
    "id": 11,
    "name": "Chennai"
}```
  - list of locations
    - Endpoint ``GET /api/location/``
    - Header ```{ "Authorization" : Token 1ad6b92d2bb866f130e6943ba2ab818ce01be1b8 }```
    - Response ```[
    {
        "id": 11,
        "name": "Chennai"
    },
    {
        "id": 3,
        "name": "Delhi"
    },
    {
        "id": 1,
        "name": "Kolkata"
    },
    {
        "id": 4,
        "name": "Mumbai"
    },
    {
        "id": 2,
        "name": "Pune"
    }
]```
- **Price**:
  - #### To get all price list
    - Endpoint ```GET /api/pricing/```
    - Header ```{ "Authorization" : Token 1ad6b92d2bb866f130e6943ba2ab818ce01be1b8 }```
    - Response ```[
      {
          "id": 1,
          "source": {
              "id": 1,
              "name": "Kolkata"
          },
          "destination": {
              "id": 2,
              "name": "Pune"
          },
          "pricing": "50.00"
      },
      {
          "id": 3,
          "source": {
              "id": 3,
              "name": "Delhi"
          },
          "destination": {
              "id": 2,
              "name": "Pune"
          },
          "pricing": "80.00"
      },
      {
          "id": 4,
          "source": {
              "id": 2,
              "name": "Pune"
          },
          "destination": {
              "id": 4,
              "name": "Mumbai"
          },
          "pricing": "10.00"
      },
      {
          "id": 5,
          "source": {
              "id": 3,
              "name": "Delhi"
          },
          "destination": {
              "id": 4,
              "name": "Mumbai"
          },
          "pricing": "10.00"
      },
      {
          "id": 6,
          "source": {
              "id": 3,
              "name": "Delhi"
          },
          "destination": {
              "id": 2,
              "name": "Pune"
          },
          "pricing": "10.00"
      }
  ]```
  - #### To add new price  
    - Endpoint ``POST /api/pricing/``
    - Header ```{ "Authorization" : Token 1ad6b92d2bb866f130e6943ba2ab818ce01be1b8 }```
    - Body ```{
    "source": 3,
    "destination": 2,
    "pricing": 10.00
}```
    - Response ```{
    "source": 3,
    "destination": 1,
    "pricing": "10.00"
}```
- **Ticket**:
  - Create New Ticket
    - Endpoint ```POST /api/ticket/```
    - Header ```{ "Authorization" : Token 1ad6b92d2bb866f130e6943ba2ab818ce01be1b8 }```
    - Body ```{
    "source": 3,
    "destination": 2,
    "travel_date": "2023-09-5",
    "passenger_name": "Aritra",
    "seat_number":11
}```
    - Response ```{"source":3,"destination":1,"travel_date":"2023-09-05","passenger_name":"Aritra","seat_number":"20","is_cancelled":false,"pricing":{"id":8,"source":{"id":3,"name":"Delhi"},"destination":{"id":1,"name":"Kolkata"},"pricing":"10.00"}}```
  - Get list of tickets
    - Endpoint ```GET /api/ticket/``` or ```GET /api/tickets/```
    - Header ```{ "Authorization" : Token 1ad6b92d2bb866f130e6943ba2ab818ce01be1b8 }```
    - Response ```[
    {
        "uuid": "376de282-52c1-425e-8b41-a313c46eb3cd",
        "source": {
            "id": 1,
            "name": "Kolkata"
        },
        "destination": {
            "id": 2,
            "name": "Pune"
        },
        "travel_date": "2023-10-05",
        "passenger_name": "Aritra",
        "seat_number": "50",
        "is_cancelled": true,
        "pricing": {
            "id": 1,
            "source": {
                "id": 1,
                "name": "Kolkata"
            },
            "destination": {
                "id": 2,
                "name": "Pune"
            },
            "pricing": "50.00"
        }
    },
    {
        "uuid": "212f1eef-f7c3-4c60-b10a-c485be4b6bdb",
        "source": {
            "id": 3,
            "name": "Delhi"
        },
        "destination": {
            "id": 2,
            "name": "Pune"
        },
        "travel_date": "2023-10-05",
        "passenger_name": "Aritra",
        "seat_number": "50",
        "is_cancelled": false,
        "pricing": {
            "id": 3,
            "source": {
                "id": 3,
                "name": "Delhi"
            },
            "destination": {
                "id": 2,
                "name": "Pune"
            },
            "pricing": "80.00"
        }
    },
    {
        "uuid": "2ce56467-2526-48a8-93e7-1a2376df7e6c",
        "source": {
            "id": 3,
            "name": "Delhi"
        },
        "destination": {
            "id": 4,
            "name": "Mumbai"
        },
        "travel_date": "2023-09-01",
        "passenger_name": "Das",
        "seat_number": "10",
        "is_cancelled": false,
        "pricing": {
            "id": 5,
            "source": {
                "id": 3,
                "name": "Delhi"
            },
            "destination": {
                "id": 4,
                "name": "Mumbai"
            },
            "pricing": "10.00"
        }
    },
    {
        "uuid": "11c26498-611f-4067-b619-714308b4ec8f",
        "source": {
            "id": 3,
            "name": "Delhi"
        },
        "destination": {
            "id": 4,
            "name": "Mumbai"
        },
        "travel_date": "2023-09-01",
        "passenger_name": "Aritra",
        "seat_number": "10",
        "is_cancelled": false,
        "pricing": {
            "id": 5,
            "source": {
                "id": 3,
                "name": "Delhi"
            },
            "destination": {
                "id": 4,
                "name": "Mumbai"
            },
            "pricing": "10.00"
        }
    },
    {
        "uuid": "92896379-9c61-4aa8-959c-dd1b7fc31258",
        "source": {
            "id": 3,
            "name": "Delhi"
        },
        "destination": {
            "id": 4,
            "name": "Mumbai"
        },
        "travel_date": "2023-09-02",
        "passenger_name": "Aritra",
        "seat_number": "10",
        "is_cancelled": false,
        "pricing": {
            "id": 5,
            "source": {
                "id": 3,
                "name": "Delhi"
            },
            "destination": {
                "id": 4,
                "name": "Mumbai"
            },
            "pricing": "10.00"
        }
    },
    {
        "uuid": "d4b4a6ef-5633-4c51-be3e-bb8570337960",
        "source": {
            "id": 3,
            "name": "Delhi"
        },
        "destination": {
            "id": 4,
            "name": "Mumbai"
        },
        "travel_date": "2023-09-05",
        "passenger_name": "Aritra",
        "seat_number": "11",
        "is_cancelled": false,
        "pricing": {
            "id": 5,
            "source": {
                "id": 3,
                "name": "Delhi"
            },
            "destination": {
                "id": 4,
                "name": "Mumbai"
            },
            "pricing": "10.00"
        }
    },
    {
        "uuid": "ff1798e9-bd81-4055-8a12-e50363051f62",
        "source": {
            "id": 3,
            "name": "Delhi"
        },
        "destination": {
            "id": 2,
            "name": "Pune"
        },
        "travel_date": "2023-09-05",
        "passenger_name": "Aritra",
        "seat_number": "11",
        "is_cancelled": false,
        "pricing": {
            "id": 3,
            "source": {
                "id": 3,
                "name": "Delhi"
            },
            "destination": {
                "id": 2,
                "name": "Pune"
            },
            "pricing": "80.00"
        }
    },
    {
        "uuid": "069fd097-bb3b-42b7-bff6-5834ae254d5b",
        "source": {
            "id": 3,
            "name": "Delhi"
        },
        "destination": {
            "id": 1,
            "name": "Kolkata"
        },
        "travel_date": "2023-09-05",
        "passenger_name": "Aritra",
        "seat_number": "20",
        "is_cancelled": false,
        "pricing": {
            "id": 8,
            "source": {
                "id": 3,
                "name": "Delhi"
            },
            "destination": {
                "id": 1,
                "name": "Kolkata"
            },
            "pricing": "10.00"
        }
    }
]```
  - Cancel Ticket
    - Endpoint ``PUT /api/ticket/<id>/``
    - Header ```{ "Authorization" : Token 1ad6b92d2bb866f130e6943ba2ab818ce01be1b8 }```
    - Response ```{
    "uuid": "ff1798e9-bd81-4055-8a12-e50363051f62",
    "source": {
        "id": 3,
        "name": "Delhi"
    },
    "destination": {
        "id": 2,
        "name": "Pune"
    },
    "travel_date": "2023-09-05",
    "passenger_name": "Aritra",
    "seat_number": "11",
    "is_cancelled": true,
    "pricing": {
        "id": 3,
        "source": {
            "id": 3,
            "name": "Delhi"
        },
        "destination": {
            "id": 2,
            "name": "Pune"
        },
        "pricing": "80.00"
    }
}```
  - Filter Tickets
    - Endpoint ```GET /api/tickets/?source_name=NAME``` or ```GET /api/tickets/?destination_name=Delhi``` or ```GET /api/tickets/?passenger_name=NAME```
    - Header ```{ "Authorization" : Token 1ad6b92d2bb866f130e6943ba2ab818ce01be1b8 }```
    - Response ```[
    {
        "uuid": "376de282-52c1-425e-8b41-a313c46eb3cd",
        "source": {
            "id": 1,
            "name": "Kolkata"
        },
        "destination": {
            "id": 2,
            "name": "Pune"
        },
        "travel_date": "2023-10-05",
        "passenger_name": "Aritra",
        "seat_number": "50",
        "is_cancelled": true,
        "pricing": {
            "id": 1,
            "source": {
                "id": 1,
                "name": "Kolkata"
            },
            "destination": {
                "id": 2,
                "name": "Pune"
            },
            "pricing": "50.00"
        }
    },
    {
        "uuid": "212f1eef-f7c3-4c60-b10a-c485be4b6bdb",
        "source": {
            "id": 3,
            "name": "Delhi"
        },
        "destination": {
            "id": 2,
            "name": "Pune"
        },
        "travel_date": "2023-10-05",
        "passenger_name": "Aritra",
        "seat_number": "50",
        "is_cancelled": false,
        "pricing": {
            "id": 3,
            "source": {
                "id": 3,
                "name": "Delhi"
            },
            "destination": {
                "id": 2,
                "name": "Pune"
            },
            "pricing": "80.00"
        }
    },
    {
        "uuid": "11c26498-611f-4067-b619-714308b4ec8f",
        "source": {
            "id": 3,
            "name": "Delhi"
        },
        "destination": {
            "id": 4,
            "name": "Mumbai"
        },
        "travel_date": "2023-09-01",
        "passenger_name": "Aritra",
        "seat_number": "10",
        "is_cancelled": false,
        "pricing": {
            "id": 5,
            "source": {
                "id": 3,
                "name": "Delhi"
            },
            "destination": {
                "id": 4,
                "name": "Mumbai"
            },
            "pricing": "10.00"
        }
    },
    {
        "uuid": "92896379-9c61-4aa8-959c-dd1b7fc31258",
        "source": {
            "id": 3,
            "name": "Delhi"
        },
        "destination": {
            "id": 4,
            "name": "Mumbai"
        },
        "travel_date": "2023-09-02",
        "passenger_name": "Aritra",
        "seat_number": "10",
        "is_cancelled": false,
        "pricing": {
            "id": 5,
            "source": {
                "id": 3,
                "name": "Delhi"
            },
            "destination": {
                "id": 4,
                "name": "Mumbai"
            },
            "pricing": "10.00"
        }
    },
    {
        "uuid": "d4b4a6ef-5633-4c51-be3e-bb8570337960",
        "source": {
            "id": 3,
            "name": "Delhi"
        },
        "destination": {
            "id": 4,
            "name": "Mumbai"
        },
        "travel_date": "2023-09-05",
        "passenger_name": "Aritra",
        "seat_number": "11",
        "is_cancelled": false,
        "pricing": {
            "id": 5,
            "source": {
                "id": 3,
                "name": "Delhi"
            },
            "destination": {
                "id": 4,
                "name": "Mumbai"
            },
            "pricing": "10.00"
        }
    },
    {
        "uuid": "ff1798e9-bd81-4055-8a12-e50363051f62",
        "source": {
            "id": 3,
            "name": "Delhi"
        },
        "destination": {
            "id": 2,
            "name": "Pune"
        },
        "travel_date": "2023-09-05",
        "passenger_name": "Aritra",
        "seat_number": "11",
        "is_cancelled": true,
        "pricing": {
            "id": 3,
            "source": {
                "id": 3,
                "name": "Delhi"
            },
            "destination": {
                "id": 2,
                "name": "Pune"
            },
            "pricing": "80.00"
        }
    },
    {
        "uuid": "069fd097-bb3b-42b7-bff6-5834ae254d5b",
        "source": {
            "id": 3,
            "name": "Delhi"
        },
        "destination": {
            "id": 1,
            "name": "Kolkata"
        },
        "travel_date": "2023-09-05",
        "passenger_name": "Aritra",
        "seat_number": "20",
        "is_cancelled": false,
        "pricing": {
            "id": 8,
            "source": {
                "id": 3,
                "name": "Delhi"
            },
            "destination": {
                "id": 1,
                "name": "Kolkata"
            },
            "pricing": "10.00"
        }
    }
]```
- **Summary**:
  - Endpoint ``GET /api/ticket-summary/?start_date=DATE&end_date=DATE``
  - Header ```{ "Authorization" : Token 1ad6b92d2bb866f130e6943ba2ab818ce01be1b8 }```
  - Response ```{
    "Delhi": {
        "Sep-2023": {
            "ticket_count": 2,
            "total_pricing": 90.0
        },
        "Oct-2023": {
            "ticket_count": 1,
            "total_pricing": 80.0
        }
    },
    "Kolkata": {
        "Oct-2023": {
            "ticket_count": 1,
            "total_pricing": 50.0
        }
    }
}```
- **Traveller**:
  - To add ticket to a user
      - Endpoint ``POST /api/traveller/``
      - Body ``{"ticket": 2 }``
      - Response ```{"message": "Logout successful" }```
  _ To get ticket details of a user
      - Endpoint ``GET /api/traveller/<id>/``
      - Response ```[
    {
        "uuid": "376de282-52c1-425e-8b41-a313c46eb3cd",
        "source": {
            "id": 1,
            "name": "Kolkata"
        },
        "destination": {
            "id": 2,
            "name": "Pune"
        },
        "travel_date": "2023-10-05",
        "passenger_name": "Aritra",
        "seat_number": "50",
        "is_cancelled": true,
        "pricing": {
            "id": 1,
            "source": {
                "id": 1,
                "name": "Kolkata"
            },
            "destination": {
                "id": 2,
                "name": "Pune"
            },
            "pricing": "50.00"
        }
    }
]```