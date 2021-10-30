# This version adds more ease of use and functionality by creating a GUI.


from PIL import Image
import os
import shutil
import win32gui
import re
import keyboard
import PySimpleGUI as sg

unsorted_directory = "D:/Save Files/Export/Picture/New"
sorted_directory = "D:/Save Files/DriveVersion/Picture"
#unsorted_directory = "C:/Users/lando/Documents/Landon/ImageSorter/TestSource"
#sorted_directory = "C:/Users/lando/Documents/Landon/ImageSorter/TestDest"


# Handle file browsing for selecting unsorted folder
def select_unsorted():
    return

# Handle file browsing for selecting sorted folder
def select_sorted():
    return

# Creates the gui
def gui():
    # Creates the elements in the window
    layout = [[sg.Text("Chose folder of unsorted media")], [sg.Button("Select source")], [sg.Text("Chose folder of sorted media")], 
        [sg.Button("Select destination")]]
    # Create the window with elements
    window = sg.Window("Photo Sorter", layout)
    return window

# Manages window events
def event_loop(window):
    # Create an event loop
    while True:
        event, values = window.read()
        # Select source folder
        if event == "Select source":
            select_unsorted()
        if event == "Select destination":
            select_sorted()
        # Close Window
        if event == sg.WIN_CLOSED:
            break

    window.close()

"""
# Get user input, returns type of response
def get_input(prompt_type):
    keyboard.on_press_key("Enter", lambda _:print("You pressed r"))
    if prompt_type == "y_n":
        print("<Enter: Accept>  <Backspace: Decline>")
        if user_response == 
            prompt_response = "Yes"
            return prompt_response
        elif user_response == "N" or "n" or "no" or "No" or "Ye" or "ye":
            prompt_response = "Yes"
            return prompt_response


# Manages the UI commands
def ui(prompt_type):
    prompt_complete = False
    while(prompt_complete == False):
        if prompt_type == "y_n":
            if 
            prompt_complete = True
"""


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