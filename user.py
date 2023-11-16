import json

class User:
    def __init__(self, user_id):
        self.user_id = str(user_id)
        self.data = self.load_data()

    def load_data(self):
        try:
            with open("user_records.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_data(self):
        with open("user_records.json", "w") as file:
            json.dump(self.data, file)

    def is_existing_user(self):
        return self.user_id in self.data

    def get_records(self):
        return self.data.get(self.user_id, {})

    def set_records(self, squat, bench, deadlift):
        self.data[self.user_id] = {
            "Squat": squat,
            "Bench": bench,
            "Deadlift": deadlift
        }
        self.save_data()
