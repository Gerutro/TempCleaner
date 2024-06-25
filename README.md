# TempCleaner

Cleans your `temp` and `%temp%` directories.

-----

## Windows Defender
Windows Defender complains about "Critical threat" and "Trojan" because the application gets the ability to do anything with a folder that requires administrator rights without running the program as an administrator. The corresponding function is:  
```python
def change_permissions(path):
    try:
        current_permissions = os.stat(path).st_mode
        if not (current_permissions & stat.S_IRWXU):
            _log.log(logging.INFO, f"Changing permissions for {cut_path(path)}.")

            new_permissions = current_permissions | stat.S_IRWXU
            os.chmod(path, new_permissions)
            _log.log(logging.INFO, f"{cut_path(path)}: 1000")
        else:
            _log.log(logging.INFO, f"{cut_path(path)}: 1500")
    except Exception as e:
        _log.log(logging.ERROR, f"{cut_path(path)}: {e}")
        print(f"Error when changing permissions for {cut_path(path)}: {e}")
```
Defender sees this and does not allow the program to run.

-----

## Log file
.log file is located in: `C:\Users\user\AppData\Roaming\TempCleaner\main.log`

-----

## Error codes
If you want to analyze .log file yourself, codes here:
- 1000 - changing permissions for path successful
- 1500 - permissions for path are already set correctly
- 2000 - file is occupied by another program
- 2500 - no access to directory

-----

## GitHub releases
You can see the prefixes in the version name.   
All prefixes list:  
- `-rx0` - release version;  
- `-prx0` - pre-release version;  
- `-bx0` - beta version;  
- `-ax0` - alpha version;  
- `-fx0` - only for first-first testers(usually the lead developer).  
