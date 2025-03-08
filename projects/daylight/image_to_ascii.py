import sys
import math

from PIL import Image
import numpy as np


def get_ascii_char(grid, threshold=128):
    if not grid:
        return " "
    # avg_color = np.mean(cell, axis=(0, 1))
    # print(avg_color)
    # if all(float(x) == float(255) for x in avg_color):
    #    return " "

    # If empty cell, return space
    if cell.size == 0:
        return " "

    # Resize the cell to 3x3 using PIL
    if len(cell.shape) == 3:  # Color image
        pil_cell = Image.fromarray(cell)
        # Convert to grayscale
        pil_cell = pil_cell.convert("L")
    else:  # Already grayscale
        pil_cell = Image.fromarray(cell)

    # Resize to 3x3
    pil_cell = pil_cell.resize((3, 3), Image.BILINEAR)

    # Convert back to numpy array and normalize to [0,1] range
    small_cell = np.array(pil_cell).astype(float) / 255.0

    # Invert so that darker pixels have higher values (1.0 = black, 0.0 = white)
    normalized_cell = 1.0 - small_cell

    norm_sum = np.sum(normalized_cell)
    if norm_sum < 0.5:
        return " "

    # Define patterns (1 = dark, 0 = light)
    patterns = [
        (" ", np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])),  # Empty (all white)
        ("#", np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])),  # Full (all black)
        ("-", np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]])),  # Horizontal middle
        ("_", np.array([[0, 0, 0], [0, 0, 0], [1, 1, 1]])),  # Bottom line
        ("▔", np.array([[1, 1, 1], [0, 0, 0], [0, 0, 0]])),  # Top line
        ("|", np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]])),  # Vertical middle
        ("|", np.array([[1, 0, 0], [1, 0, 0], [1, 0, 0]])),  # Vertical left
        ("|", np.array([[0, 0, 1], [0, 0, 1], [0, 0, 1]])),  # Vertical right
        ("/", np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]])),  # Diagonal (/)
        ("\\", np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])),  # Diagonal (\)
        ("+", np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])),  # Plus-sign (+)
        ("X", np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]])),  # X
    ]

    # Find the best matching pattern
    best_match = " "
    best_score = -1

    # print(normalized_cell)
    for option in patterns:
        char, pattern = option
        # Calculate similarity score using dot product
        # This measures how well the pattern and cell align
        score = np.sum(normalized_cell * pattern) / np.sum(pattern)

        # Penalize extra dark pixels that don't match the pattern
        anti_pattern = 1 - pattern
        penalty = np.sum(normalized_cell * anti_pattern) / np.sum(anti_pattern)

        # Adjusted score
        adjusted_score = score - penalty

        if adjusted_score > best_score:
            best_score = adjusted_score
            best_match = char
        # print(f"char={char} score={adjusted_score} best={best_match} {best_score}")

    return best_match

    return "x"


# Terminal aspect ratio of height-to-width
char_aspect_ratio = 1.844


num_chars_width = 120
image_path = sys.argv[1]

img = Image.open(image_path)

# Get image dimensions
img_width, img_height = img.size
print(f"Image width={img_width} height={img_height}")

# Calculate grid dimensions
grid_width = img_width / num_chars_width

# Calculate height based on maintaining the aspect ratio
num_chars_height = math.ceil(
    (img_height / img_width) * num_chars_width / char_aspect_ratio
)
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
