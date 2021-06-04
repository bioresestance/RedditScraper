import praw
from exif import Image

class rsOrganizer:

    def __init__(self, filePath, postDetails):
        self.filePath = filePath
        self.postDetails = postDetails
        try:
            # Try and load in the EXIF metadata
            self.metaData = Image(self.file)
        except:
            print("Unable to load metadata from file!")
            return


        