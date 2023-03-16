import re                           # clean_line()
from num2words import num2words     # clean_line()
from pydub import AudioSegment      # split_audio()
import os                           # make_directory(), make_audio_directory(), move_file()
import shutil                       # make_directory(), make_audio_directory()

## STAGE 1: GET INPUTS
def get_all_inputs():

    script_file = ''
    list_of_speakers = []
    list_of_audio_files = []
    list_of_transcript_files = []

    ## script_file
    script_file = input('\nEnter script file (.txt): ')

    ## list_of_speakers
    number_of_speakers = int(input('\nHow many speakers?:\n> '))
    if number_of_speakers > 1:
        print()
        for speaker in range(0, number_of_speakers):
            print('Speaker #'+str(speaker+1)+':')
            speaker_name = input('> ').lower()
            list_of_speakers.append(speaker_name)
    else:
        list_of_speakers.append('narrator')

    ## list_of_audio_files
    ## list_of_transcript_files
    for speaker in list_of_speakers:
        print('\n---'+speaker.capitalize()+'---')
        audio_file = input('Audio file (.wav): ')
        transcript_file = input('Transcript file (.word.srt): ')

        audio_file = (speaker, audio_file)
        transcript_file = (speaker, transcript_file)

        list_of_audio_files.append(audio_file)
        list_of_transcript_files.append(transcript_file)

    return list_of_speakers, list_of_audio_files, list_of_transcript_files, script_file
def example_inputs(): # for testing purposes, to avoid repeatedly entering the same shit over and over
    list_of_speakers = ['andy', 'john', 'narrator']
    list_of_audio_files = ['test\\wav-andy.wav', 'test\\wav-john.wav', 'test\\wav-narrator.wav']
    list_of_transcript_files = ['test\\andy.mp3.word.srt', 'test\\john.mp3.word.srt', 'test\\narrator.mp3.word.srt']
    script_file = 'test\\test-script.txt'

    return list_of_speakers, list_of_audio_files, list_of_transcript_files, script_file

## STAGE 2: CLEAN TEXT
def clean_script(script_file, list_of_speakers):
    # script_file = example.txt

    script_lines_raw = []

    # import all lines to script_lines
    with open(script_file) as f:
        for line in f:
            line = line.strip()
            if line != '':
                script_lines_raw.append(line)

    script_lines_clean = []
    script_lines_clean_with_names = []

    for raw_line in script_lines_raw:

        # name not detected until check later
        name_present = False

        # send line as string clean_line()
        clean_line = clean_lines(raw_line)

        # go through each speaker name
        for speaker in list_of_speakers:
            # if first word of clean_line is speaker name,
            # split clean_line, and join back together everything after the first word
            if clean_line.split(' ')[0] == speaker:
                name_present = True

                clean_line_without_name = ' '.join(clean_line.split(' ')[1:])   # make variable without name
                clean_line_with_name = clean_line                               # make variable with name present

        if name_present == True:
            script_lines_clean.append(clean_line_without_name)              # nameless line  > nameless script, for transcript comparison
            script_lines_clean_with_names.append(clean_line_with_name)      # line with name > named script,    for file sorting
        else:
            script_lines_clean.append(clean_line)
            script_lines_clean_with_names.append(clean_line)

    # script_lines_clean            - all lines with names removed
    # script_lines_clean_with_names - all lines with names remaining
    return script_lines_clean, script_lines_clean_with_names
