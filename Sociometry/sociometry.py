import os
import random
import time

# third party modules
import Utils.sociometry_tools as sociometry_tools
import Utils.moodle_tools as moodle_tools
import Utils.gmail_tools as gmail_tools
import Utils.zip_tools as zip_tools
import Utils.docx_tools as docx_tools

MAIN_FOLDER = "./Sociometry/" + "סוציומטרי מא סמסטר ג" + "_" + str(random.randint(0, 1000)) + "/"
MAIN_FOLDER = "./Sociometry/" + "test" + "_" + str(random.randint(0, 1000)) + "/"
MAIN_FOLDER = "./Sociometry/" + "סוציומטרי לדוגמא" + "/"
MAIN_FOLDER = "./Sociometry/" + "סוציומטרי_ניסוי" + "/"


def stage_1():
    try:
        os.mkdir(MAIN_FOLDER)
    except Exception as e:
        pass

    responses_path = MAIN_FOLDER + "Responses/"
    outputs_path = MAIN_FOLDER + "Outputs/"
    # os.mkdir(responses_path)
    # os.mkdir(outputs_path)
    #
    # # Pull all responses from moodle
    # moodle_tools.save_stage_1(responses_path)

    # Run Amir's script
    socio_tool = sociometry_tools.SociometryTools(responses_path, outputs_path)
    socio_tool.run()

    # Turn into Zip file for Adi
    try:
        os.mkdir(outputs_path + "חניכים_קבצים" + "/")
    except:
        pass

    zip_path = "./Sociometry/Outputs.zip"
    docx_tools.create_docx_dir(outputs_path + "חניכים" + "/", outputs_path + "חניכים_קבצים" + "/")
    zip_tools.compress(outputs_path, zip_path)

    # Send to Adi metula
    gmail_tools.stage1(zip_path)


def stage_2():
    pass


if __name__ == "__main__":
    stage_1()
