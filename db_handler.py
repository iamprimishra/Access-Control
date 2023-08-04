import json


class DB_Handler:

    def __init__(self):
        pass

    def get_logs(self):
        with open("log.txt", "r") as f:
            return f.read()

    def get_last_access_time(self, key):
        with open("log.txt", "r") as f:
            data = f.read().split("\n")[::-1]
            # print(data)
            for line in data:
                # print(key,line)
                if key in line.strip():
                    # print(line.strip().split(" ")[:2])
                    return " ".join(line.strip().split(" ")[:2])

    def is_key_valid(self, key):
        with open("data.json", 'r') as f:
            access_keys = json.load(f)
            access_keys = access_keys["data"]["access-keys"]
            return key in access_keys

    def get_data(self):
        with open("data.json", 'r') as f:
            return json.load(f)

    def add_data(self, data):
        with open("data.json", "w") as f:
            f.write(json.dumps(data, sort_keys=True, indent=4))

    def get_access_keys(self):
        with open("data.json", 'r') as f:
            res = json.dumps(f.read())
            return res

    def add_access_key_and_name(self, name, key):
        data = self.get_data()
        key = key.strip()
        data["data"]["access-keys"].append(key)
        data["data"]["name"][key] = name.strip()
        print(data)
        self.add_data(data)

    def get_mode(self):
        with open("mode.txt", "r") as f:
            return f.read().strip()

    def change_name(self, name, key):
        data = self.get_data()
        data["data"]["name"][key] = name.strip()
        print(data)
        self.add_data(data)

    def delete_data(self, key):
        data = self.get_data()
        data["data"]["access-keys"].remove(key)
        data["data"]["name"].pop(key)
        self.add_data(data)
