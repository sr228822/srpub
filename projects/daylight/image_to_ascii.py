import sys
import math

from PIL import Image
import numpy as np

def get_ascii_char(grid):
    if not grid:
        return " "
    #print(grid)
    #print(len(grid))
    #print(len(grid[0]))
    avg_color = np.mean(cell, axis=(0, 1))
    print(avg_color)
    if all(float(x) == float(255) for x in avg_color):
        return " "
    return "x"
    

# Terminal aspect ratio of height-to-width
char_aspect_ratio = 1.844


num_chars_width = 80
image_path = sys.argv[1]

img = Image.open(image_path)

# Get image dimensions
img_width, img_height = img.size
print(f"Image width={img_width} height={img_height}")

# Calculate grid dimensions
grid_width = img_width / num_chars_width

# Calculate height based on maintaining the aspect ratio
num_chars_height = math.ceil((img_height / img_width) * num_chars_width / char_aspect_ratio)
print(f"num chars width={num_chars_width} height={num_chars_height}")
grid_height = img_height / num_chars_height

print(f"grid width={grid_width} height={grid_height}")

# Convert image to numpy array for easier manipulation
img_array = np.array(img)

# Initialize grid for storing colors
color_grid = []


# Extract colors from each cell
grid = []
for y in range(num_chars_height):
    row = []
    for x in range(num_chars_width):
        # Calculate cell boundaries
        x_start = int(x * grid_width)
        y_start = int(y * grid_height)
        x_end = min(int((x + 1) * grid_width), img_width)
        y_end = min(int((y + 1) * grid_height), img_height)

        # Extract the cell area
        cell = img_array[y_start:y_end, x_start:x_end]

        char = get_ascii_char(grid)
        row.append(char)

    grid.append(row)

for row in grid:
    print("".join(row))
