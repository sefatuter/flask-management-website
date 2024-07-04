# Registration System

## Home

![home](https://github.com/sefatuter/flask-management-website/assets/95074982/f5584d41-97b1-4b21-a5b4-fc793e51228b)

## Login

![login](https://github.com/sefatuter/flask-management-website/assets/95074982/624a3cdd-d4d9-49e6-a8f8-1c6bbead8c99)

## Register

![register](https://github.com/sefatuter/flask-management-website/assets/95074982/4303ecab-f026-40dd-9622-e713c1de3c5a)

## Main

![main](https://github.com/sefatuter/flask-management-website/assets/95074982/4df7f302-c3e6-44bc-8edb-332f13434829)

## Admin Panel

![admin panel](https://github.com/sefatuter/flask-management-website/assets/95074982/eac74efb-4861-4bdb-92de-baaab3a3690e)

## List

![list](https://github.com/sefatuter/flask-management-website/assets/95074982/4e0299d5-dff8-4692-9a33-6dc7c837bbbc)

## Add User

![add_user](https://github.com/sefatuter/flask-management-website/assets/95074982/3fc1cdb9-6197-469f-8463-c3d2ab86c2f5)

## Dashboard

![dashboard](https://github.com/sefatuter/flask-management-website/assets/95074982/8dcfe4d9-3454-40f3-98c9-40ddf5256982)

## Dashboard Edit

![dashboard_update](https://github.com/sefatuter/flask-management-website/assets/95074982/cdd929af-5af3-40e8-b4ec-6ace6c1bb4cd)

## User Update

![user_update](https://github.com/sefatuter/flask-management-website/assets/95074982/5e6fd224-9183-406f-95be-4b283c282f8f)


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

