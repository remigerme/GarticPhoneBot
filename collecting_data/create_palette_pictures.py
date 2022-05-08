from mimetypes import init
# Move to src/ to use the script
from image import init_gp_palette

from PIL import Image


def create_picture(r, g, b, c = 10):
    im = Image.new("RGB", (c, c), (r, g, b))
    return im

def main():
    gp_palette = init_gp_palette()
    for i in range(len(gp_palette) // 3):
        r, g, b = gp_palette[i], gp_palette[i + 1], gp_palette[i + 2]
        im = create_picture(r, g, b)
        im.save("p_{}_{}_{}.png".format(r, g, b))

if __name__ == "__main__":
    main()