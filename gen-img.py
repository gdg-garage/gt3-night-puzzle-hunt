from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from lib import load_words


def main():
    # map_img = Image.open("map_grid.png")
    map_img = Image.open("mapy_right_trim.png")
    map_img.putalpha(255)
    width, height = map_img.size
    words = sorted(load_words())

    font = ImageFont.truetype("RobotoMono-Medium.ttf", 18)

    # measure text size
    img = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(img)
    text_width, text_height = draw.textsize(words[0], font=font)

    distance = 32
    text_side_bumper = 6
    safe_zone_left = text_width + 3 * text_side_bumper  # 1x for each side and once for line coming out of the image
    safe_zone_up = text_width + 13 * text_side_bumper  # 1x for each side and once for line coming out of the image
    map_with_white = Image.new("RGBA", (width + safe_zone_left, height + safe_zone_up), (255, 255, 255, 255))
    map_with_white.paste(map_img, (safe_zone_left, safe_zone_up))

    width += safe_zone_left
    height += safe_zone_up

    y_start = safe_zone_up
    x_start = safe_zone_left
    word_pos = 0

    # grid and text overlay
    img = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(img)
    text_middle = text_height / 2

    for i in range(round((height - y_start) / distance)):
        text = words[word_pos].upper()

        draw.text((text_side_bumper, y_start + i * distance), text, (0, 0, 0), font=font)
        draw.line(
            ((text_width + 2 * text_side_bumper, text_middle + y_start + i * distance),
             (width, text_middle + y_start + i * distance)),
            fill=(0, 0, 0, round(.40 * 255)), width=1)
        word_pos += 1

    for i in range(round((width - x_start) / distance)):
        text = words[word_pos].upper()
        text_img = Image.new("RGBA", (text_width, text_height))

        # Print into the rotated area
        d = ImageDraw.Draw(text_img)
        d.text((0, 0), text, (0, 0, 0), font=font)

        text_img = text_img.rotate(90, expand=True)

        # Insert it back into the source image
        img.paste(text_img, (x_start + i * distance, text_side_bumper))

        draw.line(
            ((text_middle + x_start + i * distance, text_width + 2 * text_side_bumper),
             (text_middle + x_start + i * distance, height)),
            fill=(0, 0, 0, round(.40 * 255)), width=1)

        word_pos += 1
        if word_pos >= len(words):
            word_pos = len(words) - 1

    img = Image.alpha_composite(map_with_white, img)
    img = img.convert("RGB")  # Remove alpha for saving in jpg format.
    img.save('final.png')


if __name__ == '__main__':
    main()
