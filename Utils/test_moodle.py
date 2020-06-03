import Utils.web_services as web_services


def test():
    moodle = web_services.MoodleAPI()
    moodle.get_token()
    moodle.get_assignments()
    # moodle.upload_file()


if __name__ == '__main__':
    test()
