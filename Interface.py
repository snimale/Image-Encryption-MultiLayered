from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import Interface_Util

decryption_root = None
root = Tk()
root.attributes('-fullscreen', True)
root.title("Image Encryption")
root.config(bg="#D3D3D3")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

header_frame = Frame(root, bg='black', height=60)
header_frame.pack(fill=X, padx=20, pady=20)
header_label = Label(header_frame, text="Image Encryption and Decryption", font="comicsans 40 bold", bg='black', fg="white")
header_label.pack(pady=10)

debug_frame = Frame(root, bg='black', width=root.winfo_screenwidth() // 2, height=root.winfo_screenheight())
debug_frame.pack(side=RIGHT, fill=BOTH, padx=150, pady=100)
debug_text = Text(debug_frame, bg='white', wrap=WORD)
debug_text.pack(side=LEFT, fill=BOTH, expand=True)


original_image_path = ""
top_layer_image_path = ""
final_encrypted_image_path = ""  # done
final_encrypted_image_name = ""  # done
public_key = []  # [618596131, 317223818411189325457]  # done
private_key = []  # [291273621025443274195, 317223818411189325457]
optically_encrypted_image_path = ""
optically_encrypted_image_name = ""
steganography_detection_image_path = ""
steganography_detection_image_name = ""
initial_encrypted_image_path = ""
steganography_decrypted_image_path = ""
steganography_decrypted_image_name = ""
decrypted_image_path = ""
decrypted_image_name = ""
cipher_text = ""
save_decrypted_steganography = BooleanVar()
save_decrypted_steganography.set(False)
save_optically_encrypted = BooleanVar()
save_optically_encrypted.set(False)
save_steganography_detection = BooleanVar()
save_steganography_detection.set(False)


def encrypt():
    global root
    global public_key
    global final_encrypted_image_name
    global cipher_text

    try:
        public_key = [int(public_key_entry.get()), int(public_key_n_entry.get())]
    except ValueError:
        log("Please Enter All The File Paths & keys Needed For The Operations.")
        return

    final_encrypted_image_name = final_image_name_entry.get()

    if original_image_path == "" or top_layer_image_path == "" or final_encrypted_image_path == "" or final_encrypted_image_name == "" or public_key == ["Enter public key", "Enter n"]:
        log("Please Enter All The File Paths & keys Needed For The Operations.")
        return
    if save_optically_encrypted.get() is True and (optically_encrypted_image_path == "" or optically_encrypted_image_name == ""):
        log("Please Enter All The File Paths Needed For The Operations.")
        return
    if save_steganography_detection.get() is True and (steganography_detection_image_name == "" or steganography_detection_image_path == ""):
        log("Please Enter All The File Paths Needed For The Operations.")
        return

    root.destroy()
    cipher_text = Interface_Util.on_click_encrypt(original_image_path,
                                    top_layer_image_path,
                                    final_encrypted_image_path, final_encrypted_image_name,
                                    public_key,
                                    save_optically_encrypted.get(), optically_encrypted_image_path, optically_encrypted_image_name,
                                    save_steganography_detection.get(), steganography_detection_image_path, steganography_detection_image_name)
    print("Cipher Text Generated: ", cipher_text)
    open_decryption_ui()


def decrypt():
    global decryption_root
    global private_key
    global decrypted_image_name
    global cipher_text

    cipher_text = cipher_text_entry.get()
    decrypted_image_name = output_image_name_entry.get()
    try:
        private_key = [int(private_key_entry.get()), int(private_key_n_entry.get())]
    except ValueError:
        d_log("Please Enter All The File Paths & keys Needed For The Operations.")
        return

    if initial_encrypted_image_path == "" or decrypted_image_path == "" or decrypted_image_name == "" or private_key == [] or cipher_text == "":
        d_log("Please Enter All The File Paths & keys Needed For The Operations.")
        return
    if save_decrypted_steganography.get() is True and (steganography_decrypted_image_path == "" or steganography_decrypted_image_name == ""):
        d_log("Please Enter All The File Paths Needed For The Operations.")
        return

    decryption_root.destroy()
    Interface_Util.on_click_decrypt(initial_encrypted_image_path,
                                    decrypted_image_path, decrypted_image_name,
                                    cipher_text, private_key,
                                    save_decrypted_steganography.get(), steganography_decrypted_image_path, steganography_decrypted_image_name)


def load_original_img_path():
   global original_image_path
   original_image_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png")])


def load_top_layer_img_path():
   global top_layer_image_path
   top_layer_image_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png")])


def load_encrypted_img_path():
   global final_encrypted_image_path
   final_encrypted_image_path = filedialog.askdirectory(title="Select a Folder")


def load_save_optical_img_path():
   global optically_encrypted_image_path
   optically_encrypted_image_path = filedialog.askdirectory(title="Select a Folder")


def load_save_steg_det_img_path():
   global steganography_detection_image_path
   steganography_detection_image_path = filedialog.askdirectory(title="Select a Folder")


def load_decryption_input_img_path():
    global initial_encrypted_image_path
    initial_encrypted_image_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png")])


def load_decryption_output_img_path():
    global decrypted_image_path
    decrypted_image_path = filedialog.askdirectory(title="Select a Folder")


def load_save_steg_decryption_img_path():
    global steganography_decrypted_image_path
    steganography_decrypted_image_path = filedialog.askdirectory(title="Select a Folder")


def log(message):
    debug_text.insert(END, message + '\n')
    debug_text.see(END)


def d_log(message):
    d_debug_text.insert(END, message + '\n')
    d_debug_text.see(END)


def open_decryption_ui():
    global decryption_root
    global private_key_entry
    global private_key_n_entry
    global d_debug_text
    global output_image_name_entry
    global cipher_text_entry

    decryption_root = Tk()
    decryption_root.attributes('-fullscreen', True)
    decryption_root.title("Image Encryption and Decryption")
    decryption_root.config(bg="#D3D3D3")
    d_screen_width = decryption_root.winfo_screenwidth()
    d_screen_height = decryption_root.winfo_screenheight()

    d_header_frame = Frame(decryption_root, bg='black', height=60)
    d_header_frame.pack(fill=X, padx=20, pady=20)
    d_header_label = Label(d_header_frame, text="Image Decryption", font="comicsans 40 bold", bg='black', fg="white")
    d_header_label.pack(pady=10)

    d_debug_frame = Frame(decryption_root, bg='black', width=decryption_root.winfo_screenwidth() // 2, height=decryption_root.winfo_screenheight())
    d_debug_frame.pack(side=RIGHT, fill=BOTH, padx=150, pady=100)
    d_debug_text = Text(d_debug_frame, bg='white', wrap=WORD)
    d_debug_text.pack(side=LEFT, fill=BOTH, expand=True)

    # Private Key UI
    private_key_entry = Entry(decryption_root, font=("Arial", 16), width=15)
    private_key_entry.insert(0, "Enter Private Key")
    private_key_entry.place(x=(d_screen_width // 4 - private_key_entry.winfo_reqwidth() // 2) - 150, y=d_screen_height // 2 + 125)

    private_key_n_entry = Entry(decryption_root, font=("Arial", 16), width=15)
    private_key_n_entry.insert(0, "Enter n")
    private_key_n_entry.place(x=(d_screen_width // 4 - private_key_n_entry.winfo_reqwidth() // 2) + 150, y=d_screen_height // 2 + 125)

    # Name of Output File and cipher text entry
    output_image_name_entry = Entry(decryption_root, font=("Arial", 16), width=30)
    output_image_name_entry.insert(0, "Enter Decrypted Image Name")
    output_image_name_entry.place(x=(d_screen_width // 4 - output_image_name_entry.winfo_reqwidth() // 2), y=d_screen_height // 2 - 30)

    cipher_text_entry = Entry(decryption_root, font=("Arial", 16), width=30)
    cipher_text_entry.insert(0, "Enter Cipher Text")
    cipher_text_entry.place(x=(d_screen_width // 4 - cipher_text_entry.winfo_reqwidth() // 2) , y=d_screen_height // 2 + 60)


    # Select images and folders path UI
    input_encrypted_img_button = Button(decryption_root, text="Select Input Image", font="comicsans 20 bold", cursor="hand2", bg="black", fg="white", command=load_decryption_input_img_path)
    input_encrypted_img_button.config(width=25, height=1)
    input_encrypted_img_button.place(x=(d_screen_width // 4 - input_encrypted_img_button.winfo_reqwidth() // 2), y=d_screen_height // 2 - 200)

    decrypted_img_button = Button(decryption_root, text="Select Output Location", font="comicsans 20 bold", cursor="hand2", bg="black", fg="white", command=load_decryption_output_img_path)
    decrypted_img_button.config(width=25, height=1)
    decrypted_img_button.place(x=(d_screen_width // 4 - decrypted_img_button.winfo_reqwidth() // 2), y=d_screen_height // 2 - 100)

    begin_decryption_button = Button(decryption_root, text="Start Decryption", font="comicsans 20 bold", cursor="hand2", bg="#1100FF", fg="white", command=decrypt)
    begin_decryption_button.config(width=15, height=1)
    begin_decryption_button.place(x=(d_screen_width // 4 - begin_decryption_button.winfo_reqwidth() // 2), y=d_screen_height // 2 + 200)

    # Save mid steps
    steganography_reverse_save_tick = Checkbutton(decryption_root, width=30, text="Save steganography Decryption Output", command=load_save_steg_decryption_img_path, variable=save_decrypted_steganography, onvalue=True, offvalue=False)
    steganography_reverse_save_tick.pack(pady=5)
    steganography_reverse_save_tick.place(x=(d_screen_width // 4 - steganography_reverse_save_tick.winfo_reqwidth() // 2), y=d_screen_height // 2 + 300)

    return


original_img_button = Button(root, text="Select Original Image", font="comicsans 20 bold", cursor="hand2", bg="black", fg="white", command=load_original_img_path)
original_img_button.config(width=25, height=1)
original_img_button.place(x=(screen_width//4 - original_img_button.winfo_reqwidth()//2), y=screen_height//2-200)

top_layer_img_button = Button(root, text="Select Top Layer Image", font="comicsans 20 bold", cursor="hand2", bg="black", fg="white", command=load_top_layer_img_path)
top_layer_img_button.config(width=25, height=1)
top_layer_img_button.place(x=(screen_width//4 - top_layer_img_button.winfo_reqwidth()//2), y=screen_height//2-100)

encrypted_img_button = Button(root, text="Select Final Location", font="comicsans 20 bold", cursor="hand2", bg="black", fg="white", command=load_encrypted_img_path)
encrypted_img_button.config(width=25, height=1)
encrypted_img_button.place(x=(screen_width//4 - encrypted_img_button.winfo_reqwidth()//2), y=screen_height//2)

begin_encryption_button = Button(root, text="Start Encryption", font="comicsans 20 bold", cursor="hand2", bg="#1100FF", fg="white", command=encrypt)
begin_encryption_button.config(width=15, height=1)
begin_encryption_button.place(x=(screen_width//4 - begin_encryption_button.winfo_reqwidth()//2), y=screen_height//2+200)

final_image_name_entry = Entry(root, font=("Arial", 16), width=30)
final_image_name_entry.insert(0, "Enter Encrypted Image Name")
final_image_name_entry.place(x=(screen_width//4 - final_image_name_entry.winfo_reqwidth()//2), y=screen_height//2+60)


# get public key
public_key_entry = Entry(root, font=("Arial", 16), width=15)
public_key_entry.insert(0, "Enter Public Key")
public_key_entry.place(x=(screen_width//4 - public_key_entry.winfo_reqwidth()//2) - 150, y=screen_height//2+125)

public_key_n_entry = Entry(root, font=("Arial", 16), width=15)
public_key_n_entry.insert(0, "Enter n")
public_key_n_entry.place(x=(screen_width//4 - public_key_n_entry.winfo_reqwidth()//2) + 150, y=screen_height//2+125)


# save mid steps
optical_encryption_tick = Checkbutton(root, width=30, text="Save optical encryption image", command=load_save_optical_img_path, variable=save_optically_encrypted, onvalue=True, offvalue=False)
optical_encryption_tick.pack(pady=5)
optical_encryption_tick.place(x=(screen_width//4 - optical_encryption_tick.winfo_reqwidth()//2) + -150, y=screen_height//2+300)

steganography_detection_tick = Checkbutton(root, width=30, text="Save steganography Analysis Image", command=load_save_steg_det_img_path, variable=save_steganography_detection, onvalue=True, offvalue=False)
steganography_detection_tick.pack(pady=5)
steganography_detection_tick.place(x=(screen_width//4 - steganography_detection_tick.winfo_reqwidth()//2) + 150, y=screen_height//2+300)

root.mainloop()

