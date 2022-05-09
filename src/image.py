from cst import GP_COLORS
from locate import locate_playground, locate_palette
from utils import click

from PIL import Image
from PIL.ImagePalette import ImagePalette


def get_palette_from_colors(colors):
    palette = []
    for c in colors:
        palette.extend(c)
    return palette

def convert_to_gp_image(image, palette):
    im_palette = Image.new("P", (1, 1))
    im_palette.putpalette(palette)
    im = image.quantize(colors= min(256, len(palette)), palette=im_palette)
    return im


def draw(gp_image, x0, y0, colors, scale):
    # The size of gp_image must have already been checked
    p_locations = locate_palette(colors)
    for (i, (r, g, b)) in enumerate(colors):
        if (r, g, b) == (255, 255, 255):
            continue

        # Select the color
        click(*p_locations[(r, g, b)])

        # Paint every pixel of the image of this color
        w, h = gp_image.size
        for x in range(w):
            for y in range(h):
                p = gp_image.getpixel((x, y))
                if p == i:
                    click(x0 + scale * x, y0 + scale * y)


def draw_from(image, colors, resize, scale = 2):
    # Use the allowed palette
    palette = get_palette_from_colors(colors)
    gp_image = convert_to_gp_image(image, palette)
    # Resize if wanted
    w, h = gp_image.size
    (x0, y0, w0, h0) = locate_playground()
    if resize:
        gp_image = gp_image.resize((w0 // scale, h0 // scale))
    elif scale * w > w0 or scale * h > h0:
        print("The image is bigger than the playground. It'll be cropped in the center to fit in.")
        d = 2 * scale
        left = w // d - min(w, w0) // d
        right = w // d + min(w, w0) // d
        top = h // d - min(h, h0) // d
        bottom = h // d + min(h, h0) // d
        gp_image = gp_image.crop((left, top, right, bottom))
    draw(gp_image, x0, y0, colors, scale)

def main():
    input()
    im = Image.open("yoshi.jpg")
    draw_from(im, GP_COLORS, True, 5)

if __name__ == "__main__":
    main()