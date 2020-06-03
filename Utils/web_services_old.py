import requests
import base64


class MoodleAPI:
    BASE_URL = "http://talportal.tk/moodle/webservice/rest/server.php"

    MOBILE_TOKEN = "ab4694d00be1c59dddceaafc3ce879f7"
    MY_SERVICE_TOKEN = "84952d24fbdaee722cda4395ecc4b2d8"

    BASE_PARAMS = {
        "wstoken": MY_SERVICE_TOKEN,
        "moodlewsrestformat": "json"
    }

    def __init__(self):
        pass

    def get_token(self):
        token_url = "http://talportal.tk/moodle/login/token.php"
        params = {
            "username": "talporteam",
            "password": "CyberCyber1*",
            "service": "moodle_mobile_app"
        }
        print(requests.post(token_url, data=params).content)
        MoodleAPI.BASE_PARAMS["wstoken"] = requests.post(token_url, data=params).json()["token"]

    def make_api_call(self, wsfunction, args={}):
        # set API params
        params = MoodleAPI.BASE_PARAMS.copy()
        params["wsfunction"] = wsfunction
        params = {**params, **args}

        print(requests.post(MoodleAPI.BASE_URL, data=params).content)
        return requests.post(MoodleAPI.BASE_URL, data=params).json()

    def get_file_call(self, url):
        params = {
            "token": MoodleAPI.BASE_PARAMS["wstoken"]
        }
        return requests.get(url=url, params=params).content

    def save_submission(self):
        self.make_api_call("mod_assign_save_submission")

    def get_assignments(self):
        params = {
            "courseids[0]": 8
        }
        self.make_api_call("mod_assign_get_assignments", params)

    def get_submissions(self):
        data = self.make_api_call(
            "mod_assign_get_submissions",
            {"assignmentids[0]": 1}
        )
        for submission in data["assignments"][0]["submissions"]:
            self.save_file(submission["plugins"][0]["fileareas"][0]["files"][0])

    def save_file(self, file):
        with open(f'./files/{file["filename"]}', 'wb') as f:
            f.write(self.get_file_call(file["fileurl"]))

    def upload_file(self):
        filename = "./files/gant.xlsx"

        params = {
            "filearea": "draft",
            "filepath": "/",
            "filename": "NewFile.xlsx",
            "component": "user",
            "itemid": 0,
        }
        default_params = {
            # "contextid": 0,
            "contextlevel": "user",
            "instanceid": 2,
        }
        params = {**params, **default_params}

        with open(filename, 'rb') as f:
            params["filecontent"] = base64.b64encode(f.read())

        self.make_api_call("core_files_upload", params)

    # def upload_file_2(self):
    #     params = {
    #         "filepath": "example/",
    #         "token": MoodleAPI.BASE_PARAMS["wstoken"],
    #         "itemid": 0
    #     }
    #     with open("files/High-Performance-Habits.pdf", 'rb') as f:
    #         params["file_1"] = base64.b64encode(f.read())
    #
    #     url = "http://talportal.tk/moodle/webservice/upload.php"
    #     a = requests.post(url=url, data=params).content
    #     print(a)