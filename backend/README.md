1. Run web backend.

    Move to horse_racing_backend folder
    
    ```
        cd horse_racing_backend
    ```

    1) Configuration
        - config/credentials.json file configuration.

        You should enter the values for username, password and app_key in betfair.com site account.

        Reference to https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Application+Keys for getting app_key.
        
        ```
            {
                "username": "your_username",
                "password": "your_password",
                "app_key": "your_app_key",
                "certs_path": "./certs"
            }
        ```

        You can store the certification info (*.pem file) in ./certs folder.

        Reference to https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Non-Interactive+%28bot%29+login for getting certification
        informations.

        - mysql database configuration (config/db.json file)

            You should enter the values as follows in config/db.json file.

            ```
            {
                "username": "db_user",
                "password": "db_password",
                "dbname": "db_name",
                "host": "db_host"
            }
            ```

    2) Run backend process

        You can run these command in terminal
        
        ```
        pip install -r requirements.req

        python server.py
        ```