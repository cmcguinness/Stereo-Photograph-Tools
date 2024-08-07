# Stereo Photography Tools

I have a 3D camera, the Fuji W3, which generates .MPO files that have the left and right images from each shot.  That is not exactly the most popular format around, and I started cobbling together tools to process the images.

 In the past, Photoshop had support for them, but it's ability to work with 3D images has been deprecated.

This is a utility to do a few typical things I want to do:

* Break out the left and right images
* Create a Holmes Card from the images
* Create a cross-eye viewable image from the two
* Create a cross-eyed card in Holmes format (basically, takes the middle squares from left and right)
* Create a Wiggle3d animated GIF (Left/Right images alternating quickly)
* Create a red/cyan anaglyph

There are two modes of operation:

1. Batch, where all *.MPO files in a directory are converted, and
2. Interactive, where you load an MPO file into the app and then make adjustments on alignment, style, and gamma (γ) before saving it.

You can of course modify the code to suit your needs.



## Design

The repo is both a library and a standalone CLI tool.  The primary library is `sterotools.py`. Its class, `StereoTools`, takes a left/right pair of images and generates a variety of representations of them suitable for viewing.

The file `mpo.py` contains a class that can read .MPO images, such as produced by my Fuji camera, and extract the left/right images.  The file `leftrightpair.py` will read in two separate image files that hold left/right images.

The file `main.py` contains an example program that will scan a source directory for MPO files and generate different versions of each.



## Batch Usage

After installing the requirements, the `start_batch.py` runs from the command line without options.

You can edit the section that reads:

```python
if __name__ == '__main__':
    # Example usage
    source_dir = '/Users/charles/Library/Mobile Documents/com~apple~CloudDocs/Photos/102_FUJI'  # Update this path
    output_dir = 'outputs'  # Update this path

    extract_images_from_mpos(source_dir, output_dir, log_status=True)
```

To have the correct directories for the source of the .mpo files and where you want to put them, and then just run it.  It will cycle through all the .mpo files and convert them into the other formats.



## Interactive Usage

If you run the program `start_interactive.py`, it will prompt you to open an MPO file to allow you to build an anaglyph.  On the top of the window with the image are controls so:

* Change the alignment between the two images.  Generally speaking, if you bring the subject of the image into alignment, it will be the easiest to see.
* Flip into a mode where you see the difference between the left and right images to help align them,
* Toggle between various color modes (Color, Low Color, and B&W)
* Change the gamma (γ) of the output image to make it brighter or darker
* Save the current anaglyph to a file.  It will only ask you for a directory and then generate a timestamped name.



## Speed

Compressing PNG images is a trade-off between speed and amount of compression.

The last line of the method `save_image` determines the compression level.  0 is none, 1 is fast, and 9 is slow (but presumably, good).  Adjust as you like.



## Holmes Cards

The [Holmes Card](https://en.wikipedia.org/wiki/Stereoscope#Holmes_stereoscope) format was created in 1861, and is the most common format for printed 3D images.  Here are the specs for the size and placement of images I am using:

| Measurement           | Inches                |
| --------------------- | --------------------- |
| Width                 | 7.0 inches            |
| Height                | 3.5 inches            |
| Left/Right Margin     | 0.4 inch              |
| Middle Margin         | 0.2 inch              |
| Bottom Margin         | 0.3 inch              |
| Top Margin            | 0.2 inch              |
| Image Width           | 3.0 inch              |
| Image Height          | 3.0 inch              |
| Left Edge Right Image | 0.4 + 3.0 + 0.2 = 3.6 |

I create a Holmes Card at 300dpi, but you are free to adjust the resolution as you see fit.  It creates a slightly gray background to make it easier to cut the card out of a print at the right dimensions.



## Anaglyph Generation

Anaglyphs restrict the left image to the red channel and the right image to the blue and green channels of the merged image.  How you do that mapping turns out to produce some interesting effects and side-effects.  The code contains three mappings you can experiment with:

* Both Left & Right Color

  The output image is created by merging red channel of the left image and the blue and green channels of the right image.  

* Left B&W, Right Color: 

  The red channel of the output image has a greyscale version of the left image, and the blue and green channels are copied as-is from the blue and green channels of the right image.

* Both Left & Right B&W:

  The red channel is a greyscale version of the left image, and the blue and green channels each have a greyscale version of the right image.

The conversion of an image to greyscale is done via an approximate luminosity algorithm: BW = R * .3 + G * .6 + B * .1 .  

In addition, there's an option to apply a gamma correction to the red channel (<1 brightens, >1 darkens) if you want to play with the balance between left and right.

So long as the red channel only has data from the left image and the green and blue channels from the right image, you can come up with a large variety of mappings.



