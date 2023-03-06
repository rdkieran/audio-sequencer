## cleans up .word.srt transcript, making it faster to parse later

import re
from num2words import num2words

def fix_srt(srt_file):
    x = 0
    final_lines = []
    with open(srt_file) as f:
        for line in f.readlines():
            line = line.lower().strip()
            x += 1
            if x == 2:
                timestamp = line
            elif x == 3:
                line = re.sub(r'[^\w\s]','',line)
                if " " in line:
                    word_one = line.split()[0]
                    word_two = line.split()[1]

                    if word_one.isalpha() == False:
                        word_one = num2words(word_one)
                    if word_two.isalpha() == False:
                        word_two = num2words(word_two)

                    final_lines.append(timestamp)
                    final_lines.append(word_one)
                    final_lines.append(timestamp)
                    final_lines.append(word_two)
                else:
                    if line.isalpha() == False:
                        line = num2words(line)
                    final_lines.append(timestamp)
                    final_lines.append(line)
            elif x == 4:
                x = 0
            else:
                continue

    srt_file = srt_file.split('.')
    new_file_name = srt_file[0]+'-CLEAN.'+srt_file[-1]

    with open(new_file_name, "w") as f:
        for line in final_lines:
            f.write(line.strip())
            f.write("\n")

def main():
    srt_file = input(".srt transcript file: ")
    fix_srt(srt_file)

main()