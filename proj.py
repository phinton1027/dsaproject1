from PIL import Image

class MiniPhotoshop:
    def __init__(self, file_path):
        try:
            self.original_img = Image.open(file_path).convert("RGB")
            self.width, self.height = self.original_img.size
            self.pixel_grid = self._image_to_2d_array()
        except FileNotFoundError:
            raise FileNotFoundError(f"image file invalid")

    def _image_to_2d_array(self):
        flat_data = list(self.original_img.getdata())
        return [flat_data[i * self.width:(i + 1) * self.width] for i in range(self.height)]

    def apply_grayscale(self):
        for y in range(self.height):
            for x in range(self.width):
                r, g, b = self.pixel_grid[y][x]
                avg = (r + g + b) // 3
                self.pixel_grid[y][x] = (avg, avg, avg)

    def apply_solarize(self, threshold=128):
        for y in range(self.height):
            for x in range(self.width):
                r, g, b = self.pixel_grid[y][x]
                r = 255 - r if r > threshold else r
                g = 255 - g if g > threshold else g
                b = 255 - b if b > threshold else b
                self.pixel_grid[y][x] = (r, g, b)

    def apply_contrast(self, level=50):
        factor = (259 * (level + 255)) / (255 * (259 - level))
        for y in range(self.height):
            for x in range(self.width):
                r, g, b = self.pixel_grid[y][x]
                nr = min(255, max(0, int(factor * (r - 128) + 128)))
                ng = min(255, max(0, int(factor * (g - 128) + 128)))
                nb = min(255, max(0, int(factor * (b - 128) + 128)))
                self.pixel_grid[y][x] = (nr, ng, nb)

    def save(self, output_path):
        flat_pixels = [pixel for row in self.pixel_grid for pixel in row]
        new_img = Image.new("RGB", (self.width, self.height))
        new_img.putdata(flat_pixels)
        new_img.save(output_path)

def run_menu():
    file_name = input("Enter the filename of your image (input.jpg): ")
    
    try:
        editor = MiniPhotoshop(file_name)
        
        print("\nAvailable transformations:")
        print("1. Grayscale")
        print("2. Solarize")
        print("3. High Contrast")
        choices = input("Enter the numbers you want to apply (e.g., 13): ")

        if "1" in choices:
            editor.apply_grayscale()
            print(">> Applied Grayscale")
        if "2" in choices:
            editor.apply_solarize()
            print(">> Applied Solarize")
        if "3" in choices:
            editor.apply_contrast()
            print(">> Applied High Contrast")

        output_name = "processed_image.png"
        editor.save(output_name)
        print("Done")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_menu()
