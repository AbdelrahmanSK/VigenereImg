import datetime
import imghdr
from PIL import Image
import os


def load_image(image_path):
    try:
        return Image.open(image_path)
    except FileNotFoundError:
        print("Error: File not found.")
        return None
    except Exception as e:
        print("Error loading image:", e)
        return None

def save_image(image, output_path):
    try:
        image.save(output_path)
        print(f"Processed image saved as {output_path}")
    except Exception as e:
        print("Error saving image:", e)

def vigenere_encrypt(image, key):
    width, height = image.size
    encrypted_image = Image.new("RGB", (width, height))
    pixels = image.load()

    key_index = 0
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            r = (r + ord(key[key_index % len(key)])) % 256
            g = (g + ord(key[key_index % len(key)])) % 256
            b = (b + ord(key[key_index % len(key)])) % 256
            encrypted_image.putpixel((x, y), (r, g, b))
            key_index += 1

    return encrypted_image

def vigenere_decrypt(image, key):
    width, height = image.size
    decrypted_image = Image.new("RGB", (width, height))
    pixels = image.load()

    key_index = 0
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            r = (r - ord(key[key_index % len(key)])) % 256
            g = (g - ord(key[key_index % len(key)])) % 256
            b = (b - ord(key[key_index % len(key)])) % 256
            decrypted_image.putpixel((x, y), (r, g, b))
            key_index += 1

    return decrypted_image


def process_image(method, key, image_path, output_path):
    image = load_image(image_path)
    if image is None:
        return

    if method == 'E':
        encrypted_image = vigenere_encrypt(image, key)
        suffix = 'Enc_Img'
    elif method == 'D':
        encrypted_image = vigenere_decrypt(image, key)
        suffix = 'Dec_Img'
    else:
        print("Invalid method. Use 'E' for encryption or 'D' for decryption.")
        return

    output_dir = os.path.dirname(image_path)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    output_filename = f"{suffix}({timestamp}).jpg"
    output_path = os.path.join(output_dir, output_filename)
    save_image(encrypted_image, output_path)


if __name__ == "__main__":
    method = input("Enter 'E' for encryption or 'D' for decryption: ").upper()
    key = input("Enter the encryption/decryption key (a string): ")
    image_path = input("Enter the image file path: ")
    output_dir = input("Enter the output directory path: ")  # Ask for output directory path
    process_image(method, key, image_path, output_dir)
