import whisper
from utils.menu import menu
from utils.colorPrint import *
from prompt_toolkit import prompt

def format_time_srt(seconds, flag):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if flag:
        milliseconds = int((seconds - int(seconds)) * 100)
        if hours == 0 and minutes == 0:
            return f"{secs:02}.{milliseconds:02}"
        elif hours == 0:
            return f"{minutes:02}:{secs:02}.{milliseconds:02}"
        else:
            return f"{hours:02}:{minutes:02}:{secs:02}.{milliseconds:02}"
    else:
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"


def  edit(start_time_list,end_time_list,texts):
    while True:
        options = [f"{start_time} - {end_time} : {text}" for start_time,end_time,text in zip(start_time_list,end_time_list,texts)]+['Confirm Changes']
        ch = menu("Choose Line to edit",options)
        if ch == -1:
            continue
        elif ch == len(options):
            return start_time_list,end_time_list,texts,1
        elif ch == len(options)+1:
            return start_time_list,end_time_list,texts,0
        else:
            edited_text = prompt(f"{start_time_list[ch-1]} - {end_time_list[ch-1]} Edit Text: ",default=texts[ch-1])
            texts[ch-1] = edited_text

def speech_to_text(file,srt_file):
    try:
        with open(srt_file, "w", encoding="utf-8") as srt_file:
            model = whisper.load_model("base")
            result = model.transcribe(file)
            print("\n")
            start_time_list = []
            end_time_list = []
            texts = []
            for segment in result['segments']:
                start_time_list.append(round(segment['start'],2))
                end_time_list.append(round(segment['end'],2))
                texts.append(segment['text'])
                
            while True:
                print("Generated Text:\n")
                for i,value in enumerate(zip(start_time_list,end_time_list,texts),start=1):
                    print(f"{i}: {format_time_srt(value[0],1)} - {format_time_srt(value[1],1)} : {value[2]}")
                ch = input("\nDo You Want To Edit The Lines [y/n] ? ").lower()
                if ch == 'y':
                    start_time_list,end_time_list,texts,flag = edit(start_time_list,end_time_list,texts)
                    if flag:
                        break
                    else:
                        continue
                elif ch == 'n':
                    break
                else:
                    error("INVAID INPUT!")
                    continue
            for i,value in enumerate(zip(start_time_list,end_time_list,texts),start=1):
                srt_file.write(f"{i}\n")
                srt_file.write(f"{format_time_srt(value[0],0)} --> {format_time_srt(value[1],0)}\n")
                srt_file.write(f"{value[2]}\n\n")
    except Exception as e:
        error(f"An Error Occured:\n\n{e}")
        exit()