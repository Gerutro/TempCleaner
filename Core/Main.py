import os
import shutil
import tempfile
import stat
import logging


AppData_dir = os.environ.get("APPDATA")

_log = logging.getLogger("Main")
os.mkdir(os.path.join(AppData_dir, "TempCleaner"))
logging.basicConfig(filename=os.path.join(AppData_dir, "TempCleaner", "main.log"),
                    level=logging.NOTSET,
                    format="%(asctime)s: %(name)s: [%(levelname)s] %(message)s",
                    filemode="w",
                    encoding="utf-8")

_log.log(logging.INFO, f"OS: {os.environ.get("OS")}")
_log.log(logging.INFO, f"AppData: {os.environ.get("APPDATA")}")
_log.log(logging.INFO, f"SystemRoot: {os.environ.get("SYSTEMROOT")}")


temp_user = tempfile.gettempdir()
temp_common = os.path.join(os.environ.get('SYSTEMROOT'), 'temp')


def cut_path(path):
    ct_path = path.split("\\")[:1] + path.split("\\")[-2:]
    ct_path.insert(1, "...")
    ct_path = "\\".join(ct_path)
    return ct_path


def change_permissions(path):
    try:
        current_permissions = os.stat(path).st_mode
        new_permissions = current_permissions | stat.S_IRWXU
        os.chmod(path, new_permissions)
    except Exception as e:
        _log.log(logging.ERROR, f"Error when changing permissions for {path}: {e}")
        print(f"Error when changing permissions for {path}: {e}")


def get_size(directory):
    result = 0
    for file in os.listdir(directory):
        result += os.path.getsize(directory + "\\" + file)
    return result


def delete_files(directory):
    try:
        change_permissions(directory)
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            try:
                if os.path.isfile(file_path):
                    change_permissions(file_path)
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except PermissionError:
                _log.log(logging.ERROR, f"Failed to delete {cut_path(file_path)}: 2000")
            except Exception as e:
                _log.log(logging.ERROR, f"Error during deletion {cut_path(file_path)}: {e}")
    except PermissionError:
        _log.log(logging.ERROR, f"{directory}: 3000")


len_temp_user_s = len(os.listdir(temp_user))
len_temp_common_s = len(os.listdir(temp_common))

size_temp_user_s = get_size(temp_user)
size_temp_common_s = get_size(temp_common)

delete_files(temp_user)
delete_files(temp_common)

size_temp_user_e = get_size(temp_user)
size_temp_common_e = get_size(temp_common)

len_temp_user_e = len(os.listdir(temp_user))
len_temp_common_e = len(os.listdir(temp_common))

print(f"User temp files deleted: {len_temp_user_s - len_temp_user_e}")
_log.log(logging.INFO, f"User temp files deleted: {len_temp_user_s - len_temp_user_e}")
print(f"Common temp files deleted: {len_temp_common_s - len_temp_common_e}")
_log.log(logging.INFO, f"Common temp files deleted: {len_temp_common_s - len_temp_common_e}")
print(f"All temp files deleted: {(len_temp_user_s - len_temp_user_e) + (len_temp_common_s - len_temp_common_e)}")
_log.log(logging.INFO, f"All temp files deleted: {(len_temp_user_s - len_temp_user_e) + (len_temp_common_s - len_temp_common_e)}")

print(f"User temp files cleared size: {round((size_temp_user_s - size_temp_user_e)/1024/1024, 2)} MB")
_log.log(logging.INFO, f"User temp files cleared size: {round((size_temp_user_s - size_temp_user_e)/1024/1024, 2)} MB")
print(f"Common temp files cleared size: {round((size_temp_common_s - size_temp_common_e)/1024/1024, 2)} MB")
_log.log(logging.INFO, f"Common temp files cleared size: {round((size_temp_common_s - size_temp_common_e)/1024/1024, 2)} MB")
print(f"All temp files cleared size: {round(((size_temp_user_s - size_temp_user_e)/1024/1024) + ((size_temp_common_s - size_temp_common_e)/1024/1024), 2)} MB")
_log.log(logging.INFO, f"All temp files cleared size: {round(((size_temp_user_s - size_temp_user_e)/1024/1024) + ((size_temp_common_s - size_temp_common_e)/1024/1024), 2)} MB")

input("\nPress enter to continue...")
