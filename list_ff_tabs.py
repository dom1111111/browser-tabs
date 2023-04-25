import lz4.block
import json
from os import path, getenv, listdir
from datetime import datetime

#---------------

# for cross platform version, these are the steps:
## check which browsers are installed
## generate that list of installed browsers and put them in a drop down menu
## set the default option for the dropdown menu to be the systems default browser

# (all buttons grayed out if no browser is installed - and a notification appears to tel user if this is so)
# then, have 2 buttons:
## generate list of current session tabs
### if no browser is open, then this button is grayed out
## generate list of previous session tabs
# > these will show a multiline text box with copyable content (md or plain text formating)

# then once this happens, there is another botton available to export the content to a txt or markdown file
## have this be a save-file dialogue

#---------------

while True:
    appdata_path = getenv('APPDATA')
    if appdata_path:
        profiles_path = path.join(appdata_path, 'Mozilla\Firefox\Profiles')
        if path.isdir(profiles_path):
            for folder in listdir(profiles_path):
                backups_path = path.join(profiles_path, path.join(folder, 'sessionstore-backups'))
                if path.isdir(backups_path):
                    current_path = path.join(backups_path, 'recovery.jsonlz4')
                    previous_path = path.join(backups_path, 'recovery.jsonlz4')
    break

CURRENT_TABS_PATH = current_path if path.isfile(current_path) else None
PREVIOUS_TABS_PATH = previous_path if path.isfile(previous_path) else None
OUTPUT_PATH = "test1.json"

#INPUT_PATH = "testing_firefox_files/recovery.jsonlz4"

def send_error(num=0):
    print('something went wrong')

def get_tabs_file(filepath):
    with open(filepath, 'rb') as file:
        mozilla_header = file.read(8)
        data = file.read()
    tabs_bytes = lz4.block.decompress(data)
    json_data_dict = json.loads(tabs_bytes)
    windows = json_data_dict.get('windows')

    overall_list = []
    # windows is a list of every open firefox window - each window is then a dict
    for window in windows:
        tabs = window.get('tabs')
        for tab in tabs:
            tab_info = tab.get('entries')
            tab_info = tab_info[-1]     # get last item in list of entries (the most recent state)
            overall_list.append((tab_info.get('title'), tab_info.get('url')))
    output = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')[:-4]}_tabs.json"
    
    with open(output, 'w') as file:
        json.dump(overall_list, file, indent=4)

#---------------

# if folder/files not found, then no option will be presented to get tabs
# and display error saying no folder found, firefox may not be installed or open

print(CURRENT_TABS_PATH)
print(PREVIOUS_TABS_PATH)

def get_previous():
    with open(PREVIOUS_TABS_PATH, 'rb') as file:
        mozilla_header = file.read(8)
        data = file.read()
    tabs_bytes = lz4.block.decompress(data)
    json_data_dict = json.loads(tabs_bytes)
    output = f"previous_tabs.json"
    with open(output, 'w') as file:
        json.dump(json_data_dict, file, indent=4)



if CURRENT_TABS_PATH:
    while True:
        print()
        print('enter "1" to get txt file of tabs. "0" to close program')
        i = input()
        if i == '1':
            # get_previous()
            get_tabs_file(CURRENT_TABS_PATH)
        elif i == '0':
            print('bye!')
            print()
            break
else:
    send_error()
    print()