def clean_transcripts(list_of_speakers, list_of_transcript_files):
    # list_of_speakers         = [name1, name2, ..]
    # list_of_transcript_files = [(name, transcript1.word.srt), (name, transcript2.word.srt), ..]

    # loop through lines in .word.srt file
    # use line_number for loop
    #
    # file lists each word entry like this:
    #
    # 79\n                              <-- line_number = 1
    # 00:00:53,896 --> 00:00:54,197\n   <-- line_number = 2
    # script.\n                         <-- line_number = 3
    # \n                                <-- line_number = 4

    all_transcripts = []

    for speaker in range(len(list_of_speakers)):
        f = open(list_of_transcript_files[speaker][1]).readlines()
        f = check_for_spaces(f)

        # store each list of word details in cleaned_words list
        cleaned_transcript = []

        # set line_number to 0 before starting loop
        line_number = 0
        # word_info = [word, word_start, word_end]
        word_info = []
        for line in f:
            line_number += 1

            line = line.strip()
                
            if line_number == 2:       # timestamps line
                line = line.split(' --> ')
                word_start = line[0]
                word_end = line[1]

            elif line_number == 3:     # word line
                    word = clean_lines(line)

            elif line_number == 4:
                word_info.append(word)
                word_info.append(word_start)
                word_info.append(word_end)

                # add word_info to cleaned_transcript until end of transcript file
                cleaned_transcript.append(word_info)

                word_info = []

                # after 4th line, .srt moves onto next word, so set line_number to 0
                line_number = 0
            
        # add list of transcript words for speaker to collection of all transcripts
        all_transcripts.append(cleaned_transcript)
    
    # all_transcripts    = [[cleaned_transcript1], [cleaned_transcript2], ..]
    # cleaned_transcript = [[word_info1], [word_info2]]
    # word_info          = [word, word_start, word_end]
    return all_transcripts 
def check_for_spaces(transcript): # called by cleaned_transcripts()
    # there are cases when transcription will render "Scene 1" as one word, which isn't recognised
    # therefore I need to split these up into two lines, "Scene" and "1" before continuing cleanup

    # 79\n                              <-- line_number = 1
    # 00:00:53,896 --> 00:00:54,197\n   <-- line_number = 2
    # script.\n                         <-- line_number = 3
    # \n                                <-- line_number = 4

    fixed_transcript = []

    line_number = 0
    for line in transcript:
        line_number += 1

        line = line.strip()

        if line_number == 1:
            number_line = line
        elif line_number == 2:     # timestamps line
            timestamp_line = line
        elif line_number == 3:     # word line
            word_line = line
        elif line_number == 4:
            blank_line = line

            if len(word_line.split()) > 1: # therefore multiple words on line
                for word in word_line.split():
                    fixed_transcript.append(number_line)
                    fixed_transcript.append(timestamp_line)
                    fixed_transcript.append(word)
                    fixed_transcript.append(blank_line)
            else:
                fixed_transcript.append(number_line)
                fixed_transcript.append(timestamp_line)
                fixed_transcript.append(word_line)
                fixed_transcript.append(blank_line)

            # after 4th line, .srt moves onto next word, so set line_number to 0
            line_number = 0

    return fixed_transcript 
def clean_lines(raw_line): # called by clean_script() and clean_transcript()
    # raw_line = string

    clean_line = []
    
    # lowercase
    raw_line = raw_line.lower()

    # for phrases like 8.30 (eight thirty), removing punctuation makes them 830 (eight hundred and thirty)
    raw_line = ' '.join(raw_line.split('.')) # replace all '.' with ' '
    raw_line = re.sub(' +', ' ', raw_line) # reduce all double spaces to single space
    raw_line = raw_line.strip() # remove blank space from end of sentences
    
    # remove all punctuation
    raw_line = re.sub(r'[^\w\s]','', raw_line)

    error = True

    # above, removed all non-alphanumeric characters
    # below, convert all numeric characters and add to cleaned_line
    while error == True:
        raw_line = raw_line.split()
        try:
            if len(raw_line)>0:
                for word in raw_line:
                    if word.isalpha() == False:
                        word = num2words(word)
                    clean_line.append(word)
            else:
                for word in raw_line:
                    if word.isalpha() == False:
                        raw_line = num2words(raw_line)
                        clean_line.append(raw_line)
                    clean_line.append(raw_line)
            error = False
        except:
            print('error at: '+' '.join(raw_line))
            raw_line = input('please correct:\n> ')

    clean_line = ' '.join(clean_line)

    return clean_line

