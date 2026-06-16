import json
import os
from typing import Optional
from ai_trip_planner.engine.models import User

class AuthManager:
    def __init__(self, data_file="ai_trip_planner/data/users.json"):
        self.data_file = data_file
        self.users = self._load_users()
        self.current_user: Optional[User] = None

    def _load_users(self):
        if not os.path.exists(self.data_file):
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w') as f:
                json.dump({}, f)
            return {}
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                return {u: User(**v) for u, v in data.items()}
        except:
            return {}

    def _save_users(self):
        data = {u: vars(v) for u, v in self.users.items()}
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)

    def signup(self, username, password, email):
        if username in self.users:
            return False, "Username already exists"
        self.users[username] = User(username=username, password=password, email=email)
        self._save_users()
        return True, "Signup successful"

    def login(self, username, password):
        if username in self.users and self.users[username].password == password:
            self.current_user = self.users[username]
            return True, "Login successful"
        return False, "Invalid username or password"

    def logout(self):
        self.current_user = None

    def save_trip(self, trip_data):
        if self.current_user:
            self.current_user.saved_trips.append(trip_data)
            self._save_users()
            return True
        return False
