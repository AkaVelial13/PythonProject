import os
import argparse
import shutil
import re


# ������ ���������� ��� ��������
DIRECTORIES = {
    "Images": [".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".bpg", ".svg", ".heif", ".psd"],
    "Videos": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mng", ".qt", ".mpg", ".mpeg", ".3gp"],
    "Documents": [".oxps", ".epub", ".pages", ".docx", ".doc", ".fdf", ".ods",
                  ".odt", ".pwi", ".xsn", ".xps", ".dotx", ".docm", ".dox",
                  ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt",
                  ".pptx", ".csv"],
    "Audio": [".aac", ".aa", ".aacp", ".dsd", ".dvf", ".m4a", ".m4b", ".m4p",
              ".mp3", ".msv", ".ogg", ".oga", ".raw", ".vox", ".wav", ".wma"],
    "Text": [".txt", ".in", ".out"],
    "Programming": [".py", ".ipynb", ".c", ".cpp", ".class", ".h", ".java",
                    ".sh", ".html", ".css", ".js", ".go", ".json"]
}


def normalize(name):
    # �������������� ������������� �������� �� ��������
    translit = {'�': 'a', '�': 'b', '�': 'v', '�': 'g', '�': 'd', '�': 'e', '�': 'yo',
                '�': 'zh', '�': 'z', '�': 'i', '�': 'y', '�': 'k', '�': 'l', '�': 'm',
                '�': 'n', '�': 'o', '�': 'p', '�': 'r', '�': 's', '�': 't', '�': 'u',
                '�': 'f', '�': 'h', '�': 'ts', '�': 'ch', '�': 'sh', '�': 'shc', '�': '',
                '�': 'y', '�': '', '�': 'e', '�': 'yu', '�': 'ya'}
    name = name.lower()
    for cyr, lat in translit.items():
        name = name.replace(cyr, lat)
    # ������ ������������ �������� �� '_'
    name = re.sub(r'[^\w\s-]', '_', name)
    # �������� ������������� ��������
    name = re.sub(r'\s+', ' ', name)
    # ������ �������� �� '_'
    name = name.strip().replace(' ', '_')
    return name


def create_directories(root):
    """
    ������� ���������� ��� ������
    """
    for directory in DIRECTORIES:
        directory_path = os.path.join(root, directory)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)


def process_file(file_path, root):
    """
    ������������ ���� � ���������� ��� � ��������������� ����������
    """
    for directory, extensions in DIRECTORIES.items():
        for extension in extensions:
            if file_path.lower().endswith(extension):
                file_directory = os.path.join(root, directory)
                # ���������� ���� � ����� �� ��� � ����������
                file_name, file_ext = os.path.splitext(os.path.basename(file_path))
                # �������������� ����� � ������� ������� normalize
                file_name = normalize(file_name) + file_ext
                destination = os.path.join(file_directory, file_name)
                shutil.move(file_path, destination)
                return

    # ���� ���������� ����� �� �������, ���������, �������� �� ���� �������
    archive_extensions = [".zip", ".tar", ".gz"]
    if any(file_path.lower().endswith(extension) for extension in archive_extensions):
        # ���������� ������ � ����� Archives
        archive_name, _ = os.path.splitext(os.path.basename(file_path))
        archive_directory = os.path.join(root, "Archives", archive_name)
        if not os.path.exists(archive_directory):
            os.makedirs(archive_directory)
        shutil.unpack_archive(file_path, archive_directory)

        # �������� ������
        os.remove(file_path)
        return

    # ���� ���� �� �������� ������� � ���������� ����� �� �������, ����������� ���� � ����� "Unknown"
    unknown_directory = os.path.join(root, "Unknown")
    if not os.path.exists(unknown_directory):
        os.makedirs(unknown_directory)
    destination = os.path.join(unknown_directory, os.path.basename(file_path))
    shutil.move(file_path, destination)
    return


def process_directory(root):
    """
    ������������ ��� ����� � ����������
    """
    create_directories(root)
    for path, _, files in os.walk(root):
        for file in files:
            file_path = os.path.join(path, file)
            process_file(file_path, root)


def delete_empty_directories(root):
    """
    ������� ������ ���������� �� �������� ����������
    """
    excluded_directories = [os.path.join(args.path)]

    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        if not dirnames and not filenames and dirpath not in excluded_directories:
            os.rmdir(dirpath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--exclude", nargs='+')
    args = parser.parse_args()
    delete_empty_directories(args.path)
    process_directory(args.path)