## STAGE 3: FIND MATCHES
def find_matches(script, all_transcripts, list_of_speakers):
    ##      INPUT
    # script           = [line1, line2, ..]
    # list_of_speakers = [speaker1, speaker2, ..]
    #
    # all_transcripts      = [speaker1, speaker2, ..]
    #   speaker_transcript = [[word1], [word2], ...]
    #       word           = [word, word_start, word_end]
    #
    ##      OUTPUT
    # matched_lines           = [[speaker1], [speaker2], ..]
    #   speaker_matches       = [[line1_info], [line2_info], ..]
    #       matched_line_info = ['line_start', 'line_end', line]

    matched_lines = []

    for speaker in range(len(list_of_speakers)):
        transcript = all_transcripts[speaker]

        speaker_matches = compare_script_and_transcript(script, transcript)

        matched_lines.append(speaker_matches)

    return matched_lines
def compare_script_and_transcript(script, transcript): #called by find_matches()
    ##      INPUT
    # script     = [line1, line2, ..]
    # transcript = [[word1], [word2], ...]
    #   word     = [word, word_start, word_end]
    # name       = 'name'
    #
    ##      OUTPUT
    # speaker_matches     = [[line1_info], [line2_info], ..]
    #   matched_line_info = ['line_start', 'line_end', line]
    
    speaker_matches = []

    for script_line in script:
        script_line = script_line.split(' ')

        first_word_in_line = script_line[0]

        line_length = len(script_line)

        position_in_transcript = 0

        transcript_line = []
        for word in transcript:
            current_word_in_transcript = word[0]

            if first_word_in_line == current_word_in_transcript: # possible match found

                for position_from_first_match in range(line_length):
                    
                    try:
                        word = transcript[position_in_transcript + position_from_first_match][0]
                        transcript_line.append(word)
                    except:
                        continue # try/except in case I'm at the end of the file

                    if " ".join(transcript_line) == " ".join(script_line):
                        line = ' '.join(transcript_line)

                        first_word_timestamp = transcript[position_in_transcript][1]
                        last_word_timestamp = transcript[position_in_transcript + line_length-1][2]

                        matched_line = [first_word_timestamp, last_word_timestamp, line]
                        
                        speaker_matches.append(matched_line)
                        transcript_line = [] # reset variable if above succeeds

            transcript_line = [] # reset variable if no match found

            position_in_transcript += 1

    speaker_matches = remove_duplicates(speaker_matches)

    return speaker_matches
def remove_duplicates(matched_lines): # called by compare_script_and_transcript()
    filtered_matched_lines = []

    for line in matched_lines:
        if line not in filtered_matched_lines:
            filtered_matched_lines.append(line)

    return filtered_matched_lines

## STAGE 4: SPLIT AUDIO
def split_audio(list_of_audio_files, list_of_speakers, matched_lines):
    ##      INPUTS
    # list_of_audio_files   = [(name, file1.wav), (name, file2.wav), ..]
    # list_of_speakers      = [name1, name2, ..]
    # matched_lines           = [[speaker1], [speaker2], ..]
    #   speaker_matches       = [[line1_info], [line2_info], ..]
    #       matched_line_info = ['line_start', 'line_end', line]

    ##      OUTPUTS
    # output_folders        = [path\projectname_name1, path\projectname_name2, ..]

    split_audio_output_folders = []

    for speaker in range(len(list_of_speakers)):

        speaker_matches = matched_lines[speaker]            # provides instructions for splitter
        speaker_audio_file = list_of_audio_files[speaker][1]   # provides file names for audio splitting and file naming
        speaker_name = list_of_speakers[speaker]            # provides speaker name for file naming

        line_count = len(speaker_matches)
        file_number_length = len(str(line_count))

        audio_file_name = speaker_audio_file.split('\\')[-1]
        audio_file_name = audio_file_name.split('.')[0]

        # create full destination path for output audio files
        audio_file_path = '\\'.join(speaker_audio_file.split('\\')[:-1])
        if len(list_of_speakers) > 1:
            destination_folder = '-'.join([audio_file_name, speaker_name])
            destination_path = [audio_file_path+'\\'+destination_folder]
        else:
            destination_folder = '-'.join([audio_file_name, "final"])
            destination_path = [audio_file_path+'\\'+destination_folder]

        make_audio_directory(destination_path[0])

        print("\nLoading:", audio_file_name+".wav...")
        audio = AudioSegment.from_wav(speaker_audio_file)
        
        file_number = 1
        for line in speaker_matches:
            audio_start = line[0]
            audio_end = line[1]
            audio_dialogue = line[2]

            audio_start, audio_end = convert_to_milliseconds(audio_start, audio_end)

            audio_chunk = audio[audio_start:audio_end]

            try:
                audio_chunk.export( (destination_path[0]+"\\{}-{}.wav").format(str(file_number).zfill(file_number_length), audio_dialogue), format="wav")
            except:
                print('invalid path:\n> '+(destination_path[0]+"\\{}-{}.wav").format(str(file_number).zfill(file_number_length), audio_dialogue))
            file_number += 1

        file_folder = '\\'.join([audio_file_path, destination_folder])
        split_audio_output_folders.append(file_folder)
    
    return split_audio_output_folders
