import bcrypt
from sqlalchemy.exc import SQLAlchemyError

from models import User

class LoginManager:
    def __init__(self, session):
        self.session = session

    @staticmethod
    def verifyUsername(username):
        return isinstance(username, str) and 6 <= len(username) <= 12

    @staticmethod
    def verifyPassword(password):
        return isinstance(password, str) and password.isdigit() and 4 <= len(password) <= 6

    def _save(self):
        try:
            self.session.commit()
            return True
        except SQLAlchemyError:
            self.session.rollback()
            return False

    def _find_user(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def create_user(self, username, password, role):
        if not (self.verifyUsername(username) and self.verifyPassword(password)):
            return False
        if not isinstance(role, str) or len(role) == 0:
            return False
        if self._find_user(username) is not None:
            return False
        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = User(username=username, password_hash=password_hash, role=role)
        self.session.add(user)
        return self._save()

    def authenticate_user(self, username, password):
        if not (self.verifyUsername(username) and self.verifyPassword(password)):
            return None
        user = self._find_user(username)
        if user is None:
            return None
        if bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            return user
        return None