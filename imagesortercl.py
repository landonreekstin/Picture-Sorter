from PIL import Image
import os
import shutil
import win32gui
import re
import keyboard
import PySimpleGUI as sg

unsorted_directory = "D:/Save Files/Export2/Image"
sorted_directory = "D:/Save Files/DriveVersion/Picture"
#unsorted_directory = "C:/Users/lando/Documents/Landon/ImageSorter/TestSource"
#sorted_directory = "C:/Users/lando/Documents/Landon/ImageSorter/TestDest"

# Window active management
class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)

    def set_focus(self):
        """Activate the window"""
        win32gui.SetActiveWindow(self._handle)

# command line ui management
class PromptResponse:
    # Prompmt responses for a yes or no question
    # Returns action for a yes response
    def y(self):
        return True
    # Returns action for a no response
    def n(self):
        return False

    # prompt responses for a user command
    # Action for delete command, deletes current unsorted image
    def delete(self):
        return
    # Action for skip command, skips current unsorted image
    def skip(self):
        return
    # Action for help command, returns key commands for actions
    def help():
        return


# autocompletes directory, creates new if none found
def autocomplete(val):
    dir_exists = False
    # loops over the exisiting directories in the sorted_directory
    for filename in os.listdir(sorted_directory):
        # checks if input matches any part of the actual directories
        lowercase_filename = filename.lower()
        val_lower = val.lower()
        if val in filename:
            dir_exists = True
            new_file_path = os.path.join(sorted_directory, filename)
            return new_file_path
        elif val in lowercase_filename:
            dir_exists = True
            new_file_path = os.path.join(sorted_directory, filename)
            return new_file_path
        elif val_lower in lowercase_filename:
            dir_exists = True
            new_file_path = os.path.join(sorted_directory, filename)
            return new_file_path

    if dir_exists == False:
        print("No autocomplete found, create new directory as " + val + "?")
        response = input()
        user_verify = False
        while (user_verify == False):
            if response == "Y" or "y":
                user_verify = True
                path = os.path.join(sorted_directory, val)
                os.mkdir(path)
                print("Created directory")
                return path
            elif response == "N" or "n":
                print("Enter new directory name:")
                dir_name = input()
                path = os.path.join(sorted_directory, dir_name)
                os.mkdir(path)
                print("Directory created")
                return path
            else:
                print("Invalid Response")
                #loop back and ask again



# Saves file to its new directory
def saveNewDir(dir, file):
    full_source_path = os.path.join(unsorted_directory, file)
    full_save_path = dir
    
    shutil.move(full_source_path, full_save_path)
    print("File moved successfully")

# shows unsorted image and prompts target directory
def promptSortOption(filename):
    # creating image preview of unsorted image
    unsorted_image = Image.open(filename)
    unsorted_image.show()
    
    user_verify = False
    while (user_verify == False):
        print("Enter target folder: ")
        target_dir = input()
        # returns full target directory
        returned_dir = autocomplete(target_dir)
        print(returned_dir + ": OK to use this directory?")
        user_response = input("Enter Y/N")
        if user_response == "Y" or "y":
            user_verify = True
            # Y accepted, move file to new directory
            print("Moving file")
            saveNewDir(returned_dir, filename)
        elif user_response == "N" or "n":
            user_verify = False
            # loop back and ask again
        else:
            print("Invalid Response")
            #loop back and ask again



def main():
    for filename in os.listdir(unsorted_directory):
        filepath = os.path.join(unsorted_directory, filename)
        promptSortOption(filepath)
        if len(os.listdir(unsorted_directory)) == 0:
            print("No more files to sort")
            exit()
        else:
            continue

if __name__ == "__main__":
    main()