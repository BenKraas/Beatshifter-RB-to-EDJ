import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
import xml.etree.ElementTree as ET
from pydub import AudioSegment

class XMLEditor:
    def __init__(self):
        self.XML_content = ""
        self.XML_path = ""
        self.XML_saved = False
        self.Path_to_dev_XML = Path("/home/ben/scripts/Beatshifter-RB-to-EDJ/Dev/2024-03-09.xml")
        self.window = tk.Tk()
        self.window.title('XML Editor')
        self.window.geometry('500x200')
        self.create_buttons()
        self.create_text_fields()

    def create_buttons(self):
        button_frame = tk.Frame(self.window)
        button_frame.pack(side=tk.TOP)

        load_button = tk.Button(button_frame, text='Load XML', command=self.open_file, width=20, height=5)
        load_button.pack(side=tk.LEFT)

        shift_button = tk.Button(button_frame, text='Apply Shift', command=self.shift_position_marks, width=20, height=5)
        shift_button.pack(side=tk.LEFT)

        save_button = tk.Button(button_frame, text='Save XML', command=self.save_xml, width=20, height=5)
        save_button.pack(side=tk.LEFT)

    def create_text_fields(self):
        text_frame = tk.Frame(self.window)
        text_frame.pack(side=tk.BOTTOM)

        self.xml_path_button = tk.Button(text_frame, state=tk.DISABLED, width=20, height=2)
        self.xml_path_button.pack(side=tk.LEFT)

        self.xml_content_button = tk.Button(text_frame, state=tk.DISABLED, width=20, height=2)
        self.xml_content_button.pack(side=tk.LEFT)

        self.xml_created_button = tk.Button(text_frame, state=tk.DISABLED, width=20, height=2)
        self.xml_created_button.pack(side=tk.LEFT)

    def update_text_fields(self):
        self.xml_path_button.config(state=tk.NORMAL)
        self.xml_content_button.config(state=tk.NORMAL)
        self.xml_created_button.config(state=tk.NORMAL)

        self.xml_path_button.config(text="")
        self.xml_content_button.config(text="")
        self.xml_created_button.config(text="")

        if self.XML_path != "":
            self.xml_path_button.config(text="XML loaded")
        if self.XML_content != "":
            self.xml_content_button.config(text="XML shifted")
        if self.XML_saved == True:
            self.xml_created_button.config(text="XML saved")

        self.xml_path_button.config(state=tk.DISABLED)
        self.xml_content_button.config(state=tk.DISABLED)
        self.xml_created_button.config(state=tk.DISABLED)

    ## LOGIC
    def open_file(self):
        file_path = self.Path_to_dev_XML
        self.XML_path = file_path
        self.update_text_fields()

    def shift_position_marks(self):
        tree = ET.parse(self.XML_path)
        root = tree.getroot()

        for dj_playlists in root.iter('DJ_PLAYLISTS'):
            for collection in dj_playlists.iter('COLLECTION'):
                for track in collection.iter('TRACK'):
                    # Print entire track content for debugging
                    # print(ET.tostring(track, encoding='utf-8').decode())

                    # Get .mp3 file path
                    file_path = Path(track.get('Location'))

                    # For development purposes, replace C with /mnt/c
                    file_path = file_path.as_posix().replace('C:', '/mnt/c')

                    # Detect silence in .mp3 file
                    silence_ms = self.detect_silence(file_path)

                    # Print track title for debugging
                    print(f"Track: {track.get('Name')}/nFound: {silence_ms} of silence")


        self.XML_content = ET.tostring(root, encoding='utf-8').decode()
        self.update_text_fields()

    def save_xml(self):
        file_path = str(self.XML_path).replace('.xml', '_shifted.xml')

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(self.XML_content)

        self.XML_saved = True
        self.update_text_fields()

    def detect_silence(self, file_path):
        # Load the MP3 file
        audio = AudioSegment.from_file(file_path)

        # Define the duration of a frame in milliseconds (for 44.1kHz sample rate)
        frame_duration = 26.122448979591837  # Approx. 26.122 ms per frame for 44.1kHz sample rate

        # Duration of silence frame to be checked (in milliseconds)
        silence_frame_duration = frame_duration * 1152  # 1152 frames per mp3 frame

        # Get the first segment of the audio with duration equal to the expected silence frame duration
        first_segment = audio[:silence_frame_duration]

        # Check if the first segment is silent
        is_silent = first_segment.dBFS < -60  # Adjust threshold as per your requirement

        return is_silent
        
        


    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    editor = XMLEditor()
    editor.run()




#LEGACY
                    # if tempo is not None:
                    #     inizio = float(tempo.get('Inizio'))

                    #     for position_mark in track.iter('POSITION_MARK'):
                    #         start = float(position_mark.get('Start'))
                    #         start = round(start, 3)
                    #         position_mark.set('Start', str(start + inizio))

"""
Write a function which iterates over every TRACK an XML file and shifts all POSITION_MARK Start values by the Inizio (shift value)

The XML file will have the following structure:

<DJ_PLAYLISTS Version="1.0.0">
  <PRODUCT Name="rekordbox" Version="6.8.2" Company="AlphaTheta"/>
  <COLLECTION Entries="386">
    <TRACK TrackID="22929579" Name=" Turbine" Artist="Misanthrop" Composer=""
           Album="Analog" Grouping="" Genre="Drum &amp; Bass" Kind="MP3 File"
           Size="8655333" TotalTime="215" DiscNumber="0" TrackNumber="4"
           Year="2019" AverageBpm="172.02" DateAdded="2024-02-04" BitRate="320"
           SampleRate="44100" Comments="" PlayCount="2" Rating="255" Location="file://localhost/C:/Users/Kasto/OneDrive/DJ-Main/Archive%20of%20great%20music/Library/Purchased/LDnB/12600437_Turbine_(Original%20Mix)_P2023.mp3"
           Remixer="" Tonality="2A" Label="Neosignal Recordings" Mix="">
      <TEMPO Inizio="0.042" Bpm="172.02" Metro="4/4" Battito="1"/>
      <POSITION_MARK Name="Build 1" Type="0" Start="22.365" Num="0" Red="170" Green="114"
                     Blue="255"/>
      <POSITION_MARK Name="" Type="0" Start="67.011" Num="1" Red="40" Green="226"
                     Blue="20"/>
      <POSITION_MARK Name="" Type="0" Start="133.980" Num="2" Red="180" Green="50"
                     Blue="255"/>
      <POSITION_MARK Name="" Type="0" Start="156.303" Num="3" Red="40" Green="226"
                     Blue="20"/>
      <POSITION_MARK Name="" Type="0" Start="100.495" Num="4" Red="16" Green="177"
                     Blue="118"/>
      <POSITION_MARK Name="" Type="0" Start="111.657" Num="5" Red="170" Green="114"
                     Blue="255"/>
      <POSITION_MARK Name="" Type="0" Start="215.250" Num="7" Red="255" Green="18"
                     Blue="123"/>
    </TRACK>
"""


