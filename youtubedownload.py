# Author: Ale Cruz
# Purpose: Script used to download YouTube videos with the
#          url provided
# Date: 04-05-21
# Version: 1.0

# libraries in use
import sys
import os
import _thread
import tkinter as tk
from tkinter import filedialog

from datetime import datetime
from urllib.error import URLError

from pytube import YouTube
from pytube.exceptions import PytubeError
from pytube.exceptions import RegexMatchError
from pytube.exceptions import VideoUnavailable


class YouTubeDownload:
    '''Window displays the widgets to ask user for import about
a specific video user wants to download'''
    
    def __init__(self):
        '''Construct a window to ask user for information about
the video he or she wishes to download and store. It will ask the user
for the link of the video as well as the location to store it at.
'''
        #Create all of the widgets that will be manipulated
        self.main_window = None
        self.url_field = None
        self.audio_video_radbutton = None
        self.audio_only_radbutton = None
        self.save_field = None
        self.explore_button = None
        self.download_button = None
        self.message_label = None

        # Create main window that will contain all of the widgets
        self.main_window = tk.Tk(screenName = "MainWindow")
        self.main_window.title("YouTube Download")
        self.fix_size()

        # Input variables from user
        self.audio_only = tk.BooleanVar(self.main_window, False) # audio or video holder
        self.url = tk.StringVar(self.main_window) # url holder
        self.path = tk.StringVar(self.main_window) # path holder

        # Create label with title of screen
        self.create_title_of_screen()

        # Create video link input with label and field
        self.create_link_video_input()

        # Create radio buttons for type of download
        self.create_radiobutton_download_type()

        # Create destination of download with label, field, and auto-location button
        self.create_download_path()

        # Create download button
        self.create_download_button()

        self.main_window.mainloop()


    def create_title_of_screen(self):
        '''Creates the title of the screen with font and the
placement in the in window'''

        # Create label title of the screen
        self.main_window.update() # Update the window
        title_label = "YouTube Video and Audio Downloader"
        screen_title_label = tk.Label(self.main_window, text = title_label)

        # set font
        screen_title_label.configure(font = ("Arial", 18, "bold"))

        # set locations
        x_location = (self.main_window.winfo_width() // 2) - \
                     (screen_title_label.winfo_reqwidth() // 2)
        y_location = 30

        # placement in window
        screen_title_label.place(x = x_location, y = y_location)


    def create_link_video_input(self):
        '''Creates the textfield for input of the url of the video. It also
creates the label for the input textfield. It gives font and placement in
the window'''

        # Creates the textfield for the link of the video
        self.url_field = tk.Entry(self.main_window, textvariable = self.url)
        self.url_field.configure(font = ("Cambria", 13, "normal"))

        # Creates the label for the link of the video
        title_label = "Video URL"
        url_label = tk.Label(self.main_window, text = title_label)
        url_label.configure(font = ("Tahoma", 11, "normal"))

        # set locations
        x_field = (self.main_window.winfo_width() // 2) - 175
        y_field = (self.main_window.winfo_height() // 5)
        x_label = x_field - (url_label.winfo_reqwidth())
        y_label = y_field

        # placement in window
        self.url_field.place(x = x_field, y = y_field, width = 400)
        url_label.place(x = x_label, y = y_label)


    def create_radiobutton_download_type(self):
        '''Creates the radiobuttons to specify the type of download.
It sets the location within the mainWindow'''

        # Creates the radio buttons
        self.audio_video_radbutton = tk.Radiobutton(self.main_window,
                                                   text = "Video with Audio",
                                                   variable = self.audio_only,
                                                   value = False)
        self.audio_video_radbutton.configure(font=("System", 12, "normal"))
        
        self.audio_only_radbutton = tk.Radiobutton(self.main_window,
                                                    text = "Audio Only",
                                                    variable = self.audio_only,
                                                    value = True)
        self.audio_only_radbutton.configure(font=("System", 12, "normal"))

        self.url_field.update() # updates the url field

        # sets the locations
        x_video = self.main_window.winfo_width() // 2
        y_video = self.url_field.winfo_y() + self.url_field.winfo_reqheight() + 10
        x_audio = x_video - self.audio_video_radbutton.winfo_reqwidth()
        y_audio = y_video

        # placement in window
        self.audio_only_radbutton.place(x = x_audio, y = y_audio)
        self.audio_video_radbutton.place(x = x_video, y = y_video)

        
    def create_download_path(self):
        '''Create the widgets to gather input of the user to where to save the video.
It specifies the location of widgets in the window'''

        # creates the save label
        save_text = "Save To"
        save_label = tk.Label(self.main_window, text = save_text)
        save_label.configure(font = ("Tahoma", 11, "normal"))

        # Creates the save text field 
        self.save_field = tk.Entry(self.main_window,
                                   textvariable = self.path,
                                   state = 'disabled')
        self.save_field.configure(font = ("Cambria", 13, "normal"))

        # Button to open explorer
        self.explore_button = tk.Button(self.main_window, text = "Open Folder",
                                   command = self.open_folder_action)
        self.explore_button.configure(font = ("Ubuntu", 13, "normal"))

        # get locations
        x_save_field = self.url_field.winfo_x() - (save_label.winfo_reqwidth() // 2) \
                       - (self.explore_button.winfo_reqwidth() // 2)
        y_save_field = (self.main_window.winfo_height() * 4) // 10
        x_explore_button = x_save_field + 405
        y_explore_button = y_save_field - 3
        x_save_label = x_save_field - save_label.winfo_reqwidth()
        y_save_label = y_save_field

        # placement in window
        save_label.place(x = x_save_label, y = y_save_label)
        self.save_field.place(x = x_save_field, y = y_save_field, width = 400)
        self.explore_button.place(x = x_explore_button, y = y_explore_button)
        

    def create_download_button(self):
        '''Creates a download button and it sets its font with the location within
the window'''

        #create the download button
        self.download_button = tk.Button(self.main_window,
                                    text = "Download",
                                    command = self.download_button_action)
        self.download_button.configure(font = ("Ubuntu", 13, "normal"))

        # sets locations
        x_location = self.main_window.winfo_width() // 2 - \
                     (self.download_button.winfo_reqwidth() // 2)
        y_location = self.main_window.winfo_height() * 6 // 10

        # Placement in window
        self.download_button.place(x = x_location, y = y_location)


    def download_button_action(self):
        '''Action taken when the download button is pressed'''
        
        # Get the link of the video
        # If no link is given, then the default of where the
        # program is running will be used
        url_link = self.url.get()
        if len(self.path.get()) == 0:
            path_save = os.getcwd() + "\\"
            self.save_field['state'] = 'normal'
            self.save_field.insert(tk.INSERT, path_save)
            self.save_field['state'] = 'disabled'
        else:
            path_save = self.path.get()

        # Create a new thread to handle the download and the buttom
        # thread will go back to handle gui
        _thread.start_new_thread(self.download_video, (url_link, path_save, ))


    def open_folder_action(self):
        '''Action taken when the open button is pressed'''

        # Let user decide the file name path of where to store the video
        filename_path = filedialog.askdirectory()
        if len(filename_path) != 0:
            self.save_field['state'] = 'normal'
            self.save_field.delete('0', tk.END)
            self.save_field.insert(tk.INSERT, filename_path + "/")
            self.save_field['state'] = 'disabled'

    def set_message(self, value):
        '''Sets the text of the label message to display user state of program'''

        # If message label hasn't been created yet
        if self.message_label == None:
            self.message_label = tk.Label(self.main_window, text = value)
            self.message_label.configure(font = ("Helvetica", 12, "normal"))
        else:
            self.message_label.config(text = value)

        # get locations
        x_location = self.main_window.winfo_width() // 2 - \
                         (self.message_label.winfo_reqwidth() // 2)
        y_location = self.main_window.winfo_height() * 8 // 10

        # Place on window
        self.message_label.place(x = x_location, y = y_location)


    def widgets_active(self, is_active : bool):
        '''This method activates and deactivates the widgets of radio buttons
and regular buttons. This method is used when a download is being performed.
            :param bool is_active:
                    True to activate. False to deactivate'''

        # Activate them
        if is_active:
            self.download_button['state'] = 'normal'
            self.audio_video_radbutton['state'] = 'normal'
            self.audio_only_radbutton['state'] = 'normal'
            self.explore_button['state'] = 'normal'
        else: # Deactivate them
            self.download_button['state'] = 'disabled'
            self.audio_video_radbutton['state'] = 'disabled'
            self.audio_only_radbutton['state'] = 'disabled'
            self.explore_button['state'] = 'disabled'
    

    def fix_size(self, width : int = 750, height : int = 400):
        '''Fixed the size of the mainwindow.
            :param int width:
                    The Width of the window
            :param int height:
                    The height of the window'''
        
        self.main_window.geometry(str(width)+"x"+str(height))
        self.main_window.resizable(0, 0)

    def download_video(self, url_link, path_save):
        '''This method itself is a thread that will download the video
from the given url link and save it in the path given. It catch most
errors given.

            Invalid URL: Simple enough if the link is invalid or doesn't exist
            Video Unavailable: If the video is private or if the video is from
                               youtube red it won't download
            Connection Error: If there is no internet you can't get the video
            Other Error: Any other error

            :param url_link:
                    The link of the video
            :param path_save:
                    Path to where to save the video.'''
        
        self.widgets_active(False) # deactivate widgets since download is in progress

        # Get the link
        try:
            youtube_video = YouTube(url_link)
            self.set_message("Downloading...")
        except RegexMatchError:
            self.set_message("Invalid URL")
            self.widgets_active(True)
            return

        # Decide if whole video or just audio
        try:
            if self.audio_only.get():
                video = youtube_video.streams.get_audio_only()
            else:
                video = youtube_video.streams.get_highest_resolution()
                
            video.download(path_save) # download 
        except VideoUnavailable:
            self.set_message("Video Unavailable")
            self.widgets_active(True)
            return
        except URLError:
            self.set_message("Connection Error")
            self.widgets_active(True)
            return
        except (PytubeError, Exception):
            self.set_message("An Error Occurred")
            self.widgets_active(True)
            return
            
        self.set_message("Completed!")
        self.widgets_active(True)

            


def main():
    '''Main method '''
    window_frame = YouTubeDownload()

if __name__ == "__main__":
    main()

    
