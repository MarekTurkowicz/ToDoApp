from repositories.user_repository import UserRepository

class UserController:
    def __init__(self):
        self.user_repository = UserRepository()

    def create_user(self, user, password, email):
        return self.user_repository.add_user(user, password, email)

    def find_user_by_id(self, user_id):
        return self.user_repository.get_user_by_id(user_id)

    def find_user_by_email(self, email):
        return self.user_repository.get_user_by_email(email)

    def delete_user(self, user_id):
        return self.user_repository.delete_user(user_id)

    def close(self):
        return self.user_repository.close()
