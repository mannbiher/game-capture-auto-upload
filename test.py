import unittest
from upload import upload_file, upload_thumbnail
from file_operations import get_largest_files


class TestStringMethods(unittest.TestCase):
    # def test_upload(self):
    #     file_path = (
    #         'C:\\Users\\Neha\\Documents\\Wondershare Filmora\\Output\\'
    #         'My Video.mp4')
    #     title = 'Test Video'
    #     upload_file(file_path, title)

    # def test_thumbnail(self):
    #     thumbnail = 'output.jpeg'
    #     upload_thumbnail('dBo4OobGUc0',thumbnail)

    def test_largest_file(self):
        folder = 'C:\\Users\\Neha\\Documents\\Wondershare Filmora\\Output'
        print(get_largest_files(folder))


if __name__ == '__main__':
    unittest.main()
