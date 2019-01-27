import time
import sys
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from process_video import Processor


if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(
        Processor(), 
        path=args[0] if args else '.',
        recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
