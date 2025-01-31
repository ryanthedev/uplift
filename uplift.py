import os
import sys
import time
import logging
from PIL import Image
from waveshare_epd import epd7in5_V2

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Get the path to the 'pics' folder
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pics')

try:
    logging.info("Initializing e-Paper display")
    epd = epd7in5_V2.EPD()

    logging.info("Initializing and clearing display")
    epd.init()
    epd.Clear()

    # Get a list of image files in the 'pics' directory
    image_files = [f for f in os.listdir(picdir) if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp'))]

    if not image_files:
        logging.info("No images found in the 'pics' directory")
        epd.sleep()
        sys.exit()

    # Loop forever over the images
    while True:
        for image_file in image_files:
            image_path = os.path.join(picdir, image_file)
            logging.info(f"Displaying image: {image_path}")

            # Open and resize the image to fit the display
            Himage = Image.open(image_path).convert('1')
            Himage = Himage.resize((epd.width, epd.height), Image.ANTIALIAS)

            # Display the image
            epd.display(epd.getbuffer(Himage))

            # Wait for 10 seconds before showing the next image
            time.sleep(10)

except IOError as e:
    logging.error(e)

except KeyboardInterrupt:
    logging.info("Interrupted by user (Ctrl+C)")
    epd7in5_V2.epdconfig.module_exit(cleanup=True)
    sys.exit()