def make_audio_directory(destination_path):

    try: # remove directory if it's already there before making one
        shutil.rmtree(destination_path)
        os.mkdir(destination_path)
    except: # else just make new directory
        os.mkdir(destination_path)

    # destination_path = folder_path/destination_folder
    return destination_path
def convert_to_milliseconds(audio_start, audio_end): # called by split_audio()

    timestamps = [audio_start, audio_end]

    start = True # for adding buffer to millisecond count, switched to False at end of first loop

    ## timestamp = '00:00:29,174'
    for timestamp in timestamps:
        timestamp = timestamp.split(':')
        seconds_milliseconds = timestamp[2].split(',')

        hours, minutes = int(timestamp[0]), int(timestamp[1])
        seconds, milliseconds = int(seconds_milliseconds[0]), int(seconds_milliseconds[1])

        total_milliseconds = (hours*3600*1000) + (minutes*60*1000) + seconds*1000 + milliseconds

        padding = 300 # number of milliseconds

        if start == True:
            total_milliseconds -= padding   # add padding value to start
            start = False               # set start to False so else runs on next loop
            audio_start = total_milliseconds
        else:
            total_milliseconds += padding   # add padding value to end
            audio_end = total_milliseconds

    return audio_start, audio_end

## STAGE 5: ORGANISE FILES (MULTIPLE SPEAKERS ONLY)
def sort_files(split_audio_output_folders, script_with_names):
    ## INPUTS
    # script_with_names          = ['name-and-line', 'name2-and-line2', ..]
    # split_audio_output_folders = [path\projectfolder1, path\projectfolder1, ..]

    all_files = get_files(split_audio_output_folders)
    destination_path = make_final_directory(split_audio_output_folders)
    sorting_instructions = get_instructions(script_with_names)
    
    find_and_move_files(all_files, destination_path, sorting_instructions)
def get_files(split_audio_output_folders):  # called in sort_files(), return all_files
    # split_audio_output_folders = [path\projectfolder1, path\projectfolder1, ..]

    all_files = []
    
    for folder in split_audio_output_folders:
        list_of_files = os.listdir(folder)
        list_of_files = (folder, list_of_files)
        all_files.append(list_of_files)

    # all_files = [(path\projectfolder1, [file1, file2, ..]), (path\projectfolder1, [file1, file2, ..])]
    return all_files
def make_final_directory(split_audio_output_folders): # called in sort_files(), return destination_path
    # split_audio_output_folders = [path\projectfolder1, path\projectfolder1, ..]
    #                          ie. [project_path\speaker_folder, ..]

    # isolate folder path for all speaker audio file folders
    folder_path = split_audio_output_folders[0]                 #project_path\speaker_folder\ (speaker_folder = 'projectname-speaker')
    folder_path = '\\'.join(folder_path.split('\\')[:-1])       #project_path\

    # get folder name for final
    destination_folder = folder_path.split('\\')[-1]                   # 'projectname-speaker'
    destination_folder = folder_path.split('\\')[0]                    # 'projectname'

    # create new directory for sorting files
    destination_path = os.path.join(folder_path, 'final', destination_folder)
    try: # remove directory if it's already there before making one
        shutil.rmtree(destination_path)
        os.mkdir(destination_path)
    except: # else just make new directory
        os.mkdir(destination_path)

    # destination_path = folder_path/destination_folder
    return destination_path
