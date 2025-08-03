from src.controllers.controller import Controller
from src.util.dao import DAO

import re
emailValidator = re.compile(r'.*@.*')

# Mer strikt email validator som kräver korrekt email-format
emailValidator = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

class UserController(Controller):
    def __init__(self, dao: DAO):
        super().__init__(dao=dao)

    
    def get_user_by_email(self, email: str):
        """Given a valid email address of an existing account, return the user object contained in the database associated 
        to that user. For now, do not assume that the email attribute is unique. Additionally print a warning message containing the email
        address if the search returns multiple users.
        
        parameters:
            email -- an email address string 
        returns:
            user -- the user object associated to that email address (if multiple users are associated to that email: return the first one)
            None -- if no user is associated to that email address
        raises:
            ValueError -- in case the email parameter is not valid (i.e., conforming <local-part>@<domain>.<host>)
            Exception -- in case any database operation fails
        """

        # Kolla om email är tom sträng
        if not email or email.strip() == "":
            raise ValueError('Error: invalid email address')

        # Validera email format
        if not re.fullmatch(emailValidator, email):
            raise ValueError('Error: invalid email address')

        try:
            users = self.dao.find({'email': email})

            # Om inga användare hittas, returnera None
            if len(users) == 0:
                return None
            # Om exakt en användare hittas, returnera den
            elif len(users) == 1:
                return users[0]
            # Om flera användare hittas, printa varning och returnera första
            else:
                print(f'Error: more than one user found with mail {email}')
                print(f'Warning: multiple users found with email {email}')
                return users[0]

        except Exception as e:
            # Låt undantaget propagera uppåt
            raise

    
    def update(self, id, data):
        try:
            update_result = super().update(id=id, data={'$set': data})
            return update_result
        except Exception as e:
            raise
