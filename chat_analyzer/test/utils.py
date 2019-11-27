import os


def get_test_path(relative_file_path: str) -> str:
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    return os.path.join(current_directory, "test_files/" + relative_file_path)
