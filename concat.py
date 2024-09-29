import subprocess
import sys
import os
import re

output_name = sys.argv[1]

def extract_number(filename):
    match = re.search(r'(\d+)', filename)
    return int(match.group(0)) if match else 0

parts = os.listdir("temp")
parts = sorted(parts, key=extract_number)

playlist = [f"file '{os.getcwd()}/temp/{part}'\n".replace('\\', '/') for part in parts]

print(playlist)

with open('playlist.txt', 'w') as output:
    output.writelines(playlist)

print(os.getcwd())
subprocess.run(["ffmpeg", 
                "-f", "concat",
                "-safe", "0", 
                "-i", "playlist.txt", 
                "-c", "copy", f"{output_name}"
                ])