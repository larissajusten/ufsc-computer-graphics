from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time
import os
import signal

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, filename):
        self.filename = filename
        self.process = None
        self.start_script()

    def start_script(self):
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
        print("\n🔁 Reiniciando script...\n")
        self.process = subprocess.Popen(["python", self.filename])

    def on_modified(self, event):
        if event.src_path.endswith(self.filename):
            self.start_script()

if __name__ == "__main__":
    filename = "main.py" 
    event_handler = ReloadHandler(filename)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
