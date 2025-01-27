

class UserController:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def get_id_by_username(self, username):
        return self.user_repository.get_id_by_username(username)

    def create_user(self, user, password, email):
        return self.user_repository.add_user(user, password, email)

    def find_user_by_id(self, user_id):
        return self.user_repository.get_user_by_id(user_id)

    def find_user_by_email(self, email):
        return self.user_repository.get_user_by_email(email)

    def get_user_by_username_and_password(self,username,password):
        if self.user_repository.get_user_by_username_and_password(username,password):
            return self.user_repository.get_user_by_username_and_password(username,password)

    def delete_user(self, user_id):
        return self.user_repository.delete_user(user_id)

    def close(self):
        return self.user_repository.close()
