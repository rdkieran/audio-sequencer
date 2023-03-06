## manipulating directories of split audio files. reading directories of files, parsing filenames, changing filenames
## refering to original script to extract sequence of commands for sorting files

import os

def get_speaker_names():
    list_of_speakers = []
    number_of_speakers = input("How many speakers?: ")
    for speaker in range(int(number_of_speakers)):
        print("\nSpeaker No."+str(speaker+1)+" name:")
        speaker_name = input().lower()
        list_of_speakers.append(speaker_name)
    return list_of_speakers

def get_folders(list_of_speakers):
    list_of_folders = []
    for speaker in list_of_speakers:
        print("\n------\nSpeaker: "+speaker.capitalize())
        folder = input("Audio file folder: ")
        name_and_folder = (speaker,folder)
        list_of_folders.append(name_and_folder)
    return list_of_folders

def get_files(list_of_folders, list_of_speakers):
    all_files = []
    
    for speaker in range(len(list_of_speakers)):
        folder = list_of_folders[speaker][1]
        list_of_files = os.listdir(folder)
        list_of_files = (list_of_speakers[speaker], folder, list_of_files)
        all_files.append(list_of_files)

    return all_files

def make_directory(list_of_folders):
    folder_path = list_of_folders[0][1]

    folder_path = '\\'.join(folder_path.split('\\')[:-1])
    #eg 'C:\Users\Robbie\Documents\AudioTranscription\7-two-person-dialogue\albert--albert-audio'
    ##  | <--------------------------------------------------------------> |

    destination_folder = 'final-splits'
    dir = os.path.join(folder_path, destination_folder)
    try:
        os.rmdir(dir)
        os.mkdir(dir)
    except:
        os.mkdir(dir)

def get_instructions():
    script = input("Script file: ")
    script_lines = []

    with open(script) as f:
        for line in f:
            line = line.strip().split(' ')

            name = line[0]
            line = ' '.join(line[1:])

            line = (name, line)
            script_lines.append(line)
    
    return script_lines

## using script, move files into new folder in correct order.
## when moving files, always take the /last/ repeated line, and leave the old one behind.
def find_files(script_lines, all_files):
    file_number = 0000

    for line in script_lines:
        script_name, script_line = line[0], line[1]
        for speaker in all_files:
            speaker_name = speaker[0]
            ## ie. david, albert
            speaker_folder = speaker[1]
            ## eg. c:\\Users\\Robbie\\Documents\\AudioTranscription\\7-two-person-dialogue\\david--david-audio
            speaker_files = speaker[2]
            ## list of file names

            if script_name == speaker_name:
                for file_name in speaker_files:
                    file_line = (file_name.split('-')[1]).split('.')[0]
                    if file_line.strip() == script_line.strip():
                        file_number += 1
                        move_file(file_number, speaker_folder, file_name)
            else:
                continue

## rename / move matched files found by find_files(), in order of script
def move_file(file_number, speaker_folder, file_name):
    speaker_folder_path = '\\'.join(speaker_folder.split('\\')[:-1])
    new_file_path = speaker_folder_path +'\\final-splits\\'+ str(file_number).zfill(4) +'-'+ file_name

    old_file = speaker_folder+'\\'+file_name

    os.rename(old_file, new_file_path)

def main():
    list_of_speakers = get_speaker_names()                      ## list_of_speakers = [name1, name2]
    list_of_folders = get_folders(list_of_speakers)             ## list_of_folders = [(name1, folder), (name2, folder)]
    all_files = get_files(list_of_folders, list_of_speakers)    ## all_files = [(name1, [file1, file2]), (name2, [file1, file2])]
    make_directory(list_of_folders)                              ## make new directory to move files into
    script_lines = get_instructions()                           ## script_lines = [(name1, line1), (name2, line1), (name1,line2)]

    print(all_files)
    find_files(script_lines, all_files)

main()