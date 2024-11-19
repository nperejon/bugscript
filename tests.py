from source.file_manager import FileManager
from utils import execute_file


if __name__ == '__main__':
    test_files = ['01.bug', '02.bug', '03.bug', '04.bug', '05.bug', '06.bug']

    file_manager = FileManager()

    for file in test_files:
        print(f"\n\nExecuting file {file}: \n")
        execute_file(file_manager, 'tests', file)