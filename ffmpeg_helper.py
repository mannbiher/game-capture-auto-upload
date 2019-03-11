import subprocess
import logging
from upload_exceptions import FfmpegFileError

logger = logging.getLogger(__name__)


def create_thumbnails(video_file, folder):
    """ Creates thumbnails from video."""
    outfile = f'{folder}//out%02d.jpg'
    ffmpeg_args = ['ffmpeg',
                   # skip first 60 seconds
                   '-ss', '60',
                   '-i', video_file,
                   '-frames:v', '5',
                   '-vsync', 'vfr',
                   # one snapshot per minute of video
                   '-vf', 'fps=1/60',
                   outfile]
    process = subprocess.run(ffmpeg_args, capture_output=True)

    if process.returncode != 0:
        if process.stderr:
            logger.error(process.stderr)
        else:
            logger.error(process.stdout)
        raise RuntimeError('Ffmpeg failed to create thumbnails.')


def insert_watermark(input_file, out_file, image_path):
    """ Insert watermark on video."""
    ffmpeg_args = ['ffmpeg',
                   '-i', input_file,
                   '-i', image_path,
                   '-filter_complex', 'overlay=10:10',
                   '-crf', '18',
                   '-y', out_file]
    process = subprocess.run(ffmpeg_args, capture_output=True)

    if process.returncode != 0:
        if process.stderr:
            logger.debug(process.stderr)
        else:
            logger.debug(process.stdout)
        raise FfmpegFileError('Input file cannot be processed.')
