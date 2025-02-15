# Django Project Setup Guide

## Overview

This project is a Django-based web application.

Follow the steps below to clone the repository and set up the project on your local machine.

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python (version 3.10 or higher)
- Docker and Docker Compose (if using Docker setup)
- Git

---

## Installation Instructions

### 1. Clone the Repository

To get started, clone the repository using Git:

```bash
git clone https://github.com/mallick-portfolio/foringBoard.git
cd foringBoard
```

## 2. Run Project

### 2.1. Using Docker Setup

If you are using Docker, navigate to the project directory and run the following commands to start the containers

```bash
docker-compose up --build
```
If the given command is not working with your system, try the following command:
```bash
docker compose up --build
```

### 2.2. Without Docker Setup

If you are not using Docker, navigate to the project directory and run the following commands to install the dependencies and start the development server

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## API documentation

- [API Documentation](https://documenter.getpostman.com/view/20671684/2sAYXEDHwB)
