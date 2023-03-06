##!pip install git+https://github.com/m-bain/whisperX
##!pip install git+https://github.com/openai/whisper.git
##!sudo apt update && sudo apt install ffmpeg

import os

def make_project_directory():
    ## define project title for creating project folder
    project_title = input("Enter project title: ")
    project_title = '-'.join(project_title.lower().split(' '))

#filename = input('Enter .mp3 audio file to transcribe: ')
#command = '!whisperx '+ filename +' --model medium.en'
#os.system(command)