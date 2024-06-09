import os

from PIL import Image

from stereopair import StereoPair


class LeftRightPair(StereoPair):

    # We want to find the longest common substring in file names to get some sense of the name for the pair
    @staticmethod
    def find_longest(s1, s2):
        longest = ''
        for i_left in range(len(s1)):
            for i_right in range(len(s2)):
                for len_left in range(len(s1[i_left:]), 0, -1):
                    if s1[i_left:i_left + len_left] == s2[i_right:i_right + len_left]:
                        match = s1[i_left:i_left + len_left]
                        if len(match) > len(longest):
                            longest = match
                        break

        return longest

    def __init__(self, left_file_path, right_file_path):

        left_image = Image.open(left_file_path)
        right_image = Image.open(right_file_path)

        # Try to discern a common root name
        left_name = os.path.splitext(os.path.basename(left_file_path))[0]
        right_name = os.path.splitext(os.path.basename(right_file_path))[0]
        name = self.find_longest(left_name, right_name)

        # There may be names like foo-left.pn and foo-right.png giving us a common name
        # of foo-, so get rid of leading or trailing punctuation
        while name.startswith(' ') or name.startswith('_') or name.startswith('-') or name.startswith('.'):
            name = name[1:]

        while name.endswith(' ') or name.endswith('_') or name.endswith('-') or name.endswith('.'):
            name = name[:-1]

        if name == '':
            name = left_name

        exif = left_image.getexif()
        if 306 in exif:
            timestamp = exif[306]
            timestamp = timestamp.replace(':', '-').replace(' ', '-')
        else:
            timestamp = ''

        super().__init__(left_image, right_image, name, timestamp)


# test code
if __name__ == "__main__":
    image = LeftRightPair('test_data/DSCF2118-left.png', 'test_data/DSCF2118-right.png')
    print(f'Common name: {image.name}, Timestamp: {image.timestamp}')
