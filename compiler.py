from source.file_manager import FileManager
import sys

from utils import execute_file

if __name__ == '__main__':
    args = sys.argv

    if(len(args) != 2):
        raise Exception("The bug file path must be passed as argument! ex: python compiler.py file.bug")

    file = args[1]

    file_manager = FileManager()
    execute_file(file_manager, './', file)