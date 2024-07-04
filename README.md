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

## Base URL:  ```http://localhost:5000/api```


* Method: GET

    1. Retrieve All Users

    Endpoint : ```GET /users```

    GET http://localhost:5000/api/users

    Response:
        * Status: '200 OK'
        * Body:
        
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

    2. Create a New User

    Endpoint : ```POST /users```