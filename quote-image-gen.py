#!/usr/bin/env python3
import argparse
import textwrap
from PIL import Image, ImageDraw, ImageFont

def fit_text_to_image(draw, text, font_path, max_width, max_height):
    # Start with a large font size and decrease until it fits
    font_size = int(max_height * 0.69)
    while font_size > 10:  # Avoid font size becoming too small
        font = ImageFont.truetype(font_path, font_size)
        wrapped_lines = wrap_text(draw, text, font, max_width)
        line_heights = [draw.textbbox((0, 0), line, font=font)[3] for line in wrapped_lines]
        total_height = sum(line_heights)

        # Check if it fits both width and height
        if total_height <= max_height and all(draw.textbbox((0, 0), line, font=font)[2] <= max_width for line in wrapped_lines):
            return font, wrapped_lines
        font_size -= 2

    # Fallback: use default font if no size works
    return ImageFont.load_default(), wrap_text(draw, text, ImageFont.load_default(), max_width)

def wrap_text(draw, text, font, max_width):
    wrapped_lines = []
    for line in text.split("\n"):
        # Dynamically determine text wrapping width
        line_width = max_width
        wrapped_lines.extend(textwrap.wrap(line, width=40))  # Tweak dynamically based text-size

    return wrapped_lines

def main():
    parser = argparse.ArgumentParser(
        description="Create an 800x400 grayscale image with centered text."
    )
    parser.add_argument("image", help="Path to the input image.")
    parser.add_argument("text", help="Text to overlay.")
    parser.add_argument("--padding", type=int, default=20, help="Side padding.")
    parser.add_argument("--output", default="output.jpg", help="Output file.")
    parser.add_argument("--font", default=None, help="Path to a TTF font file.")
    args = parser.parse_args()

    # Load and convert image
    img = Image.open(args.image).convert("L").resize((800, 400))
    draw = ImageDraw.Draw(img)

    # Set font path or default font
    font_path = args.font if args.font else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    # Fit text to the image
    max_width = 800 - (args.padding * 2)
    max_height = 400 - (args.padding * 2)
    try:
        font, wrapped_lines = fit_text_to_image(draw, args.text, font_path, max_width, max_height)
    except OSError:
        print("Font file not found. Using default font.")
        font, wrapped_lines = fit_text_to_image(draw, args.text, None, max_width, max_height)

    # Calculate total text block height
    total_height = sum(draw.textbbox((0, 0), line, font=font)[3] for line in wrapped_lines)

    # Center vertically
    y = (400 - total_height) // 2

    # Draw text centered horizontally
    for line in wrapped_lines:
        text_bbox = draw.textbbox((0, 0), line, font=font)
        line_width, line_height = text_bbox[2], text_bbox[3]
        x = (800 - line_width) // 2
        draw.text(
            (x, y), line, font=font, fill="black",
            stroke_width=2, stroke_fill="white"
        )
        y += line_height

    img.save(args.output)

if __name__ == "__main__":
    main()
