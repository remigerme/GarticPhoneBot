from mimetypes import init
# Move to src/ to use the script
from cst import GP_COLORS
from image import get_palette_from_colors

from PIL import Image


def create_picture(r, g, b, c = 10):
    im = Image.new("RGB", (c, c), (r, g, b))
    return im

def main():
    gp_palette = get_palette_from_colors(GP_COLORS)
    for i in range(len(gp_palette) // 3):
        r, g, b = gp_palette[3 * i], gp_palette[3 * i + 1], gp_palette[3 * i + 2]
        im = create_picture(r, g, b)
        im.save("p_{}_{}_{}.png".format(r, g, b))

if __name__ == "__main__":
    main()