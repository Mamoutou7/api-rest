# Python REST APIs with Flask, MongoDB, and Docker

This repository contains a collection of small REST API demos built with **Flask**, **Flask-RESTful**, **MongoDB**, and **Docker Compose**.

## Projects

- **Restful API-Docker-MongoDB**: basic REST API examples, including arithmetic endpoints and a simple token-based sentence storage API.
- **Restful API-TextSimilarity**: compares two texts with spaCy and stores user/token data in MongoDB.
- **ImageClassification**: image classification API with token-based access and a TensorFlow image classifier script.
- **BankTransactionsAPI**: simple banking-style API for registration, balance checks, transfers, and loans.

## Tech Stack

- Python 3
- Flask / Flask-RESTful
- MongoDB
- Docker / Docker Compose
- spaCy (text similarity)
- TensorFlow script (image classification)

## Run a Project

Each subproject has its own `docker-compose.yml`.

```bash
cd Restful\ API-TextSimilarity
docker-compose up --build
```

Then open the API on:

```text
http://localhost:5000
```

You can do the same for:

- `BankTransactionsAPI`
- `ImageClassification`
- `Restful API-Docker-MongoDB`
- `Restful API-TextSimilarity`

## Notes

- This repository is a learning/demo project with multiple independent examples.
- Some apps contain unfinished logic, hardcoded values, or older Docker patterns, so a few fixes may be needed before production use.
- The included Dockerfiles use local absolute `WORKDIR` paths, which may need cleanup depending on your environment.

## License

No license file is included in the repository.
