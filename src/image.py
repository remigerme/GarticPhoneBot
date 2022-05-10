from cst import GP_COLORS, KB_CONTROLS
from locate import locate_playground, locate_palette
from utils import click
from state import DrawingState

from time import sleep

from PIL import Image
from PIL.ImagePalette import ImagePalette

from keyboard import is_pressed


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

def draw_partially(gp_image, p_locations, x0, y0, colors, scale, i, x_, y_, check_kb):
    # Draw the picture from the i-th color and (x, y) pixel onward
    # Return the state when finished/interrupted/paused
    # and the current color (i) and position (x, y)
    # Not recommended to set check_kb to False as
    # it's not possible to abort the drawing
    # but this helps gaining time
    n = len(colors)
    (w, h) = gp_image.size
    (x, y) = (x_, y_)
    drawing = True
    while i < n and drawing:
        (r, g, b) = colors[i]
        if (r, g, b) == (255, 255, 255):
            i += 1
            (x, y) = (0, 0)
            continue

        # Select the color
        click(*p_locations[(r, g, b)])

        # Paint every pixel of the image of this color
        while x < w and drawing:
            while y < h and drawing:
                if check_kb:
                    drawing = not (is_pressed(KB_CONTROLS["interrupt"]) or is_pressed(KB_CONTROLS["pause"]))
                p = gp_image.getpixel((x, y))
                if p == i:
                    click(x0 + scale * x, y0 + scale * y)
                y += 1
            if drawing:
                y = 0
                x += 1
        if drawing:
            x = 0
            i += 1
    if i == n:
        print("Drawing finished")
        s = DrawingState.FINISHED
    elif is_pressed("esc"):
        print("Drawing interrupted")
        s = DrawingState.INTERRUPTED
    else:
        print("Drawing paused")
        s = DrawingState.PAUSED
    return (s, i, x, y)

def draw(gp_image, x0, y0, colors, scale, check_kb):
    # The size of gp_image must have already been checked
    p_locations = locate_palette(colors)
    print("Palette has been located")
    # As we want to be able to pause / interrupt the script
    # Let's use a while loop and check keyboard events
    n = len(colors)
    i = 0
    (x, y) = (0, 0)
    drawing = True
    while drawing:
        (s, i, x, y) = draw_partially(gp_image, p_locations, x0, y0, colors, scale, i, x, y, check_kb)
        sleep(0.5)
        if s == DrawingState.FINISHED:
            drawing = False
        elif s == DrawingState.INTERRUPTED:
            drawing = False
        else:
            while not is_pressed(KB_CONTROLS["pause"]):
                pass
            print("Drawing resumed")
            sleep(0.5)

def draw_from(image, colors, resize, scale, check_kb):
    # Use the allowed palette
    palette = get_palette_from_colors(colors)
    gp_image = convert_to_gp_image(image, palette)
    # Resize if wanted
    w, h = gp_image.size
    (x0, y0, w0, h0) = locate_playground()
    print("Playground has been located")
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
    draw(gp_image, x0, y0, colors, scale, check_kb)

def main():
    input()
    im = Image.open("yoshi.jpg")
    draw_from(im, GP_COLORS, True, 6, True)

if __name__ == "__main__":
    main()