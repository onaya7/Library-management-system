# Project Name: Library Management System

## Overview

This Flask-based Library Management System is designed to help users manage books, borrowers, and other related tasks. The system provides a user-friendly interface for library administrators to perform common operations efficiently.

## Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Features](#features)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites

Make sure you have the following installed:

- [Python](https://www.python.org/downloads/)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) (Optional but recommended)

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/onaya7/Library-management-system.git
```

2. **Navigate to the project directory:**

```bash
cd library-management-system
```

3. **Create a virtual environment (recommended):**

```bash
virtualenv venv
```

4. **Activate the virtual environment:**

# On Windows, use 
    ```bash
      venv\Scripts\activate
    ```
# On macOS and Linux, use
    ```bash
      source venv/bin/activate
    ```
5. Install the required dependencies:

```bash
pip install -r requirements.txt
```
### Configuration

1. **Create a .flaskenv file in the project root and configure the following:**

```bash
FLASK_APP=wsgi.py
FLASK_ENV=development
FLASK_DEBUG=TRUE
FLASK_RUN_PORT=8080
```

2. **Create a .env file in the project root and configure the following:**

```bash
SECRET_KEY=your_secret_key
DATABASE_URI=your_database_uri
```

3. **Initialize the database:**

```bash
flask db init
flask db migrate
flask db upgrade
```

### Usage

1. **Start the Flask development server:**

```bash
flask run
```
Open your web browser and navigate to http://localhost:8000 to access the project.

### Screenshots

``
### Layered Architecture Diagram for The Library Management System
![web-infrastructure-design drawio](https://github.com/onaya7/Library-management-system/assets/63925047/aa1eba2c-90fb-4d8e-81ac-106cbc01197f)

### Use case Diagram for The Library Management System
![Use-case-diagram-lms drawio](https://github.com/onaya7/Library-management-system/assets/63925047/eba812a1-513c-4886-b5b6-ffc1409c467a)

### Entity Relationship(ER)  Diagram for The Library Management System
![library management system er diagram (500lv project work) drawio](https://github.com/onaya7/Library-management-system/assets/63925047/cdeccbf1-44a8-4672-8743-67d5ffca5076)

![Screenshot (195)](https://github.com/onaya7/Library-management-system/assets/63925047/7092a484-d0e6-48ec-9b76-0c26612a36fa)

![Screenshot (196)](https://github.com/onaya7/Library-management-system/assets/63925047/9f82ac9c-df51-4aaf-97c9-a61bb0094195)

![Screenshot (197)](https://github.com/onaya7/Library-management-system/assets/63925047/a21d1513-4d05-4534-9ef4-b48406a5bc2a)

![Screenshot (199)](https://github.com/onaya7/Library-management-system/assets/63925047/e9e49734-3c00-4eea-83b8-3967274f48b1)

![Screenshot (203)](https://github.com/onaya7/Library-management-system/assets/63925047/eb3c8ba5-2307-4af3-9f83-7e9eea74cfff)

![Screenshot (207)](https://github.com/onaya7/Library-management-system/assets/63925047/b9dd0988-c56f-46ad-86a0-9673bedb3614)

![Screenshot (209)](https://github.com/onaya7/Library-management-system/assets/63925047/373e8f43-da0f-43ff-85dc-94cac7cf029b)

![Screenshot (210)](https://github.com/onaya7/Library-management-system/assets/63925047/01fd6b40-5188-4ddb-8063-c1b090d7b53e)

![Screenshot (215)](https://github.com/onaya7/Library-management-system/assets/63925047/0c007286-7843-4ff9-a219-5031ea3ba2e2)

![Screenshot (213)](https://github.com/onaya7/Library-management-system/assets/63925047/7a68ea90-827d-4eb8-aca7-76b637ff7d49)

### Library card generated for the users by the librarian on the Library Management System
![17_EEN_033_library_card (1)](https://github.com/onaya7/Library-management-system/assets/63925047/d2674533-3bc9-49f6-ae8e-e504f1853382)


## Contributing

We welcome contributions to CoinControl project! if you'd like to contribute, please follow these steps:

1.  Fork the repository on Github.

2.  Create a new branch for your feature or bug fix:

```bash
git checkout -b feature/your-feature-name
```

3.  Make your modifications and commit your changes:

```bash
git commit -m "Add your meaningful commit message"
```

4.  Push your changes to your forked repository:

```bash
git push origin feature/your-feature-name
```

5.  Submit a pull request to the master branch of the original repository.

Please ensure your code adheres to the project's coding conventions and includes appropriate tests.

## License

CoinControl is released under the MIT License, which allows you to use, modify, and distribute the code freely. See the LICENSE file for more details.
[MIT LICENSE](https://github.com/onaya7/Library-management-system/blob/master/LICENSE.md).