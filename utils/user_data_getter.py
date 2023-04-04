import requests


class UserData:
    
    def __init__(self, link='http://localhost:8000') -> None:
        self.__api_link = link
        
    
    def get_email_creds_by_token(self, email, token)-> dict | bool:
        req = requests.get(f'{self.__api_link}/api/v1/emaillist/',
                           headers={'Authorization': f'Token {token}'},
                           params={"email": email})
        if not req.ok:
            return False
        
        return req.json()
