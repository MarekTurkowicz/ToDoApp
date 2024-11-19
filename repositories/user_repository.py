from database.database import SessionLocal
from models.user_model import User

class UserRepository:
    def __init__(self):
        self.session = SessionLocal()

    def add_user(self, username: str, password: str, email: str) -> User:
        new_user = User(username=username, password=password, email=email)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user

    def get_user_by_id(self, user_id: int) -> User:
        return self.session.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> User:
        return self.session.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> User:
        return self.session.query(User).filter(User.email == email).first()

    def get_user_by_username_and_password(self, username: str, password: str) -> User:
        return self.session.query(User).filter(
            (User.username == username) & (User.password == password)
        ).first()

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False

    def close(self):
        self.session.close()