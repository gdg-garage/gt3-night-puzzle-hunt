from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from lib import load_words


def main():
    # map = Image.open("map_grid.png")
    map_img = Image.open("mapy.png")
    map_img.putalpha(255)
    width, height = map_img.size
    words = load_words()

    safe_zone = 60
    map_with_white = Image.new("RGBA", (width + safe_zone, height + safe_zone), (255, 255, 255, 255))
    map_with_white.paste(map_img, (safe_zone, safe_zone))

    width += safe_zone
    height += safe_zone

    # font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 12)
    font = ImageFont.truetype("/home/tivvit/.local/share/fonts/Roboto Mono for Powerline.ttf", 14)

    distance = 32
    y_start = safe_zone + distance / 2
    word_pos = 0

    img = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(img)
    text_width, text_height = draw.textsize(words[0], font=font)
    line_offset = text_height / 2

    for i in range(round((height - y_start) / distance)):
        text = words[word_pos].upper()

        draw.text((4, y_start + i * distance), text, (0, 0, 0), font=font)
        draw.line(
            ((text_width + 8, line_offset + y_start + i * distance), (width, line_offset + y_start + i * distance)),
            fill=(0, 0, 0, round(.40 * 255)), width=1)
        word_pos += 1

    img = Image.alpha_composite(map_with_white, img)
    img = img.convert("RGB")  # Remove alpha for saving in jpg format.
    img.save('sample-out.png')


if __name__ == '__main__':
    main()
