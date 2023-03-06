from pydub import AudioSegment
import os

def get_speaker_names(number_of_speakers):
    list_of_speakers = []
    for speaker in range(int(number_of_speakers)):
        print("\nSpeaker No."+str(speaker+1)+" name:")
        speaker_name = input().lower()
        list_of_speakers.append(speaker_name)
    return list_of_speakers

def get_timestamps(transcript_file):
    all_timestamps = []
    with open(transcript_file) as transcript:
        for line in transcript:
            line = line.strip().split(' --- ')
            line_start = line[0]
            line_end = line[1]

            start = True ## define start / end to determine cropping of file (+/-250ms)
            line_start = convert_to_seconds(line_start, start)
            start = False
            line_end = convert_to_seconds(line_end, start)

            just_line = line[2]

            line_timestamp = [line_start,line_end,just_line]
            all_timestamps.append(line_timestamp)
    return all_timestamps

def convert_to_seconds(timestamp, start):
    ## timestamp = '00:00:29,174'
    hours_minutes = timestamp.split(':')
    seconds_milliseconds = hours_minutes[2].split(',')

    hours = int(timestamp[0])
    minutes = int(timestamp[1])
    seconds = int(seconds_milliseconds[0])
    milliseconds = int(seconds_milliseconds[1])

    if start == False:
        total_milliseconds = (hours*3600*1000) + (minutes*60*1000) + seconds*1000 + milliseconds + 250
    if start == True:
        total_milliseconds = (hours*3600*1000) + (minutes*60*1000) + seconds*1000 + milliseconds - 250

    return total_milliseconds

def make_directory(audio_file, speaker):
    audio_file_split = audio_file.split('\\')

    ## get file name
    audio_file_name = audio_file_split[len(audio_file_split)-1:][0]
    audio_file_name = audio_file_name.split('.')[0] ## get rid of file extension

    ## get file path
    audio_file_path = '\\'.join(audio_file_split[:len(audio_file_split)-1])

    ## get destination folder
    if speaker != '':
        destination_folder = speaker+'--'+audio_file_name
    else:
        destination_folder = audio_file_name

    dir = os.path.join(audio_file_path, destination_folder)
    os.mkdir(dir)

    return audio_file_name, audio_file_path, destination_folder

def split_audio(all_timestamps, audio_file, audio_file_name, audio_file_path, destination_folder):
    line_count = len(all_timestamps)
    digit_length = len(str(line_count))

    print("\nLoading:", audio_file_name+"...")
    audio = AudioSegment.from_wav(audio_file)

    for file_number in range(line_count):
        audio_start = all_timestamps[file_number][0]
        audio_end = all_timestamps[file_number][1]
        line = all_timestamps[file_number][2]

        file_number = str(file_number).zfill(digit_length)
        print(str(int(file_number)+1),"of",str(line_count))

        audio_chunk = audio[audio_start:audio_end]
        audio_chunk.export( (audio_file_path+'/'+destination_folder+"/{}-{}.wav").format(file_number, line), format="wav")

def main():
    speaker_ask = input("\nAre there multiple speakers? (Y/N): ").lower()
    if speaker_ask.startswith('y') == True:
        number_of_speakers = input("How many speakers?: ")
        list_of_speakers = get_speaker_names(number_of_speakers)
    else:
        list_of_speakers = ['']

    for speaker in list_of_speakers:
        if speaker != '':
            print("\n------\nSpeaker: "+speaker.capitalize())

        transcript_file = input("\nTranscript file: ")

        audio_file = input("Audio file: ")
        audio_file_name, audio_file_path, destination_folder = make_directory(audio_file, speaker)
    
        all_timestamps = get_timestamps(transcript_file)
        split_audio(all_timestamps, audio_file, audio_file_name, audio_file_path, destination_folder)

main()