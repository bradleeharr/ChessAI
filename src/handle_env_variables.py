from dotenv import find_dotenv, set_key, dotenv_values


class UserVars():
    def __init__(self):
        config = dotenv_values(find_dotenv())
        self.username = config["USERNAME"]

    def save(self):
        set_key(find_dotenv(), "USERNAME", self.username)