from uuid import uuid1
from datetime import date

class InvalidUserDataError(Exception):
    pass
class User:

    def __init__(self,
                 username: str = None,
                 phone: str = None,
                 mail: str = None):
        self.id = str(uuid1())
        self.date_create = date.today()
        self.username = username
        self.phone = phone
        self.mail = mail
        if username and len(username) < 3:
            raise InvalidUserDataError(f"Имя пользователя '{username}' слишком короткое (минимум 3 символа)")

        if mail and "@" not in mail:
            raise InvalidUserDataError(f"Email '{mail}' должен содержать @")

    def update(self,
               username: str = None,
               phone: str = None,
               mail: str = None
               ) -> bool:
        try:
            updated = False

            if username is not None:

                self.username = username
                updated = True

            if phone is not None:
                self.phone = phone
                updated = True

            if mail is not None:
                self.mail = mail
                updated = True

            return updated

        except Exception:
            return False

