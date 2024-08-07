#    ┌──────────────────────────────────────────────────────────┐
#    │                       Stereo Tools                       │
#    │                                                          │
#    │       A class for processing a left, right pair of       │
#    │      images into a variety of formats for saving /       │
#    │                viewing  as stereo images.                │
#    │                                                          │
#    └──────────────────────────────────────────────────────────┘
import os
from PIL import Image, ImageTk
import numpy as np
from stereopair import StereoPair
from tkinter import Tk, Canvas, Button, Label, PhotoImage, mainloop, Frame

saved_class = None

class StereoTools:
    def __init__(self, image: StereoPair=None):
        self.lbl = None
        self.image: StereoPair = image
        self.shift_x = 0
        self.shift_y = 0
        self.tkimg = None
        self.outdir = None
        self.outname = None

    # Pass in the image pair
    def set_image(self, image: StereoPair):
        self.image = image
        self.shift_x = 0
        self.shift_y = 0

    # Save an image to the output directory; create the directory if it does not exist
    # The name will be generated from self.image's name, timestamp, and the passed in suffix
    def save_image(self, image, output_directory, suffix=None):
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        output_file_name = ''
        if self.image.timestamp is not None and self.image.timestamp != '':
            output_file_name = f'{self.image.timestamp}-'

        output_file_name = f'{output_file_name}{self.image.name}'

        if suffix is not None:
            output_file_name = f'{output_file_name}--{suffix}'

        output_file_name += '.png'

        output_file_path = os.path.join(output_directory, output_file_name)

        image.save(output_file_path, compress_level=1)

        self.outname = output_file_name
        self.outdir = output_directory

    # Create a stereo card with the left and right images side-by-side
    # Note that the images are cropped to 900x900 pixels by taking the central square (assumes landscape images)
    def make_card(self, isHolmes=True, output_directory=None):
        def normalize_size(image: Image):
            # Resize the images to the same size
            width, height = image.size
            crop_left = int((width - height) / 2)
            crop_right = width - crop_left
            new_image = image.crop((crop_left, 0, crop_right, height))
            return new_image.resize((900, 900), Image.Resampling.LANCZOS)

        right_image = normalize_size(self.image.right_image)
        left_image = normalize_size(self.image.left_image)

        # Create a new image with double the width
        stereo_image = Image.new('RGB', (2100, 1050), color='#F8F8F8')

        if isHolmes:
            stereo_image.paste(left_image, (int(300 * 0.4), int(300 * 0.2)))
            stereo_image.paste(right_image, (int(300 * 3.6), int(300 * 0.2)))
            suffix='holmes'
        else:
            # Cross-eyed
            stereo_image.paste(right_image, (int(300 * 0.4), int(300 * 0.2)))
            stereo_image.paste(left_image, (int(300 * 3.6), int(300 * 0.2)))
            suffix='square-crossed'

        if output_directory is not None:
            self.save_image(stereo_image, output_directory, suffix)

        return stereo_image

    # Create a Holmes card from the images
    def make_holmes_card(self, output_directory = None):
        return self.make_card(isHolmes=True, output_directory=output_directory)

    # Create a square-crossed card from the images (a holmes card with the images swapped)
    def make_square_crossed_card(self, output_directory = None):
        return self.make_card(isHolmes=False, output_directory=output_directory)

    # Create a crossed-eye image from the images, using the full width of the images
    def make_cross_eyed(self, output_directory=None, middle_margin=0.01):
        # Assume the images are the same size
        width, height = self.image.left_image.size
        margin = int(2*middle_margin*width)

        # Create a new image with double the width
        stereo_image = Image.new('RGB', (width*2+margin, height), color='#F8F8F8')

        stereo_image.paste(self.image.left_image, (width+margin,0))
        stereo_image.paste(self.image.right_image, (0,0))

        if output_directory is not None:
            self.save_image(stereo_image, output_directory, 'crossed')

        return stereo_image

    def save_as_wiggle3d(self, output_directory, suffix='wiggle3d', ):
        output_file_name = f"{self.image.timestamp}-{self.image.name}-{suffix}.gif"
        output_file_path = os.path.join(output_directory, output_file_name)

        self.image.left_image.save(output_file_path, save_all=True, append_images=[self.image.right_image], duration=250, loop=0)


    def make_anaglyph(self, suffix='ana', output_directory=None, style='color', gamma=1.0, red_gamma=1.0, show_diff = False):

        styles = {
            'color': {
                'left':  (1.0, 0.0, 0.0, 0,  0.0, 0.0, 0.0, 0,  0.0, 0.0, 0.0, 0),
                'right': (0.0, 0.0, 0.0, 0,  0.0, 1.0, 0.0, 0,  0.0, 0.0, 1.0, 0)

            },
            'l-bw': {
                'left':  (0.3, 0.6, 0.1, 0,  0.0, 0.0, 0.0, 0,   0.0, 0.0, 0.0, 0),
                'right': (0.0, 0.0, 0.0, 0,  0.0, 1.0, 0.0, 0,   0.0, 0.0, 1.0, 0)
            },
            'bw': {
                'left':  (0.3, 0.6, 0.1, 0,   0.0, 0.0, 0.0, 0,   0.0, 0.0, 0.0, 0),
                'right': (0.0, 0.0, 0.0, 0,   0.3, 0.6, 0.1, 0,   0.3, 0.6, 0.1, 0)
            },
            'diff': {
                'left':  (1,0,0,0, 0,1,0,0, 0,0,1,0),
                'right': (1,0,0,0, 0,1,0,0, 0,0,1,0)
            },

        }

        if show_diff:
            style = 'diff'

        left_matrix  = styles[style]['left']
        right_matrix = styles[style]['right']


        ana_left = self.image.left_image.convert('RGB', left_matrix)
        ana_right = self.image.right_image.convert('RGB', right_matrix)

        if self.shift_x != 0 or self.shift_y != 0:
            lx,ly = ana_left.size
            if self.shift_x > 0:
                ana_left = ana_left.crop(  (self.shift_x,  0,  lx,               ly))
                ana_right = ana_right.crop((0,             0,  lx-self.shift_x,  ly))
            if self.shift_x < 0:
                ana_right = ana_right.crop((-self.shift_x, 0,  lx,               ly))
                ana_left = ana_left.crop(  (0,             0,  lx+self.shift_x,  ly))

            lx,ly = ana_left.size
            if self.shift_y > 0:
                ana_left = ana_left.crop(  (0,  self.shift_y, lx, ly))
                ana_right = ana_right.crop((0, 0,            lx, ly-self.shift_y))
            if self.shift_y < 0:
                ana_right = ana_right.crop((0, -self.shift_y, lx, ly))
                ana_left = ana_left.crop(  (0, 0,             lx, ly+self.shift_y))

        # Because Red values are perceived as darker than Green, we can brighten up the red
        if red_gamma != 1.0:
            ana_left = ana_left.point(lambda x: ((x / 255) ** red_gamma) * 255)

        na_left = np.array(ana_left)
        na_right = np.array(ana_right)

        if show_diff:
            na_left = np.dot(na_left[...,:3], [0.2989, 0.5870, 0.1140])
            na_right = np.dot(na_right[...,:3], [0.2989, 0.5870, 0.1140])
            np_added = np.abs(na_left - na_right)
        else:
            np_added = na_left + na_right

        anaglyph = Image.fromarray(np_added)

        # Adjust the brightness of the final image
        if gamma != 1.0:
            anaglyph = anaglyph.point(lambda x: ((x / 255) ** gamma) * 255)

        if output_directory is not None:
            self.save_image(anaglyph, output_directory, suffix)

        return anaglyph

    # Save the left and right images as separate files
    def save_left_right_images(self, output_directory):
        for t in [('left', self.image.left_image), ('right', self.image.right_image)]:
            self.save_image(t[1], output_directory, t[0])

