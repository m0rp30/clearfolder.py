from time import sleep, strftime
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from os import mkdir, path, rename, stat
from ntpath import basename
import filetype
from filetype import guess_extension, guess_mime

class Watcher:
    DIRECTORY_TO_WATCH = "/home/luca/prova/"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            while True:
                sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        destination = "/home/luca/prova/dest/"
        filename = event.src_path

        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print(f"Received created event  {filename}")
            # Get file extension, mime and more
            file_guess_mime = guess_mime(filename)
            file_guess_extension = guess_extension(filename)
            # Set filetype if not match set to None
            if file_guess_mime is None:
                file_type = "None"
            else:
                file_guess_mime_split = file_guess_mime.split("/")
                file_type = str(file_guess_mime_split[0]).capitalize()
            # Separate filename to extension if non extension put extension from filetype
            filename_split = basename(filename).split(".")
            try:
                if len(filename_split) > 1:
                    file_extension = filename_split[-1]
                else:
                    file_extension = filename_split[1]
            except IndexError:
                if file_extension is None:
                    file_extension = filename_split.append("noname")
                else:
                    file_extension = filename_split.append(file_guess_extension)
            # Get current file Year
            modification_time = stat(filename).st_mtime
            # year = strftime("%Y") # Use this line if you want a current year
            year = datetime.fromtimestamp(modification_time).strftime('%Y')
            # Get current file Month
            # month = strftime("%m") # Use this line if you want a current month
            month = datetime.fromtimestamp(modification_time).strftime('%m')

            if not path.exists(destination + "/" + year):
                mkdir(destination + "/" + year)
            if not path.exists(destination + "/" + year + "/" + month):
                mkdir(destination + "/" + year + "/" + month)
            if not path.exists(destination + "/" + year + "/" + month + "/" + file_type):
                mkdir(destination + "/" + year + "/" + month + "/" + file_type)

            destination = destination + "/" + year + "/" + month + "/" + file_type

            new_name = destination + "/" + filename_split[0] + "." + file_extension
            i = 0
            while path.exists(new_name):
                i += 1
                new_name = destination + "/" + filename_split[0] + str(i) + "." + file_extension
                print(new_name)
            # Move file event.src_path in to destination ex. {year}/{month}/{basename(event.src_path)}


if __name__ == '__main__':
    w = Watcher()
    w.run()