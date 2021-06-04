import praw
from exif import Image

class rsOrganizer:

    def __init__(self, filePath, postDetails):
        self.filePath = filePath
        self.postDetails = postDetails


    def updateMetaData(self):
        try:
            # Load in the EXIF metadata
            self.metaData = Image(self.file)
        except:
            print("Unable to load metadata from file!")
            return
