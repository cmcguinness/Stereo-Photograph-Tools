from stereotools import StereoTools
from mpo import MPO
import os


# Extract the left/right images from all MPO files in the source directory and save them to the output directory
# In a variety of useful formats
def extract_images_from_mpos(source_directory, output_directory, log_status=False):

    tools = StereoTools()
    # Scan the source directory for all *.MPO files
    for file_name in os.listdir(source_directory):
        if file_name.lower().endswith('.mpo') and not file_name.startswith('.'):
            file_path = os.path.join(source_directory, file_name)

            if log_status:
                print(f'Extracting images from {file_name}...', end='', flush=True)

            image = MPO(file_path)
            tools.set_image(image)

            tools.save_left_right_images(output_directory)
            if log_status:
                print('left-right...', end='', flush=True)

            tools.make_holmes_card(output_directory)
            if log_status:
                print('holmes...', end='', flush=True)

            tools.make_square_crossed_card(output_directory)
            if log_status:
                print('square-crossed...', end='', flush=True)

            tools.make_cross_eyed(output_directory)
            if log_status:
                print('crossed...', end='', flush=True)

            tools.save_as_wiggle3d(output_directory=output_directory)
            if log_status:
                print('wiggle3d...', end='', flush=True)

            tools.make_anaglyph(output_directory=output_directory)
            if log_status:
                print('anaglyph...', end='', flush=True)

            if log_status:
                print('done')


# If run from the command line, extract images from the MPO files in the source directory
# and save them to the output directory
if __name__ == '__main__':
    # Example usage
    source_dir = '/Users/charles/Library/Mobile Documents/com~apple~CloudDocs/Photos/102_FUJI'  # Update this path
    output_dir = 'outputs'  # Update this path

    extract_images_from_mpos(source_dir, output_dir, log_status=True)