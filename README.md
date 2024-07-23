# Flask Registration System

Web application designed to manage and streamline organizational tasks with a robust interface. Technologies Used: Python, Flask, HTML,
CSS, JavaScript, SQLAlchemy, Jinja2

● Implements a secure login system to ensure user data privacy and protection against unauthorized access. Registration and login security
is ensured by using Google OAuth system

● Features an admin panel that allows for efficient oversight and administration of user roles and permissions.

## Installation

1. Clone the repository:
    bash
```
git clone https://github.com/sefatuter/flask-management-website.git
```

2. Navigate to the project directory, create virtual environment and activate:
```
cd flask-management-website
python -m venv venv
```

3. Install the required packages, run setup script:
     bash
```
pip install -r requirements.txt
```

4. Run App
```
flask run
```

5. Go to ```http://localhost:5000```


## Docker container

``` docker pull usersefa/flask-management-system ```
``` docker build -t myflaskapp . ```
``` docker run -d -p 5000:5000 myflaskapp ```

## Home

![1](https://github.com/user-attachments/assets/cce061eb-a31c-47f9-8f79-9ac3c8f35208)

## Login

![2](https://github.com/user-attachments/assets/6ec1a086-159a-45e9-ac0c-fa1e8dbde3a7)

## Register

![3](https://github.com/user-attachments/assets/dc6c3618-7f50-4a50-bd4a-478cdb0342d5)

## Main

![4](https://github.com/user-attachments/assets/16703a94-d97d-4fc6-adff-f4d47da67cef)

## Admin Panel

![5](https://github.com/user-attachments/assets/d31bf050-7388-4442-be43-9214369c9ee9)

## Add User

![6](https://github.com/user-attachments/assets/9dd5bdb9-d07f-4bc8-9635-8e387d6591e9)

![7](https://github.com/user-attachments/assets/a1a90194-8e3f-4d32-baba-a8634338e9c1)

![8](https://github.com/user-attachments/assets/d277e9b5-0436-435f-bcbf-9b8900768102)

## Dashboard

![9](https://github.com/user-attachments/assets/283f0fe8-35e5-4fc0-a945-7680a6761b45)

# API Documentation:

### Base URL:  ```http://localhost:5000/api```


* For Users:

    **1. Retrieve All Users**

    Endpoint : ```GET /users```

    ```
    GET http://localhost:5000/api/users
    ```

    Response:
    - Status: '200 OK'
    - Body:
        
        ```
        [
            {
                "id": 1,
                "username": "user",
                "email": "user@test.com",
                "date_added": "2023-01-01 12:00:00"
            },
            ...
        ]
        ```


    **2. Create a New User**

    Endpoint : ```POST /users```

    ```
    POST http://localhost:5000/api/users
    ```

    Request:
    - Body:
        
        ```
        {
            "username": "new_user",
            "email": "new_user@test.com",
            "password": "password123"
        }
        ```
    
    Response:
    - Status: 201 Created
    - Body:

        ```
        {
            "message": "User created successfully"
        }
        ```


    **3. Retrieve a Specific User by ID**

    Endpoint : ```GET /users/<int:user_id>```

    ```
    GET http://localhost:5000/api/users/<int:user_id>
    ```

    Response:
    - Status: '200 OK'
    - Body:
        
        ```
        [
            {
                "id": 1,
                "username": "user",
                "email": "user@test.com",
                "date_added": "2023-01-01 12:00:00"
            }
        ]
        ```
    - Status: '404 Not Found'
    - Body:

        ```
        {
            "message": "User not found"
        }
        ```


    **4. Update a Specific User by ID**

    Endpoint : ```PUT /users/<int:user_id>```

    ```
    PUT http://localhost:5000/api/users/<int:user_id>
    ```

    Request:
    - Body:
        
        ```
        {
            "username": "updated_user",
            "email": "updated_user@example.com",
            "password": "new_password123"
        }
        ```
    
    Response:
    - Status: '200 OK'
    - Body:

        ```
        {
            "message": "User updated successfully"
        }
        ```
    - Status: '404 Not Found'
    - Body:
        ```
        {
            "message": "User not found"
        }
        ```


    **5. Delete a Specific User by ID**

    Endpoint : ```DELETE /users/<int:user_id>```

    ```
    DELETE http://localhost:5000/api/users/<int:user_id>
    ```

    Response:
    - Status: '200 OK'
    - Body:
        
        ```
        {
            "message": "User deleted successfully"
        }
        ```
    - Status: '404 Not Found'
    - Body:

        ```
        {
            "message": "User not found"
        }
        ```


* For Participants:

    **1. Retrieve All Participants**

    Endpoint : ```GET /participants```

    ```
    GET http://localhost:5000/api/participants
    ```

    Response:
    - Status: '200 OK'
    - Body:
        
        ```
        [
            {
                "id": 1,
                "name": "John",
                "surname": "Doe",
                "email": "john.doe@example.com",
                "phone": "123-456-7890",
                "school_id": 1,
                "department_id": 1
            },
            ...
        ]
        ```


    **2. Create a New Participant**

    Endpoint : ```POST /participants```

    ```
    POST http://localhost:5000/api/participants
    ```

    Request:
    - Body:
        
        ```
        {
            "name": "Jane",
            "surname": "Doe",
            "email": "jane.doe@example.com",
            "phone": "987-654-3210",
            "school_id": 2,
            "department_id": 3
        }
        ```
    
    Response:
    - Status: 201 Created
    - Body:

        ```
        {
            "message": "Participant created successfully"
        }
        ```


    **3. Retrieve a Specific Participant by ID**

    Endpoint : ```GET /participant/<int:participant_id>```

    ```
    GET http://localhost:5000/api/participant/<int:participant_id>
    ```

    Response:
    - Status: '200 OK'
    - Body:
        
        ```
        {
            "id": 1,
            "name": "John",
            "surname": "Doe",
            "email": "john.doe@example.com",
            "phone": "123-456-7890",
            "school_id": 1,
            "department_id": 1
        }
        ```
    - Status: '404 Not Found'
    - Body:

        ```
        {
            "message": "Participant not found"
        }
        ```


    **4. Update a Specific Participant by ID**

    Endpoint : ```PUT /participant/<int:participant_id>```

    ```
    PUT http://localhost:5000/api/participant/<int:participant_id>
    ```

    Request:
    - Body:
        
        ```
        {
            "name": "Updated Name",
            "surname": "Updated Surname",
            "email": "updated.email@example.com",
            "phone": "123-456-7890",
            "school_id": 1,
            "department_id": 2
        }
        ```
    
    Response:
    - Status: '200 OK'
    - Body:

        ```
        {
            "message": "Participant updated successfully"
        }
        ```
    - Status: '404 Not Found'
    - Body:
        ```
        {
            "message": "Participant not found"
        }
        ```


    **5. Delete a Specific Participant by ID**

    Endpoint : ```DELETE /participant/<int:participant_id>```

    ```
    DELETE http://localhost:5000/api/participant/<int:participant_id>
    ```

    Response:
    - Status: '200 OK'
    - Body:
        
        ```
        {
            "message": "Participant deleted successfully"
        }
        ```
    - Status: '404 Not Found'
    - Body:

        ```
        {
            "message": "Participant not found"
        }
        ```

