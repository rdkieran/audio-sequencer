# for formatting .txt script files for comparison against converted .srt files
# removes all non ascii characters, removes all punctuation, converts all uppercase, and converts all non-alpha characters
# .docx files should be exported from word processor as .txt files beforehand

import re
from num2words import num2words

# write contents of .docx.txt file to 'script' string
# also removes non ascii characters
def get_script(script_file):
    script = ""
    with open(script_file) as f:
        for line in f:
            if line.strip != '':
                line = ''.join(char for char in line if ord(char) < 128) ## remove non ascii characters
                script = '\n'.join([script, line.strip().lower()]) ## forces lowercase and adds to script string

    return script

# remove all punctuation from 'script' string
def remove_punctuation(script):
    script = ' '.join(script.split('.')) ## '8.30' to '8 30', not '830'
    script = re.sub(' +', ' ', script)
    script = re.sub(r'[^\w\s]','', script)
    script = re.sub(r'\n\s*\n', '\n', script)
    
    return script

# iterates through each word in each line and converts any instance of numbers (1) to words (one)
# returns script as list of lists
def numbers_to_words(script):
    new_line = ''
    final_lines = ''
    
    skip_line = True

    for line in script.split('\n'):
        if skip_line == False:
            for word in line.strip().split(' '):
                if word.isalpha() == False:
                    word = num2words(word)
                new_line = ' '.join([new_line, word])
            final_lines = '\n'.join([final_lines, new_line.strip()])
            new_line = ''
        else:
            skip_line = False
            
    return final_lines.strip()

def write_file(script, filename):
    with open(filename, "w") as f:
        f.write(script)

def main():
    script_file = input("Script file: ")
    script_out = script_file.split('.')[0]+'-CLEAN.txt'

    script = get_script(script_file)
    script = remove_punctuation(script)
    script = numbers_to_words(script) # returns script as list of lists

    write_file(script, script_out)

main()