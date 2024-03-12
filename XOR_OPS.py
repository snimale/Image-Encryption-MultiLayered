import numpy as np


def image_adjacent_pixel_xor(image_pixels, height, width):
    first_pixel = [vals for vals in image_pixels[0][0]]  # call by value by copying the vals in another list
    for i in range(0, height):
        for j in range(0, width):
            next_pos = (i * width + j + 1)
            x = next_pos // width
            y = next_pos % width
            if next_pos > ((height * width) - 1):
                image_pixels[i][j] = [vals for vals in first_pixel]  # call by value by copying the vals in another list
                break
            image_pixels[i][j][0] = (image_pixels[x][y][0] ^ image_pixels[i][j][0])
            image_pixels[i][j][2] = (image_pixels[x][y][2] ^ image_pixels[i][j][2])
            image_pixels[i][j][1] = (image_pixels[x][y][1] ^ image_pixels[i][j][1])
    return image_pixels


def image_adjacent_pixel_xor_reverse(image_pixels, height, width):
    image_pixels.reshape(height, width, 3)
    for i in range(0, height):
        for j in range(0, width):
            prev_pos = (i * width + j - 1)
            if prev_pos == -1:
                x = height - 1
                y = width - 1
            else:
                x = prev_pos // width
                y = prev_pos % width

            if prev_pos >= (height * width) - 2:  # break at prev = second last pixel
                break

            image_pixels[i][j][0] = (image_pixels[x][y][0] ^ image_pixels[i][j][0])
            image_pixels[i][j][2] = (image_pixels[x][y][2] ^ image_pixels[i][j][2])
            image_pixels[i][j][1] = (image_pixels[x][y][1] ^ image_pixels[i][j][1])

    # move shift the image one pixel forward
    prev_pixel = image_pixels[height - 1][width - 1]
    for i in range(0, height):
        for j in range(0, width):
            curr_pixel = [vals for vals in image_pixels[i][j]]
            image_pixels[i][j] = [val for val in prev_pixel]
            prev_pixel = curr_pixel
    return image_pixels

