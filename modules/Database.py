import json
import datetime


class Database:
    def __init__(self, path):
        self.path = path
        with open(self.path, encoding="utf-8") as f:
            self.data = json.loads(f.read())

    def add(self, win: str, lose: str, time=str(datetime.datetime.now())):
        self.data.append([win, lose, time])
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f)

    def remove(self, win: str, lose: str):
        for i in range(len(self.data) - 1, -1, -1):
            if self.data[i][0] == win and self.data[i][1] == lose:
                del self.data[i]
                break
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f)
