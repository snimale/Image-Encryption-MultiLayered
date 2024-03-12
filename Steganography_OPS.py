import random
import numpy as np


def inject_image_in_top(top_image, bottom_image):
    bottom_height = len(bottom_image)
    bottom_width = len(bottom_image[0])
    top_height = len(top_image)
    top_width = len(top_image[0])

    skip_interval = get_skip_interval(bottom_height, bottom_width, top_height, top_width)
    ptr = 0

    for i in range(0, bottom_height):
        for j in range(0, bottom_width):
            curr_pixel_r_g_b_binary = [int_to_8_bit_binary(bottom_image[i][j][0]),
                                       int_to_8_bit_binary(bottom_image[i][j][1]),
                                       int_to_8_bit_binary(bottom_image[i][j][2])]
            top_image = inject_rgb_bits(curr_pixel_r_g_b_binary, top_image, ptr, skip_interval)
            ptr += 8 * skip_interval
    print("Steganography: Completed Image Injection")
    top_image = inject_garbage_rgb_bits_end(top_image, skip_interval, ptr)
    print("Steganography: Completed Garbage Injection")
    return top_image


def get_difference_steganography(original, modified):
    h, w = len(original), len(original[0])
    changed_pixels_image = [[[150, 150, 150]
                             if ((original[i][j][0] != modified[i][j][0]) or
                                 (original[i][j][1] != modified[i][j][1]) or
                                 (original[i][j][2] != modified[i][j][2]))
                             else [255, 255, 255] for j in range(0, w)] for i in range(0, h)]
    return changed_pixels_image


def extract_image_from_top(top_image, height, width):
    skip_interval = get_skip_interval(width, height, len(top_image), len(top_image[0]))
    image_pixels = [[[1, 1, 1] for i in range(0, width)] for j in range(0, height)]
    image_pixels = np.array(image_pixels)
    image_pixels = image_pixels.reshape(height, width, 3)
    for i in range(height*width):
        for k in range(3):
            curr_ptr = i * 8 * skip_interval
            curr_val_bits = []
            for j in range(0, 8):
                curr_bit = (top_image[(curr_ptr + (j*skip_interval)) // len(top_image[0])][(curr_ptr + (j*skip_interval)) % len(top_image[0])][k]) % 2
                curr_val_bits.append(curr_bit)

            curr_val = _8_bit_binary_to_int(curr_val_bits)
            image_pixels[i // width][i % width][k] = curr_val

    print("Steganography: Extraction Complete")
    image_pixels = image_pixels.reshape(height, width, 3)
    return image_pixels


def _8_bit_binary_to_int(curr_val_bits):
    return sum([2**i if curr_val_bits[i] == 1 else 0 for i in range(8)])


def get_skip_interval(bottom_height, bottom_width, top_height, top_width):
    skip_pixels = (top_width * top_height - 1) // (bottom_height * bottom_width * 8)
    return skip_pixels


def int_to_8_bit_binary(curr):
    return [0 if curr // (2 ** i) % 2 == 0 else 1 for i in range(0, 8)]


def inject_rgb_bits(bit_list, top_image, ptr, skip_interval):
    width = len(top_image[0])
    for i in range(8):
        for j in range(3):
            bit = bit_list[j][i]
            if bit == 1:
                top_image[ptr // width][ptr % width][j] = (top_image[ptr // width][ptr % width][j] | 1)
            else:
                top_image[ptr // width][ptr % width][j] = (top_image[ptr // width][ptr % width][j] & 254)
        ptr += skip_interval

    return top_image


def inject_garbage_rgb_bits_end(top_image, skip_interval, floor):
    ptr = 0
    width = len(top_image[0])
    height = len(top_image)
    while ptr <= (width * height - 1):
        if ptr % skip_interval == 0 and ptr <= floor:
            ptr += 1
            continue
        for plain in range(3):
            if (top_image[ptr // width][ptr % width][plain] & 1) == 0:
                top_image[ptr // width][ptr % width][plain] = random.choice([top_image[ptr // width][ptr % width][plain] + 1, top_image[ptr // width][ptr % width][plain]])
            else:
                top_image[ptr // width][ptr % width][plain] = random.choice([top_image[ptr // width][ptr % width][plain] - 1, top_image[ptr // width][ptr % width][plain]])
        ptr += 1

    return top_image


