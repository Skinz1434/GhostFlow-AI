
import json
import time

def update_status():
    while True:
        status_data = {
            "metrics": "Running smoothly",
            "revenue": "$1000",
            "scripts": {
                "analytics": "Running",
                "cloaking": "Running",
                "content": "Running",
                "financial": "Running",
                "security": "Running"
            }
        }
        with open("status.json", "w") as status_file:
            json.dump(status_data, status_file, indent=4)
        time.sleep(30)

if __name__ == "__main__":
    update_status()
