from backend.services.user_service import UserService
from backend.core.security import get_pass_hash, verify_pass, DUMMY_HASH, create_access_token
from backend.schemas.user import Token
from backend.utils.validators import NotFound, validate_pass, InvalidCredentialsError

class AuthService:
    def __init__(self, user_serv: UserService):
        self.user_serv = user_serv

    async def register_user(self, 
            login: str, 
            email: str,
            password: str
        ) -> Token:
        validate_pass(password)

        validated_email = await self.user_serv.validate_new_user(login, email)

        hash_pass = get_pass_hash(password)
        user = await self.user_serv.create_user(login, hash_pass, validated_email)

        access_token = create_access_token(user_data={"sub": user.login})
        return Token(access_token=access_token, token_type="bearer")
        
         
    async def login_user(self, login_or_email: str, password: str) -> dict:
        try:
            if "@" in login_or_email and "." in login_or_email:
                user = await self.user_serv.get_user_by_email(login_or_email)
            else:
                user = await self.user_serv.get_user_by_login(login_or_email)

        except NotFound as e:
            verify_pass(password, DUMMY_HASH)
            raise InvalidCredentialsError()
        
        if not verify_pass(password, user.hash_pass):
            raise InvalidCredentialsError()
        
        access_token = create_access_token(user_data={"sub": user.login})
        return Token(access_token=access_token, token_type="bearer")
    


            
