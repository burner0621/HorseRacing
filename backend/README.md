1. Configuration

    Move to horse_racing_backend folder
    
    ```
        cd horse_racing_backend
    ```

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

    Reference to https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Non-Interactive+%28bot%29+login for getting certification informations.
    - mongodb database configuration (config/db.json file)

        You should enter the values as follows in config/db.json file.

        ```
        {
            "host": "localhost",
            "dbname": "horse-racing-betfair",
            "username": "root",
            "password": "",
            "port": 27017
        }
        ```

    - logging

        You should run these commands as follows.

        ```
        mkdir logs
        
        touch flog
        ```
    
    - server configuration
        
        You should configure the config/main.json file.

        ```
        {
            "host": "0.0.0.0",
            "port": 5555
        }
        ```

        ```
        host: address of machine that runs backcend. If you don't specify this option, the default value is "0.0.0.0".

        port: server's port. If you don't specify this option, the default value is 5555.


2. Run backend process

    You can run these command in terminal
    
    ```
    pip install -r requirements.req

    python server.py
    ```