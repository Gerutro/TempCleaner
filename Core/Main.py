import os
import shutil
import tempfile
import stat


temp_user = tempfile.gettempdir()
temp_common = os.path.join(os.environ.get('SYSTEMROOT'), 'temp')


def fix_permissions(path):
    try:
        current_permissions = os.stat(path).st_mode
        new_permissions = current_permissions | stat.S_IRWXU
        os.chmod(path, new_permissions)
    except Exception as e:
        print(f"\033[31mError when changing permissions for \033[41m{path}\033[31m: \033[41m{e}\033[31m")


def delete_files(directory):
    try:
        fix_permissions(directory)
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            try:
                if os.path.isfile(file_path):
                    fix_permissions(file_path)
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except PermissionError:
                print(f"\033[31mFailed to delete \033[0m\033[41m{file_path}\033[0m\033[31m: file is occupied by another program")
            except Exception as e:
                print(f"\033[31mError during deletion \033[0m\033[41m{file_path}\033[0m\033[31m: \033[41m{e}\033[31m")
    except PermissionError:
        print(f"\033[31mNo access to directory \033[41m{directory}\033[0m")


delete_files(temp_user)
delete_files(temp_common)
input("\033[0m\nPress enter to continue...")
