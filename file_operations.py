import os
from random import shuffle


def get_largest_files(folder, count=None):
    """ Returns largest files in folder."""
    all_files = (
        os.path.join(basedir, filename)
        for basedir, dirs, files in os.walk(folder)
        for filename in files)
    sorted_files = sorted(all_files, key=os.path.getsize, reverse=True)
    if count:
        return sorted_files[:count]
    return sorted_files


def get_random_largest_file(folder, filter):
    """ Get random largest file."""
    files = get_largest_files(folder)
    filtered_files = [file_ for file_ in files if filter in files]
    shuffle(filtered_files)
    return filtered_files[0]


def get_files_by_modified_date(folder):
    all_files = (
        os.path.join(basedir, filename)
        for basedir, dirs, files in os.walk(folder)
        for filename in files)
    sorted_files = sorted(all_files, key=os.path.getmtime)
    return sorted_files
