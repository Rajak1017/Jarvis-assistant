import subprocess
import datetime
import os

def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    
    # Save the note text to a file
    with open(file_name, "w") as f:
        f.write(text)
    
    # Define Notepad++ path or fallback to default Notepad
    notepad_path = "C:\\Program Files (x86)\\Notepad++\\notepad++.exe"
    
    # Check if Notepad++ exists; otherwise, use Notepad
    if os.path.exists(notepad_path):
        subprocess.Popen([notepad_path, file_name])
    else:
        # Use default Notepad if Notepad++ is not available
        subprocess.Popen(["notepad.exe", file_name])
