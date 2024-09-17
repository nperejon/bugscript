class FileManager:
    def get_content_file(self, file_path_to_extract) -> str:
        with open(file_path_to_extract, 'r', encoding="utf-8") as file:
            result = file.read()
        return result

    def write_result_in_file(self, file_path_to_write_result : str, content : str) -> None:
        with open(file_path_to_write_result, 'w+', encoding="utf-8") as file:
            file.write(content)