# import pyminizip
#
#
# def compress(old_path, new_path):
#     pyminizip.compress(old_path, None, new_path, "CyberCyber1*", 5)
#
# import zipfile
#
# def compress(old_path, new_path):
#     zipfile.compress(old_path, None, new_path, "CyberCyber1*", 5)

import subprocess
import os


def compress(dir_path, zip_name, password):
    subprocess.call(
        '"C:\\Program Files\\7-Zip\\7z.exe" a -mem=AES256 -p' + password + ' -y ' + zip_name + " " + dir_path + "*",
        shell=True)
