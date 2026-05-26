# Travel Planner API

A RESTful CRUD API built with **FastAPI** and **SQLAlchemy** that helps travelers plan their trips, collect interesting artworks/places to visit from the Art Institute of Chicago API, and manage their travel notes.

##  Features

* **Travel Projects CRUD**: Create, read, update, and delete travel projects.
* **Places Management**: Add places to projects with strict validations.
* **Third-party Integration**: Validates and fetches place data using the [Art Institute of Chicago API](https://api.artic.edu/docs/#collections).
* **Business Logic & Validations**:
    * Max 10 places per project.
    * Prevents adding duplicate places to the same project.
    * Blocks project deletion if any place within it has already been visited.
    * Automatically marks a project as `completed` when all its places are marked as `visited`.
* **Bonus Features Implemented**:
    * Fully Dockerized (`Dockerfile` + `docker-compose.yml`).
    * Caching for third-party API responses to minimize network overhead.
    * OpenAPI/Swagger documentation auto-generated.

---

## 🛠️ Tech Stack

* **Framework**: FastAPI
* **ORM**: SQLAlchemy
* **Database**: psql
* **Containerization**: Docker & Docker Compose
* **Validation**: Pydantic v2

---

## Prerequisites

Before running the project, ensure you have the following installed:
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

---

## Getting Started & Deployment

### 1. Clone the repository

```bash
git clone https://github.com/Killingrace/developers_today.git
cd developers_today
docker compose up
```
