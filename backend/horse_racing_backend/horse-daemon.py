import os
import sys
from datetime import datetime
import subprocess
import time

def runStream():
    
    while True:
        process = subprocess.Popen ("/usr/bin/python3 ./stream.py", shell=True)
        time.sleep (120)
        process.kill ()

runStream ()