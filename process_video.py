import os
import shutil
import logging
import subprocess
from datetime import datetime, timedelta
import psutil
from watchdog.events import PatternMatchingEventHandler
import ffmpeg_helper
import image_helper
import file_operations
import upload
from upload_exceptions import FfmpegFileError


processed_files = {}
OUT_DIR = "D:\\Gaming\\Capture"
IMAGE_PATH = "C:\\Users\\neha\\Pictures\\game manthan extra small.png"
FORMAT = '%(asctime)-s - %(name)s:%(lineno)d - %(levelname)s - %(message)s'
LOGO_FILE = 'Thumb_Nail_Front.png'

logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)


def get_out_path(folder, orig_file):
    """ Get output filename from input."""
    file_name, extension = os.path.splitext(orig_file)
    outfile = file_name + "_wm"
    return f'{OUT_DIR}\\{folder}\\{outfile}{extension}'


def get_thumbnail_folder(folder, orig_file):
    """ Get folder to save thumbnails."""
    file_name, extension = os.path.splitext(orig_file)
    return f'{OUT_DIR}\\{folder}\\{file_name}'


def add_suffix_filename(file_path, suffix):
    """ Add suffix in filename."""
    full_file_name = os.path.basename(file_path)
    dir_name = os.path.dirname(file_path)
    file_name, extension = os.path.splitext(full_file_name)
    outfile = file_name + suffix + extension
    return os.path.join(dir_name, outfile)


def is_locked(orig_file):
    try:
        os.rename(orig_file, orig_file)
    except OSError:
        return True
    return False


def create_thumbnail(folder, input_file):
    """ Create thumbnails from video file."""
    file_name = os.path.basename(input_file)
    thumbnail_folder = get_thumbnail_folder(folder, file_name)
    os.makedirs(thumbnail_folder, exist_ok=True)

    ffmpeg_helper.create_thumbnails(input_file, thumbnail_folder)

    largest_files = file_operations.get_largest_files(
        thumbnail_folder, count=5)

    for image_file in largest_files:
        image_out = add_suffix_filename(image_file, '_tm')
        image_helper.create_thumbnail(
            image_file, LOGO_FILE, image_out)

    thumbnail = file_operations.get_random_largest_file(
        thumbnail_folder, '_tm')

    return thumbnail


# def is_locked(orig_file):
#     five_minutes_before = datetime.now() - timedelta(minutes=5)
#     file_stats = os.stat(orig_file)
#     size = file_stats.st_size
#     last_modified = file_stats.st_mtime

#     if orig_file in cache:
#         if (cache[orig_file]['Size'] == size
#                 and last_modified < five_minutes_before):
#             return False
#     else:
#         cache[orig_file] = {'Size': size}

#     return True


class Processor(PatternMatchingEventHandler):
    patterns = ["*.mp4"]

    def process(self, event):
        input_file = event.src_path
        folder = datetime.today().strftime('%Y-%m-%d')
        orig_file = os.path.basename(input_file)
        out_orig = f'{OUT_DIR}\\{folder}\\{orig_file}'
        out_file = get_out_path(folder, orig_file)
        os.makedirs(os.path.dirname(out_file), exist_ok=True)

        try:
            ffmpeg_helper.insert_watermark(input_file,
                                           out_file, IMAGE_PATH)
        except FfmpegFileError:
            logger.info('Failed to decode input file %s', orig_file)
            return

        logger.info('%s is processed.', orig_file)

        # 20 category is Gaming
        tags = 'residentevil2,2019,pc,hd,resident,evil,claire'
        video_id = upload.upload_file(out_file,
                                      orig_file,
                                      category='20',
                                      keywords=tags)

        logger.info('video %s upload for %s', video_id, orig_file)

        # thumbnail = create_thumbnail(folder, input_file)
        # logger.info('Thumbnails created for %s.', orig_file)
        # upload.upload_thumbnail(video_id, thumbnail)
        # logger.info('Thumbnail set for video %s', video_id)

        try:
            # move source file to
            shutil.move(input_file, out_orig)
        except (PermissionError, FileNotFoundError):
            logger.error('Could not move file %s. Ignoring event.', orig_file)
            return

        logger.info('%s moved to D drive', orig_file)

    # def on_created(self, event):
    #     self.process(event)

    def on_modified(self, event):
        if is_locked(event.src_path):
            logger.info('%s is locked for editing.', event.src_path)
        else:
            self.process(event)
