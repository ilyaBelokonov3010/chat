import pickle, json, secrets
from datetime import datetime, timezone

def login_session():
    pass

class Session:
    def __init__(self, id, user):
        self.id = id
        self.user = user
        self.date_regestration = datetime.now(timezone.utc)

class User:
    def __init__(self, id, name, password, sessions:list[Session]):
        self.id = id
        self.name = name
        self.password = password
        self.sessions = sessions

class db:
    def __init__(self):
        try:
            with open("db_sessions.pkl", "rb") as file: # read binary
                self.sessions: dict[str, Session] = pickle.load(file)
        except (EOFError, FileNotFoundError):
            with open("db_sessions.pkl", "rb") as file: # read binary
                self.sessions: dict[str, Session] = {}
        try:
            with open("db_users.pkl", "rb") as file: # read binary
                self.users: list[User] = pickle.load(file)
        except (EOFError, FileNotFoundError):
            with open("db_users.pkl", "rb") as file: # read binary
                self.users: list[User] = []

    def save(self):
        with open("db_sessions.pkl", "wb") as file: # write binary
            pickle.dump(self.sessions, file) 

    def login(self, username, password):
        for user in self.Users:
            if (user.name == username) and (user.password == password):
                new_session = Session(secrets.token_hex(32), user)
                self.sessions[len(self.sessions)] = new_session
                user.sessions.append(new_session)
                return new_session.id
        return None
    
    def render_messages(self):
        