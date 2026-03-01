from PIL import Image

def get_pixel_2d_array(img):
    width, height = img.size
    pixels = list(img.getdata())
    return [pixels[i * width:(i + 1) * width] for i in range(height)]

def create_image_from_2d(pixels_2d, mode="RGB"):
    height = len(pixels_2d)
    width = len(pixels_2d[0])
    flat_pixels = [pixel for row in pixels_2d for pixel in row]
    
    new_img = Image.new(mode, (width, height))
    new_img.putdata(flat_pixels)
    return new_img

def apply_grayscale(pixels_2d):
    new_pixels = []
    for row in pixels_2d:
        new_row = []
        for (r, g, b) in row:
            avg = (r + g + b) // 3
            new_row.append((avg, avg, avg))
        new_pixels.append(new_row)
    return new_pixels

def apply_solarize(pixels_2d, threshold=128):
    new_pixels = []
    for row in pixels_2d:
        new_row = []
        for (r, g, b) in row:
            r = 255 - r if r > threshold else r
            g = 255 - g if g > threshold else g
            b = 255 - b if b > threshold else b
            new_row.append((r, g, b))
        new_pixels.append(new_row)
    return new_pixels

def apply_brightness(pixels_2d, factor=1.5):
    new_pixels = []
    for row in pixels_2d:
        new_row = []
        for (r, g, b) in row:
            nr = min(int(r * factor), 255)
            ng = min(int(g * factor), 255)
            nb = min(int(b * factor), 255)
            new_row.append((nr, ng, nb))
        new_pixels.append(new_row)
    return new_pixels


def main():
    try:
        img = Image.open("input.jpg").convert("RGB")
    except FileNotFoundError:
        print("file not found")
        return

    pixels = get_pixel_2d_array(img)

    print("Select transformations (y/n):")
    do_gray = input("Grayscale? ") == 'y'
    do_solar = input("Solarize? ") == 'y'
    do_bright = input("Increase Brightness? ") == 'y'

    processed_pixels = pixels
    if do_gray:
        processed_pixels = apply_grayscale(processed_pixels)
    if do_solar:
        processed_pixels = apply_solarize(processed_pixels)
    if do_bright:
        processed_pixels = apply_brightness(processed_pixels)

    output_img = create_image_from_2d(processed_pixels)
    output_img.save("output.png")
    print("Done! Saved as output.png")
    print(get_pixel_2d_array(output_img))

if __name__ == "__main__":
    main()
