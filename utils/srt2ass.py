import os
import re
import codecs
from utils.colorPrint import *

def fileopen(input_file):
    encodings = ["utf-32", "utf-16", "utf-8", "cp1252", "gb2312", "gbk", "big5"]
    tmp = ''
    for enc in encodings:
        try:
            with codecs.open(input_file, mode="r", encoding=enc) as fd:
                tmp = fd.read()
                break
        except Exception:
            continue
    return [tmp, enc]

def convert_color_to_ass_format(hex_color):
    rgb_color = hex_color.lstrip('#')
    bgr_color = rgb_color[4:6] + rgb_color[2:4] + rgb_color[0:2]
    return f"&H00{bgr_color.upper()}"

def srt2ass(input_file, font='Arial', font_size=20, color='FFFFFF'):
    if '.ass' in input_file:
        return input_file

    if not os.path.isfile(input_file):
        error(input_file + ' does not exist')
        exit()

    src = fileopen(input_file)
    tmp = src[0]
    encoding = src[1]

    utf8bom = ''
    if u'\ufeff' in tmp:
        tmp = tmp.replace(u'\ufeff', '')
        utf8bom = u'\ufeff'

    tmp = tmp.replace("\r", "")
    lines = [x.strip() for x in tmp.split("\n") if x.strip()]

    subLines = ''
    tmpLines = ''
    lineCount = 0
    
    output_file = os.path.splitext(input_file)[0] + '.ass'

    for ln in range(len(lines)):
        line = lines[ln]
        if line.isdigit() and re.match(r'-?\d\d:\d\d:\d\d', lines[(ln + 1)]):
            if tmpLines:
                subLines += tmpLines + "\n"
            tmpLines = ''
            lineCount = 0
            continue
        else:
            if re.match(r'-?\d\d:\d\d:\d\d', line):
                line = line.replace('-0', '0')
                tmpLines += 'Dialogue: 0,' + line + ',SubStyle,,0,0,0,,'
            else:
                if lineCount < 2:
                    tmpLines += line
                else:
                    tmpLines += "\n" + line
            lineCount += 1

    subLines += tmpLines + "\n"

    subLines = re.sub(r'\d(\d:\d{2}:\d{2}),(\d{2})\d', r'\1.\2', subLines)
    subLines = re.sub(r'\s+-->\s+', ',', subLines)

    subLines = re.sub(r'<([ubi])>', r"{\\\g<1>1}", subLines)
    subLines = re.sub(r'</([ubi])>', r"{\\\g<1>0}", subLines)
    subLines = re.sub(r'<font\s+color="?#(\w{2})(\w{2})(\w{2})"?>', r"{\\c&H\3\2\1&}", subLines)
    subLines = re.sub(r'</font>', "", subLines)

    head_str = f'''[Script Info]
Title: Custom Subtitles
Original Script: User
ScriptType: v4.00
Collisions: Normal
PlayDepth: 0
[V4 Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding
Style: Default,{font},{font_size},{convert_color_to_ass_format(color)},0,0,0,-1,0,1,1.0,0.0,2,10,10,10,0,1
[Events]
Format: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text'''

    output_str = utf8bom + head_str + '\n' + subLines
    output_str = output_str.encode(encoding)

    with open(output_file, 'wb') as output:
        output.write(output_str)

    output_file = output_file.replace('\\', '\\\\').replace('/', '//')
    os.remove(input_file)
    return output_file