def get_instructions(script_with_names): # called in sort_files(), return sorting_instructions
    sorting_instructions = []

    for line in script_with_names:
        # split line into words
        line = line.strip().split(' ')
        
        # get first word as name
        name = line[0]
        # get remainder of words as line
        line = ' '.join(line[1:])

        #make line into tuple
        line = (name, line)

        # add tuple to list
        sorting_instructions.append(line)
    
    # sorting_instructions = [(name1, line1), (name2, line2), (name1, line3), (name2, line4), ..]
    return sorting_instructions
def find_and_move_files(all_files, destination_path, sorting_instructions): #called in sort_files()
    # all_files = [(path\projectfolder1, [file1, file2, ..]), (path\projectfolder1, [file1, file2, ..])]
    #   projectfolder = 'projectname-speakername
    # destination_path      = folder_path/destination_folder
    # sorting_instructions = [(name1, line1), (name2, line2), (name1, line3), (name2, line4), ..]

    # source file path format (audio_file_path+'/'+destination_folder+"/{}-{}.wav").format(file_number, audio_dialogue)

    file_number = 0000

    # line = (name, line)
    for line in sorting_instructions:
        script_name, script_line = line[0], line[1]

        # speaker = (path, [list of files])
        for speaker in all_files:
            # get path\\projectname-(speakername) < extract name from file after '-'
            speaker_name = speaker[0].split('-')[-1]

            # speaker_files = [filepath1, filepath2, ..]
            speaker_file_path = speaker[0]
            speaker_files = speaker[1]
            if script_name == speaker_name:
                for file_location in speaker_files: # iterate through source files in source directory
                    file_name = file_location.split('\\')[-1]                    # extract file name from path
                    file_line = (file_name.split('-')[1]).split('.')[0] # extract dialogue line from file name
                    file_location = speaker_file_path+'\\'+file_location
                    if file_line.strip() == script_line.strip():
                        file_number += 1
                        move_file(file_number, destination_path, file_location, file_name)
            else:
                continue
    
    #remove empty directories after moving is done
    try:
        for file_directory in all_files:
            os.rmdir(file_directory)
        exit
    except:
        exit
def move_file(file_number, destination_path, file_location, file_name): # called in find_and_move_files()
    try:
        file_destination = destination_path + '\\' + str(file_number).zfill(4) +'-'+ file_name
        os.rename(file_location, file_destination)
    except:
        print('file not found:\n> '+file_destination)

def main():
    ## STAGE 1: GET INPUTS
    # list_of_speakers          = [name1, name2, ..]                note: speaker name 'narrator' by default
    # list_of_audio_files       = [file1.wav, file2.wav, ..]
    # list_of_transcript_files  = [file1.word.srt, file2.word.srt, ..]
    # script_file               = 'file.txt'
    list_of_speakers, list_of_audio_files, list_of_transcript_files, script_file = get_all_inputs()
    #list_of_speakers, list_of_audio_files, list_of_transcript_files, script_file = example_inputs()

    ## STAGE 2: CLEAN TEXT
    # script            = [line1, line2, ..]
    script, script_with_names = clean_script(script_file, list_of_speakers)
    # all_transcripts   = [speaker1, speaker2, ..]
       #speaker         = [[word1], [word2], ...]
       #word            = [word, word_start, word_end]
    all_transcripts = clean_transcripts(list_of_speakers, list_of_transcript_files)

    ## STAGE 3: FIND MATCHES
    ##      MATCH LINES IN SCRIPT / TRANSCRIPTS
    # matched_lines     = [[speaker1], [speaker2], ..]
       #speaker         = [[line1_info], [line2_info], ..]
       #line_info       = ['line_start', 'line_end', line]
    matched_lines = find_matches(script, all_transcripts, list_of_speakers)

    ## STAGE 4: SPLIT AUDIO
    split_audio_output_folders = split_audio(list_of_audio_files, list_of_speakers, matched_lines)

    ## STAGE 5: ORGANISE FILES (MULTIPLE SPEAKERS ONLY)
    if len(list_of_speakers) > 1: # check for multiple speakers
        sort_files(split_audio_output_folders, script_with_names)

main()