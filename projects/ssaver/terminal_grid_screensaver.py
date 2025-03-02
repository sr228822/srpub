#!/usr/bin/env python3
"""
Mac Terminal Grid Screensaver
A 4x4 grid of terminal-like displays for use as a macOS screensaver.
"""

import curses
import argparse
import time
import subprocess
import os
import random
import threading
from typing import List, Callable, Tuple, Dict, Any

# Define color pairs
COLOR_PAIRS = {
    "default": (curses.COLOR_WHITE, curses.COLOR_BLACK),
    "green": (curses.COLOR_GREEN, curses.COLOR_BLACK),
    "blue": (curses.COLOR_BLUE, curses.COLOR_BLACK),
    "cyan": (curses.COLOR_CYAN, curses.COLOR_BLACK),
    "red": (curses.COLOR_RED, curses.COLOR_BLACK),
    "magenta": (curses.COLOR_MAGENTA, curses.COLOR_BLACK),
    "yellow": (curses.COLOR_YELLOW, curses.COLOR_BLACK),
}

class TerminalCell:
    """A single cell in the terminal grid"""

    def __init__(self, window, title: str, content_generator: Callable, color: str = "default"):
        """
        Initialize a terminal cell

        Args:
            window: The curses window for this cell
            title: The title to display at the top of the cell
            content_generator: A function that generates content for the cell
            color: The color scheme to use for this cell
        """
        self.window = window
        self.title = title
        self.content_generator = content_generator
        self.color = color
        self.content_lines = []
        self.max_lines = 0
        self.max_cols = 0
        self.update_dimensions()

    def update_dimensions(self):
        """Update the dimensions of the cell"""
        self.max_lines, self.max_cols = self.window.getmaxyx()

    def render_frame(self):
        """Render the frame of the cell"""
        self.window.clear()
        self.window.box()
        # Draw the title
        self.window.addstr(0, 2, f" {self.title} ")

    def update(self):
        """Update the content of the cell"""
        # Get new content
        new_content = self.content_generator()
        if isinstance(new_content, str):
            self.content_lines = new_content.split("\n")
        elif isinstance(new_content, list):
            self.content_lines = new_content

        # Render the frame
        self.render_frame()

        # Render the content
        for i, line in enumerate(self.content_lines):
            if i >= self.max_lines - 2:  # Leave space for the border
                break
            try:
                self.window.addstr(i + 1, 1, line[:self.max_cols-2])
            except curses.error:
                pass  # Ignore errors when writing to the last cell

        self.window.refresh()


