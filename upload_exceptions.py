class VideoUploadError(Exception):
    pass


class FfmpegFileError(VideoUploadError):
    """ Raise this error if input file cannot be transcoded."""
