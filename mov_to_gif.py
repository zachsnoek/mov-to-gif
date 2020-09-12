import os
import sys
import subprocess
import time
import imageio
from pygifsicle import optimize
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

WATCH_DIR = ""


def watcher(path):
    event_handler = LoggingEventHandler()
    event_handler.on_created = on_created

    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        print("mov_to_gif is watching {}\n".format(WATCH_DIR))

        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


def on_created(event):
    if event.src_path.endswith(".mov"):
        input_path = event.src_path
        output_path = os.path.splitext(input_path)[0] + ".gif"

        print("Converting:\t{}\nTo:\t\t{}\n".format(input_path, output_path))

        mov_to_gif(input_path, output_path)

        print("\n\nOptimizing gif...")
        optimize(output_path)

        print("\nDone.")
        subprocess.call(["open", "-R", output_path])


def mov_to_gif(input_path, output_path):
    reader = imageio.get_reader(input_path)
    fps = reader.get_meta_data()['fps']

    writer = imageio.get_writer(output_path, fps=fps)

    for i, im in enumerate(reader):
        if i % 2 == 0:
            sys.stdout.write("\rWriting frame: {0}".format(i))
            sys.stdout.flush()
            writer.append_data(im)

    writer.close()


if __name__ == "__main__":
    watcher(WATCH_DIR)