class GridScreensaver:
    """Main class for the terminal grid screensaver"""

    def __init__(self, stdscr):
        """
        Initialize the grid screensaver

        Args:
            stdscr: The main curses window
        """
        self.stdscr = stdscr
        self.running = True
        self.cells = []
        self.initialize_colors()

    def initialize_colors(self):
        """Initialize color pairs"""
        curses.start_color()
        for i, (name, (fg, bg)) in enumerate(COLOR_PAIRS.items(), 1):
            curses.init_pair(i, fg, bg)

    def get_color_pair(self, name: str) -> int:
        """Get the color pair number for a named color"""
        if name not in COLOR_PAIRS:
            name = "default"
        return list(COLOR_PAIRS.keys()).index(name) + 1

    def create_grid(self, rows: int, cols: int):
        """
        Create a grid of terminal cells

        Args:
            rows: Number of rows in the grid
            cols: Number of columns in the grid
        """
        max_lines, max_cols = self.stdscr.getmaxyx()
        cell_height = max_lines // rows
        cell_width = max_cols // cols

        # Create cells
        self.cells = []
        for i in range(rows):
            row_cells = []
            for j in range(cols):
                # Create a window for this cell
                win = curses.newwin(
                    cell_height,
                    cell_width,
                    i * cell_height,
                    j * cell_width
                )

                # Choose a content generator and color for this cell
                generator, title, color = self.get_cell_configuration(i, j)

                # Create the cell
                cell = TerminalCell(win, title, generator, color)
                row_cells.append(cell)
            self.cells.append(row_cells)

    def get_cell_configuration(self, row: int, col: int) -> Tuple[Callable, str, str]:
        """
        Get the configuration for a cell

        Args:
            row: The row of the cell
            col: The column of the cell

        Returns:
            A tuple of (content_generator, title, color)
        """
        # Define some example generators
        generators = [
            (self.generate_system_info, "System Info", "green"),
            (self.generate_clock, "Clock", "blue"),
            #(self.generate_matrix_effect, "Matrix", "green"),
            (self.generate_network_stats, "Network", "cyan"),
            (self.generate_cpu_stats, "CPU", "red"),
            (self.generate_memory_stats, "Memory", "magenta"),
            (self.generate_disk_stats, "Disk", "yellow"),
            (self.generate_processes, "Processes", "default"),
            (self.generate_weather, "Weather", "cyan"),
            (self.generate_quotes, "Quotes", "default"),
            (self.generate_calendar, "Calendar", "blue"),
            #(self.generate_ascii_art, "ASCII Art", "green"),
            (self.generate_file_system, "Files", "yellow"),
            #(self.generate_random_numbers, "Random", "magenta"),
            (self.generate_ip_info, "IP Info", "cyan"),
            (self.generate_battery_status, "Battery", "yellow"),
        ]

        # Calculate index based on row and col
        index = row * 4 + col

        # Return generator, title, and color
        return generators[index]

    def generate_system_info(self) -> List[str]:
        """Generate system information"""
        try:
            output = subprocess.check_output(["system_profiler", "SPSoftwareDataType"],
                                            universal_newlines=True)
            return output.strip().split("\n")[:10]
        except:
            return ["System Info Unavailable"]

    def generate_clock(self) -> List[str]:
        """Generate a clock display"""
        now = time.localtime()
        date_str = time.strftime("%A, %B %d, %Y", now)
        time_str = time.strftime("%H:%M:%S", now)

        return [
            "",
            "  " + "=" * 20,
            f"  {date_str}",
            "  " + "=" * 20,
            "",
            f"  {time_str}",
            "  " + "=" * 20,
        ]

    def generate_matrix_effect(self) -> List[str]:
        """Generate a matrix-like effect"""
        lines = []
        for _ in range(10):
            line = ""
            for _ in range(20):
                if random.random() > 0.7:
                    line += random.choice("01")
                else:
                    line += " "
            lines.append(line)
        return lines

    def generate_network_stats(self) -> List[str]:
        """Generate network statistics"""
        try:
            output = subprocess.check_output(["netstat", "-i"], universal_newlines=True)
            return output.strip().split("\n")[:10]
        except:
            return ["Network Stats Unavailable"]

    def generate_cpu_stats(self) -> List[str]:
        """Generate CPU statistics"""
        try:
            output = subprocess.check_output(["top", "-l", "1", "-n", "0"],
                                            universal_newlines=True)
            cpu_lines = [line for line in output.split("\n") if "CPU usage" in line]
            return ["CPU Statistics:"] + cpu_lines
        except:
            return ["CPU Stats Unavailable"]

    def generate_memory_stats(self) -> List[str]:
        """Generate memory statistics"""
        try:
            output = subprocess.check_output(["vm_stat"], universal_newlines=True)
            return output.strip().split("\n")[:10]
        except:
            return ["Memory Stats Unavailable"]

    def generate_disk_stats(self) -> List[str]:
        """Generate disk statistics"""
        try:
            output = subprocess.check_output(["df", "-h"], universal_newlines=True)
            return output.strip().split("\n")[:10]
        except:
            return ["Disk Stats Unavailable"]

    def generate_processes(self) -> List[str]:
        """Generate a list of processes"""
        try:
            output = subprocess.check_output(["ps", "-ef"], universal_newlines=True)
            return output.strip().split("\n")[:10]
        except:
            return ["Process List Unavailable"]

    def generate_weather(self) -> List[str]:
        """Generate weather information (simulated)"""
        weather_conditions = ["Sunny", "Cloudy", "Rainy", "Snowy", "Foggy", "Windy"]
        condition = random.choice(weather_conditions)
        temp = random.randint(0, 30)
        return [
            "Weather Forecast:",
            f"Condition: {condition}",
            f"Temperature: {temp}°C",
            f"Humidity: {random.randint(30, 95)}%",
            f"Wind: {random.randint(0, 30)} km/h",
        ]

    def generate_quotes(self) -> List[str]:
        """Generate random quotes"""
        quotes = [
            "The best way to predict the future is to invent it.",
            "Keep it simple, stupid.",
            "The journey of a thousand miles begins with a single step.",
            "Stay hungry, stay foolish.",
            "The only way to do great work is to love what you do.",
            "Life is what happens when you're busy making other plans.",
            "Be yourself; everyone else is already taken.",
        ]

        return ["Quote of the moment:", "", random.choice(quotes)]

    def generate_calendar(self) -> List[str]:
        """Generate a calendar for the current month"""
        try:
            output = subprocess.check_output(["cal"], universal_newlines=True)
            return output.strip().split("\n")
        except:
            return ["Calendar Unavailable"]

    def generate_ascii_art(self) -> List[str]:
        """Generate ASCII art"""
        art_options = [
            [
                "  /\\_/\\  ",
                " ( o.o ) ",
                "  > ^ <  ",
                "   Cat   "
            ],
            [
                "    _    ",
                "   / \\   ",
                "  /   \\  ",
                " /     \\ ",
                "/       \\",
                "---------",
                "Mountain "
            ],
            [
                "   ,--,  ",
                "  (( O )) ",
                "   `--'   ",
                "   Apple  "
            ],
            [
                " _______  ",
                "|       | ",
                "|  MAC  | ",
                "|_______| ",
                "Computer  "
            ]
        ]

        return random.choice(art_options)

    def generate_file_system(self) -> List[str]:
        """Generate a file system listing"""
        try:
            output = subprocess.check_output(["ls", "-la", os.environ.get("HOME", "/")],
                                            universal_newlines=True)
            return output.strip().split("\n")[:10]
        except:
            return ["File System Unavailable"]

    def generate_random_numbers(self) -> List[str]:
        """Generate random numbers"""
        numbers = []
        for _ in range(10):
            line = ""
            for _ in range(5):
                line += f"{random.randint(1, 999):4d} "
            numbers.append(line)
        return numbers

    def generate_ip_info(self) -> List[str]:
        """Generate IP information"""
        try:
            output = subprocess.check_output(["ifconfig"], universal_newlines=True)
            ip_lines = []
            for line in output.strip().split("\n"):
                if "inet " in line and "127.0.0.1" not in line:
                    ip_lines.append(line.strip())
            return ["IP Addresses:"] + ip_lines[:10]
        except:
            return ["IP Info Unavailable"]

    def generate_battery_status(self) -> List[str]:
        """Generate battery status"""
        try:
            output = subprocess.check_output(["pmset", "-g", "batt"],
                                            universal_newlines=True)
            return output.strip().split("\n")
        except:
            return ["Battery Status Unavailable"]

    def update_cells(self):
        """Update all cells"""
        for row in self.cells:
            for cell in row:
                cell.update()

    def run(self, rows=4, cols=4, interval=5):
        """Run the screensaver"""
        # Hide the cursor
        curses.curs_set(0)

        # Create the grid
        self.create_grid(rows=rows, cols=cols)

        # Main loop
        first = True
        while self.running:
            try:
                t0 = time.time()

                # Update all cells
                self.update_cells()

                # Check for key press
                self.stdscr.timeout(100)
                key = self.stdscr.getch()
                #if key != -1:
                #    self.running = False

                # Sleep for a bit
                duration = time.time() - t0
                sleep_for = max(0.1, interval-duration)
                #print(f"Sleeping for {sleep_for}")
                if not first:
                    time.sleep(sleep_for)
                first=False
            except KeyboardInterrupt:
                self.running = False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Terminal Grid Screensaver")
    parser.add_argument("--rows", type=int, default=3, help="Number of rows")
    parser.add_argument("--cols", type=int, default=3, help="Number of columns")
    parser.add_argument("--interval", type=int, default=5, help="Refresh interval")
    args = parser.parse_args()

    # Run the screensaver
    curses.wrapper(lambda stdscr: GridScreensaver(stdscr).run(rows=args.rows, cols=args.cols, interval=args.interval))


if __name__ == "__main__":
    main()
