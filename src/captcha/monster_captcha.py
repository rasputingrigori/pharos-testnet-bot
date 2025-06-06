import time, requests

from config.config import settings

async def solve_monster_captcha(params):
    retries = 5
    try:
        task_response = requests.post(
            "https://api.capmonster.cloud/createTask",
            json={
                "clientKey": settings["API_KEY_CAPMONSTER"],
                "task": {
                    "type": "TurnstileTaskProxyless",
                    "websiteURL": params["websiteURL"],
                    "websiteKey": params["websiteKey"],
                },
            },
            headers={"Content-Type": "application/json"},
        )

        request_id = task_response.json().get("taskId")
        if not request_id:
            raise Exception("Failed to create CAPTCHA task. No task ID returned.")

        result = None
        while retries > 0:
            time.sleep(10)
            result_response = requests.post(
                "https://api.capmonster.cloud/getTaskResult",
                json={
                    "clientKey": settings["API_KEY_CAPMONSTER"],
                    "taskId": request_id,
                },
                headers={"Content-Type": "application/json"},
            )
            result = result_response.json()
            if result["status"] == "processing":
                print("CAPTCHA still processing...")
            retries -= 1

        if result["status"] == "ready":
            print("CAPTCHA success..")
            return result["solution"]["token"]
        else:
            print("Error captcha:", result)
            return None
    except Exception as error:
        print("Error captcha:", str(error))
        return None