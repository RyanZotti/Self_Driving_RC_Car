import numpy as np
import cv2
import re
import os
from datetime import datetime

# example: python read_camera_file.py -f /Users/ryanzotti/Documents/repos/OpenCV_examples/output.mov

def dataprep(data_path):

    cap = cv2.VideoCapture(data_path+"/output.mov")

    video_timestamps = []
    with open(data_path+'/video_timestamps.txt') as video_timestamps_reader:
        for line in video_timestamps_reader:
            line = line.replace("\n","")
            ts = datetime.strptime(line, '%Y-%m-%d %H:%M:%S.%f')
            video_timestamps.append(ts)

    commands = []
    with open(data_path+'/clean_session.txt') as clean_session_reader:
        for line in clean_session_reader:
            line = line.replace("\n","")
            match = re.match(r"^.*\['(.*)'\].*$",line)
            if match is not None:
                command = match.group(1)
            else:
                command = 'no command'
            raw_ts = line[line.index(" ")+1:]
            ts = datetime.strptime(raw_ts, '%Y-%m-%d %H:%M:%S.%f')
            commands.append([command,ts])

    # time after which no other data is relevant because driving session has ended
    end_time = commands[len(commands)-1][1]

    # cleanup to track only command transitions
    compact_commands = []
    prev_command = None
    for item in commands:
        command, ts = item[0], item[1]
        if command != prev_command and command != 'no command':
            compact_commands.append([command,ts])
            prev_command = command
    commands = compact_commands

    # time before which no other data is relevant because driving session just started
    start_time = commands[0][1]

    current_command = commands[0][0]
    command_counter = 1
    future_command = commands[command_counter][0]
    future_command_ts = commands[command_counter][1]

    predictors = []
    target = []

    frame_counter = -1
    while(cap.isOpened()):
        frame_counter = frame_counter + 1
        ret, frame = cap.read()
        if cv2.waitKey(1) & 0xFF == ord('q'): # don't remove this if statement or video feed will die
            break
        video_timestamp = video_timestamps[frame_counter]
        if video_timestamp > start_time:
            if video_timestamp < end_time:
                #print(frame.shape)
                if video_timestamp > future_command_ts:
                    current_command = future_command
                    command_counter = command_counter + 1
                    if command_counter < len(commands):
                        future_command = commands[command_counter][0]
                        future_command_ts = commands[command_counter][1]
                    else:
                        future_command = "END"
                        future_command_ts = end_time
                    print(current_command)
                cv2.imshow('frame',frame)
                predictors.append(frame)
                target.append(current_command)
            else:
                cap.release()
                cv2.destroyAllWindows()


if __name__ == '__main__':
    data_path = str(os.path.dirname(os.path.realpath(__file__))) + "/data/1/"
    dataprep(data_path)