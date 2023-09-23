import betfairlightweight
import json
    
class Controller:
    def __init__(self):
        try:
            with open('config/credentials.json') as f:
                cred = json.load(f)
                my_username = cred['username']
                my_password = cred['password']
                my_app_key = cred['app_key']
                certs_path = cred['certs_path']
        except Exception as e:
            print(f"config/credentials.json file read failed. {str(e)}")
            return

        self.trading = betfairlightweight.APIClient(username=my_username,
                                            password=my_password,
                                            app_key=my_app_key,
                                            certs=certs_path)
        self.login()

    def login(self):
        try:
            self.trading.login()
            print("===   Login successful.   ===")
        except Exception as e:
            print(f"Login failed: {str(e)}")