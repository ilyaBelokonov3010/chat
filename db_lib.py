import pickle, json, secrets, time
from flask import render_template
class Session:
    def __init__(self, id, user):
        self.id = id
        self.user = user # user object
        self.date_regestration = time.time()

class User:
    def __init__(self, id, name, password, sessions:list[Session]):
        self.id = id
        self.name = name
        self.password = password
        self.sessions = sessions
        self.messages = []

class db:
    def __init__(self):
        try: # sessions
            with open("db_sessions.pkl", "rb") as file: # read binary
                self.sessions: dict[str, Session] = pickle.load(file) # dict[token_hex(32), Session]
        except (EOFError, FileNotFoundError):
            with open("db_sessions.pkl", "rb") as file: # read binary
                self.sessions: dict[str, Session] = {} # dict[token_hex(32), Session]
        try: # users
            with open("db_users.pkl", "rb") as file: # read binary
                self.users: list[User] = pickle.load(file)
        except (EOFError, FileNotFoundError):
            with open("db_users.pkl", "rb") as file: # read binary
                self.users: list[User] = []
        try: # messages
            with open("db_sessions.pkl", "rb") as file: # read binary
                self.messages: dict[int, tuple[str, int, float]] = pickle.load(file) # dict[id, tuple[message, user id, unix time]]
        except (EOFError, FileNotFoundError):
            with open("db_sessions.pkl", "rb") as file: # read binary
                self.messages: dict[int, tuple[str, int, float]] = {} # dict[id, tuple[message, user id, unix time]]

    def save(self):
        print('Saving db...')
        with open("db_sessions.pkl", "wb") as file: # write binary
            pickle.dump(self.sessions, file) 
        with open("db_users.pkl", "wb") as file: # write binary
            pickle.dump(self.users, file)
        with open("db_messages.pkl", "wb") as file: # write binary
            pickle.dump(self.messages, file)

    def login(self, username, password):
        for user in self.Users:
            if (user.name == username) and (user.password == password):
                new_session = Session(secrets.token_hex(32), user)
                self.sessions[len(self.sessions)] = new_session
                user.sessions.append(new_session)
                return new_session.id
        return None
    
    def get_session(self, token):
        session = self.sessions.get(token)
        if session:
            return session
        return None

    def render_messages(self):
        temp_render = ''
        for message in self.messages:
            temp_render += render_template('message.html', name = message[1][1], message = message[1][1])