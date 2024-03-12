from Steganography_OPS import *
from XOR_OPS import *
from RSA_Encry_Decry import *
from Interface import *
from PIL import Image
import numpy as np


def load_images(complete_original_image_path, complete_top_layer_image_path):
    original_image = Image.open(complete_original_image_path)
    top_layer = Image.open(complete_top_layer_image_path)
    print("Loading: Completed")
    return [original_image, top_layer]


def get_cipher_image_array(complete_top_layer_path):
    top_layer = Image.open(complete_top_layer_path)
    top_layer_pixels = [[[val for val in top_layer.getpixel((i, j))]
                        for i in range(0, top_layer.size[0])]
                        for j in range(0, top_layer.size[1])]
    top_layer_pixels = np.array(top_layer_pixels)
    top_layer_pixels = top_layer_pixels.reshape(top_layer.size[1], top_layer.size[0], 3)
    print("Conversion: Completed")
    return top_layer_pixels


def images_to_array(original_image, top_layer):
    original_top_layer_pixels = [[[val for val in top_layer.getpixel((i, j))]
                                 for i in range(0, top_layer.size[0])]
                                 for j in range(0, top_layer.size[1])]
    original_top_layer_pixels = np.array(original_top_layer_pixels)
    original_top_layer_pixels = original_top_layer_pixels.reshape(top_layer.size[1], top_layer.size[0], 3)

    top_layer_pixels = [[[val for val in top_layer.getpixel((i, j))]
                        for i in range(0, top_layer.size[0])]
                        for j in range(0, top_layer.size[1])]
    top_layer_pixels = np.array(top_layer_pixels)
    top_layer_pixels = top_layer_pixels.reshape(top_layer.size[1], top_layer.size[0], 3)

    image_pixels = [[[val for val in original_image.getpixel((i, j))]
                    for i in range(0, original_image.size[0])]
                    for j in range(0, original_image.size[1])]
    image_pixels = np.array(image_pixels)
    image_pixels = image_pixels.reshape(original_image.size[1], original_image.size[0], 3)
    print("Conversion: Completed")
    return [original_top_layer_pixels, top_layer_pixels, image_pixels]


def perform_optical_encryption(image_pixels):
    original_image_width, original_image_height = len(image_pixels[0]), len(image_pixels)
    image_pixels = image_adjacent_pixel_xor(image_pixels, original_image_height, original_image_width)
    print("Optical: Completed Encryption")
    return image_pixels


def save_optical_encryption_image(image_pixels, path):
    pixel_xor_image = Image.fromarray(image_pixels.astype('uint8'))
    pixel_xor_image.save(path)
    print("Optical: Saved Optically Encrypted Image")


def perform_steganography(top_layer_pixels, image_pixels):
    top_layer_pixels = inject_image_in_top(top_layer_pixels, image_pixels)
    print("Steganography: Completed Encryption")
    return top_layer_pixels


def save_steganography_encrypted_image(top_layer_pixels, path):
    top_layer = Image.fromarray(top_layer_pixels.astype('uint8'))
    top_layer.save(path)
    print("Steganography: Saved Steganography Encrypted Image")


def perform_steganography_analysis(original_top_layer_pixels, top_layer_pixels):
    steganography_detection_pixels = get_difference_steganography(original_top_layer_pixels, top_layer_pixels)
    steganography_detection_pixels = np.array(steganography_detection_pixels)
    steganography_detection_pixels = steganography_detection_pixels.reshape(len(top_layer_pixels), len(top_layer_pixels[0]), 3)
    print("Steganography: Completed Steganography analysis")
    return steganography_detection_pixels


def save_steganography_detection_image(steganography_detection_pixels, path):
    steganography_detection_image = Image.fromarray(steganography_detection_pixels.astype('uint8'))
    steganography_detection_image.save(path)
    "Steganography: Saved Steganography analysis image"


def perform_steganography_decryption(top_layer_pixels, original_image_height, original_image_width):
    extracted_image_pixels = extract_image_from_top(top_layer_pixels, original_image_height, original_image_width)
    print("Steganography: Completed Steganography decryption")
    return extracted_image_pixels


def save_steganography_decrypted_image(extracted_image_pixels, path):
    extracted_image = Image.fromarray(extracted_image_pixels.astype('uint8'))
    extracted_image.save(path)
    print("Steganography: Saved Steganography decrypted image")


def perform_optical_decryption(extracted_image_pixels, original_image_width, original_image_height):
    extracted_image_pixels = extracted_image_pixels.astype('int')
    optically_decrypted_image_pixels = image_adjacent_pixel_xor_reverse(extracted_image_pixels, original_image_height, original_image_width)
    print("Optical: Completed Decryption")
    return optically_decrypted_image_pixels


def save_optically_decrypted_image(optically_decrypted_image_pixels, path):
    optically_decrypted_image = Image.fromarray(optically_decrypted_image_pixels.astype('uint8'))
    optically_decrypted_image.save(path)
    print("Optical: Saved Optically decrypted image")


def perform_rsa_encryption(size, public_key):
    width = size[0]
    height = size[1]
    print("RSA: Completed Encryption")
    return str(rsa_encryption(int(''.join([str(1) for i in range(len(str(width)))]) + str(0) + str(width)+str(height)), public_key))


def perform_rsa_decryption(cipher_text, private_key):
    decrypted_text = str(rsa_decryption(int(cipher_text), private_key))
    width_digits = decrypted_text.index('0')
    width_text = decrypted_text[(width_digits+1):(2*width_digits+1)]
    height_text = decrypted_text[(2*width_digits+1):]
    width = int(width_text)
    height = int(height_text)
    print("RSA: Completed Decryption")
    return [width, height]  # size
