import bpy
import time
import os

from PIL import Image, ImageChops

from . import utils

# disable max resolution limit from PIL. Comes in the way of screenshotting abnormally huge trees
Image.MAX_IMAGE_PIXELS = None


def trimImage(img: Image.Image):
    '''function to trim out empty space from the edges, leaving a padding (as defined in preferences)
    :rtype: An ~PIL.Image.Image object.'''
    bg_clr = tuple(bpy.context.preferences.themes[0].node_editor.space.back *
                   255)  # get the background color of the shader editor from themes and map from 0-1 to 0-255 for PIL operations
    # convert float tuple to int tuple (as Image.new(color) expectes Int tuple)
    bg_clr = tuple(map(lambda i: int(i), bg_clr))

    padding = bpy.context.preferences.addons[__package__].preferences.padding_amount
    # to subtract padding amount from x_min, y_min and add to x_max, y_max for cropping
    padding_tuple = (-padding, -padding, padding, padding)

    img_w, img_h = img.size
    # tuple of image size in format (x_min, y_min, x_max, y_max) for clamping padding amount, with some 'hacky' elements
    img_size_tuple = (img_w, img_h, img_w, img_h)

    bg = Image.new(img.mode, img.size, bg_clr)
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()

    # offset the co-ords to leave space for padding
    crop_tuple = tuple(map(lambda i, j: i + j, bbox, padding_tuple))
    # clamp all values to not be outside the image (negative or greater than size of image)
    crop_tuple = tuple(map(lambda i, j: max(
        0, min(i, j)), crop_tuple, img_size_tuple))

    if bbox:
        return img.crop(crop_tuple)
    else:
        return img


# function to stitch multiple tiles to one single image
def stitchTiles(num_x, num_y, margin):
    '''function to stitch multiple tiles to one single image'''
    folder_path = utils.makeDirectory()

    tile_path = os.path.join(folder_path, f'Prt_y{0}_x{0}.png')
    tile = Image.open(tile_path)
    tile_w, tile_h = tile.size
    box = (margin, margin, tile_w-margin, tile_h-margin)
    out_canvas = Image.new(
        'RGB', ((tile_w - margin * 2) * num_x, (tile_h - margin * 2) * num_y))

    for y in range(num_y):
        for x in range(num_x):
            tile_path = os.path.join(folder_path, f'Prt_y{y}_x{x}.png')
            current_tile = Image.open(tile_path)
            cropped_tile = current_tile.crop(box)
            out_canvas.paste(cropped_tile, ((tile_w - 2 * margin) * x,
                             (tile_h - 2 * margin) * (num_y - (y + 1))))
            os.remove(tile_path)  # remove used tiles

    if not bpy.context.preferences.addons[__package__].preferences.disable_auto_crop:
        out_canvas = trimImage(out_canvas)

    timestamp = time.strftime("%y%m%d-%H%M%S")
    out_path = os.path.join(folder_path, f'NodeTreeShot{timestamp}.png')
    out_canvas.save(out_path)
