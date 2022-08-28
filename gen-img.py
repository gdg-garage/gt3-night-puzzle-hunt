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

    font = ImageFont.truetype("/home/tivvit/.local/share/fonts/Roboto Mono for Powerline.ttf", 14)

    # measure text size
    img = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(img)
    text_width, text_height = draw.textsize(words[0], font=font)

    distance = 32
    text_side_bumper = 6
    safe_zone = text_height + 3 * text_side_bumper # 1x for each side and once for line coming out of the image
    map_with_white = Image.new("RGBA", (width + safe_zone, height + safe_zone), (255, 255, 255, 255))
    map_with_white.paste(map_img, (safe_zone, safe_zone))

    width += safe_zone
    height += safe_zone

    y_start = safe_zone + distance / 2
    word_pos = 0

    # img = Image.new("RGBA", (width, height))
    # draw = ImageDraw.Draw(img)
    # text_width, text_height = draw.textsize(words[0], font=font)
    text_middle = text_height / 2

    for i in range(round((height - y_start) / distance)):
        text = words[word_pos].upper()

        draw.text((text_side_bumper, y_start + i * distance), text, (0, 0, 0), font=font)
        draw.line(
            ((text_width + 2 * text_side_bumper, text_middle + y_start + i * distance), (width, text_middle + y_start + i * distance)),
            fill=(0, 0, 0, round(.40 * 255)), width=1)
        word_pos += 1

    img = Image.alpha_composite(map_with_white, img)
    img = img.convert("RGB")  # Remove alpha for saving in jpg format.
    img.save('sample-out.png')


if __name__ == '__main__':
    main()
