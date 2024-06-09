#    ┌──────────────────────────────────────────────────────────┐
#    │                           MPO                            │
#    │                                                          │
#    │    Read in an MPO file and split its images into Left    │
#    │    and Right images for processing as a stereo photo.    │
#    │                                                          │
#    └──────────────────────────────────────────────────────────┘

import os
from PIL import Image
from stereopair import StereoPair


class MPO(StereoPair):

    def __init__(self, mpo_file_path):
        name = os.path.splitext(os.path.basename(mpo_file_path))[0]

        # The processing is pretty straight forward.  Open the file and
        # image 0 is the left image and image 1 is the right image. Note
        # that this mapping is correct for my Fuji W3 camera, but I can't
        # say that is true for any other source, so you may have to change it.
        with Image.open(mpo_file_path) as mpo_image:
            self.mpo = mpo_image
            mpo_image.seek(0)
            left_image = mpo_image.copy()

            mpo_image.seek(1)
            right_image = mpo_image.copy()

            timestamp = mpo_image.getexif()[306]

            if timestamp is None:
                timestamp = 'unknown'
            else:
                timestamp = timestamp.replace(':', '-').replace(' ', '-')

            super().__init__(left_image, right_image, name, timestamp)


#   Simple test to make sure code is working
if __name__ == "__main__":
    mpo = MPO('test_data/DSCF2118.MPO')
    print(f'Common name: {mpo.name}, Timestamp: {mpo.timestamp}')