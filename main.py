import time
import sys
from collections import namedtuple
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from process_video import Processor
import file_operations


def process_file(folder):
    video_processor = Processor()
    files = file_operations.get_files_by_modified_date(folder)
    event = namedtuple('event', ['src_path'])
    for file_ in files:
        event.src_path = file_
        video_processor.on_modified(event)


if __name__ == '__main__':
    args = sys.argv[1:]
    folder = args[0]

    while True:
        process_file(folder)
        time.sleep(300)

    # observer = Observer()
    # observer.schedule(
    #     Processor(),
    #     path=args[0] if args else '.',
    #     recursive=True)
    # observer.start()

    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     observer.stop()

    # # observer.join()
