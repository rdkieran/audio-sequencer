def get_speaker_names(number_of_speakers):
    list_of_speakers = []
    for speaker in range(int(number_of_speakers)):
        print("\nSpeaker No."+str(speaker+1)+" name:")
        speaker_name = input().lower()
        list_of_speakers.append(speaker_name)
    return list_of_speakers

def get_listed_transcript(transcript_file):
    word_info = []
    list_of_words = []
    line_loop = 0

    with open(transcript_file) as f:
        for line in f.readlines():
            line_loop += 1

            if line_loop == 1:
                word_start = line.strip()[:12]
                word_end = line.strip()[17:]

            elif line_loop == 2:
                word = line.strip().lower()
                
                word_info.append(word)
                word_info.append(word_start)
                word_info.append(word_end)

                list_of_words.append(word_info)

                word_info = []
                line_loop = 0

    return list_of_words

def get_listed_script(script_file):
    script_lines = []

    with open(script_file) as f:
        for line in f:
            script_lines.append(line.strip().split(' '))
    
    return script_lines

def compare_transcript_and_script(script, transcript, name):

    matched_lines = [] #list of matched lines with timestamps
    transcript_line = []

    for script_line in script:
        if script_line[0] == name:
            script_line = script_line[1:]

            line_length = len(script_line)
            first_word_in_line = script_line[0]

            position_in_transcript = 0
            for word_info in transcript:
                word_in_transcript = word_info[0]
                if word_in_transcript == first_word_in_line:

                    for position_from_first_match in range(line_length):
                        try:
                            word = transcript[position_in_transcript + position_from_first_match][0]
                            transcript_line.append(word)
                        except:
                            continue ## try/except in case I'm at the end of the file
                        
                    if " ".join(transcript_line) == " ".join(script_line):
                        line = ' '.join(transcript_line)
                        first_word_timestamp = transcript[position_in_transcript][1]
                        last_word_timestamp = transcript[position_in_transcript + line_length-1][2]
                        matched_line = [first_word_timestamp, last_word_timestamp, line]
                        #print(matched_line)
                        matched_lines.append(' --- '.join(matched_line))
                    
                    transcript_line = []
                position_in_transcript += 1

    return matched_lines

def remove_duplicates(matched_lines):
    filtered_matched_lines = []

    for line in matched_lines:
        if line not in filtered_matched_lines:
            filtered_matched_lines.append(line)

    return filtered_matched_lines

def write_to_file(matched_lines, name, script_file):
    if name != '':
        output_file = '\\'.join(script_file.split('\\')[:-1])+'\\'+ name+ "-transcript.txt"
    else:
        output_file = '\\'.join(script_file.split('\\')[:-1])+'\\'+ name+ "transcript.txt"

    with open(output_file, "w") as f:
        f.write('\n'.join(matched_lines))

def main():
    script_file = input("Script file: ")
    
    speaker_ask = input("\nAre there multiple speakers? (Y/N): ").lower()
    if speaker_ask.startswith('y') == True:
        number_of_speakers = input("How many speakers?: ")
        list_of_speakers = get_speaker_names(number_of_speakers)
    else:
        list_of_speakers = ['']

    for name in list_of_speakers:
        if name != '':              # therefore multiple speakers
            print("\nSpeaker:",name.capitalize())
        transcript_file = input("Transcript file: ")
    
        transcript = get_listed_transcript(transcript_file)
        script = get_listed_script(script_file)
        matched_lines = compare_transcript_and_script(script, transcript, name)
        matched_lines = remove_duplicates(matched_lines)
        write_to_file(matched_lines, name, script_file)
main()