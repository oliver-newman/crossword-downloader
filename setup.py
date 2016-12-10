"""
Python script to make the setup of the crossword download system a bit neater.
To be run after downloading the repository, in order to specify the folder into
which the puzzles are to be downloaded every day.

Usage: python setup.py <crossword_archive_path>
"""
from sys import argv
import os.path

MAIN_FILE_NAME = "downloadPuz.py"
ARCHIVE_PATH_VARIABLE_ASSIGN = "ARCHIVE_PATH ="


"""
For incorrect argument counts
"""
class ArgcException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

"""
When a nonexistent path is entered by the user
"""
class PathExistsException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg


def main():
    argc = len(argv)
    if argc != 2:
        print(argc)
        raise ArgcException("Usage: python setup.py <crossword_archive_path>")

    archivePath = argv[1]
    if not os.path.exists(archivePath):
        raise PathExistsException("Not a valid path.")

    with open(MAIN_FILE_NAME, "r") as mainFile:
        mainFileLines = mainFile.readlines()

    # Assign ARCHIVE_PATH global in main file to command line arg archivePath
    for i in range(len(mainFileLines)):
        if mainFileLines[i].startswith(ARCHIVE_PATH_VARIABLE_ASSIGN):
            print("Found line")
            mainFileLines[i] = \
                ARCHIVE_PATH_VARIABLE_ASSIGN + " \"" + archivePath + "\"\n"

    with open(MAIN_FILE_NAME, "w") as mainFile:
        mainFile.writelines(mainFileLines)


if __name__ == "__main__":
    main()
