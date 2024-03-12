import main


def on_click_encrypt(original_image_path,
                     top_layer_image_path,
                     encrypted_image_path, encrypted_image_name,
                     public_key,
                     save_optically_encrypted_image, optically_encrypted_image_path, optically_encrypted_image_name,
                     save_steganography_detection_image, stegano_detection_image_path, stegano_detection_image_name):

    # get completed paths for images
    complete_original_image_path = original_image_path
    complete_top_layer_image_path = top_layer_image_path
    complete_optically_encrypted_image_path = optically_encrypted_image_path+"/"+optically_encrypted_image_name+".png"
    complete_stegano_detection_image_path = stegano_detection_image_path+"/"+stegano_detection_image_name+".png"
    complete_encrypted_image_path = encrypted_image_path+"/"+encrypted_image_name+".png"

    # load images for use
    original_image, top_layer = main.load_images(complete_original_image_path, complete_top_layer_image_path)
    original_image_width, original_image_height = original_image.size

    # from image to pixels array
    original_top_layer_pixels, top_layer_pixels, image_pixels = main.images_to_array(original_image, top_layer)


    ######## ENCRYPTION BEGINS ########

    # optical encryption - compulsory
    image_pixels = main.perform_optical_encryption(image_pixels)
    if save_optically_encrypted_image is True:
        main.save_optical_encryption_image(image_pixels, complete_optically_encrypted_image_path)

    # steganography - compulsory
    top_layer_pixels = main.perform_steganography(top_layer_pixels, image_pixels)
    main.save_steganography_encrypted_image(top_layer_pixels, complete_encrypted_image_path)

    # choice for analysis for confirmation of proper injection
    if save_steganography_detection_image is True:
        steganography_detection_image = main.perform_steganography_analysis(original_top_layer_pixels, top_layer_pixels)
        main.save_steganography_detection_image(steganography_detection_image, complete_stegano_detection_image_path)

    # RSA cipher_text generation for decryption - compulsory
    cipher_text = main.perform_rsa_encryption([original_image_width, original_image_height], public_key)

    return cipher_text


def on_click_decrypt(encrypted_image_path,
                     decrypted_image_path, decrypted_image_name,
                     cipher_text, private_key,
                     save_decrypted_steganography_image, stegano_decrypted_image_path, stegano_decrypted_image_name):

    complete_encrypted_image_path = encrypted_image_path
    complete_decrypted_image_path = decrypted_image_path+"/"+decrypted_image_name+".png"
    complete_steganography_decrypted_image_path = stegano_decrypted_image_path+"/"+stegano_decrypted_image_name+".png"
    top_layer_pixels = main.get_cipher_image_array(complete_encrypted_image_path)


    ######## DECRYPTION BEGINS ########


    # first get size by decrypting original cipher text. size is needed for steganography decryption
    size = main.perform_rsa_decryption(cipher_text, private_key)
    width, height = size

    # get optically encrypted image back from top_layer
    extracted_image_pixels = main.perform_steganography_decryption(top_layer_pixels, height, width)
    if save_decrypted_steganography_image is True:
        main.save_steganography_decrypted_image(extracted_image_pixels, complete_steganography_decrypted_image_path)

    # perform optical decryption to get back original image
    optically_decrypted_image_pixels = main.perform_optical_decryption(extracted_image_pixels, width, height)
    main.save_optically_decrypted_image(optically_decrypted_image_pixels, complete_decrypted_image_path)

