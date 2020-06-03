import Utils.web_services as web_services

COURSE_ID = 8


def save_stage_1(dir):
    moodle = web_services.MoodleAPI()
    moodle.get_token()
    sociometry_id = get_sociometry_assign_id(moodle)
    save_submissions_to_dir(moodle, dir, sociometry_id)


def save_submissions_to_dir(moodle, dir, assign_id):
    submissions = moodle.get_submissions(assign_id)
    for submission in submissions:
        if not submission["plugins"][0]["fileareas"][0]["files"]:
            # file is empty
            pass
        else:
            moodle.save_file(submission["plugins"][0]["fileareas"][0]["files"][0], dir)


def get_sociometry_assign_id(moodle):
    courses = moodle.get_assignments(COURSE_ID)
    for assign in courses["courses"][0]["assignments"]:
        if assign["name"].startswith("העלאת סוציומטרי חניכים"):
            return assign["id"]


def get_meubad_assign_id(moodle):
    courses = moodle.get_assignments(COURSE_ID)
    for assign in courses["courses"][0]["assignments"]:
        if assign["name"].startswith("העלאת סוציומטרי מעובד"):
            return assign["id"]


def save_stage_2(dir):
    moodle = web_services.MoodleAPI()
    moodle.get_token()
    meubad_id = get_meubad_assign_id(moodle)
    save_submissions_to_dir(moodle, dir, meubad_id)