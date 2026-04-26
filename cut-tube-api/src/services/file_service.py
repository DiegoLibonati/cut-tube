import os


class FileService:
    @staticmethod
    def remove_file(file_path: str) -> None:
        os.remove(file_path)

    @staticmethod
    def path_exists(path: str) -> bool:
        return os.path.exists(path)

    @staticmethod
    def make_dirs(path: str, exist_ok: bool = True) -> bool:
        return os.makedirs(path, exist_ok=exist_ok)
