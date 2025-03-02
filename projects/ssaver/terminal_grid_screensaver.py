#!/usr/bin/env python3
"""
Mac Terminal Grid Screensaver
A 4x4 grid of terminal-like displays for use as a macOS screensaver.
"""

import argparse
import time
import subprocess
import os
import random
from typing import List, Callable, Tuple

# HTML color codes
HTML_COLORS = {
    "default": "#FFFFFF",
    "green": "#00FF00",
    "blue": "#0000FF",
    "cyan": "#00FFFF",
    "red": "#FF0000",
    "magenta": "#FF00FF",
    "yellow": "#FFFF00",
}


class TerminalCell:
    """A single cell in the terminal grid"""

    def __init__(self, title: str, content_generator: Callable, color: str = "default"):
        """
        Initialize a terminal cell

        Args:
            title: The title to display at the top of the cell
            content_generator: A function that generates content for the cell
            color: The color scheme to use for this cell
        """
        self.title = title
        self.content_generator = content_generator
        self.color = color
        self.content_lines = []
        self.max_lines = 40  # Default for web output
        self.max_cols = 300  # Default for web output

    def update(self):
        """Update the content of the cell"""
        # Get new content
        new_content = self.content_generator()
        if isinstance(new_content, str):
            self.content_lines = new_content.split("\n")
        elif isinstance(new_content, list):
            self.content_lines = new_content

    def get_html_content(self) -> str:
        """Get the content of the cell as HTML"""
        html = f'<div class="cell" style="color: {HTML_COLORS.get(self.color, "#FFFFFF")}">\n'
        html += f'<div class="cell-title">{self.title}</div>\n'
        html += '<div class="cell-content">\n'

        for line in self.content_lines[: self.max_lines]:
            html += f"{line}<br>\n"

        html += "</div>\n</div>\n"
        return html


class GridScreensaver:
    """Main class for the terminal grid screensaver"""

    def __init__(self, web_output_path=None, rows=3, cols=3):
        """
        Initialize the grid screensaver

        Args:
            stdscr: The main curses window
        """
        self.running = True
        self.web_output_path = web_output_path

        self.cells = []
        self.rows = rows
        self.cols = cols
        self.create_grid(rows=rows, cols=cols)

    def create_grid(self, rows: int, cols: int):
        """
        Create a grid of terminal cells

        Args:
            rows: Number of rows in the grid
            cols: Number of columns in the grid
        """
        # Create cells
        self.cells = []
        for i in range(rows):
            row_cells = []
            for j in range(cols):
                # Choose a content generator and color for this cell
                generator, title, color = self.get_cell_configuration(i, j)

                # Create the cell
                cell = TerminalCell(title, generator, color)
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
            (self.generate_network_stats, "Network", "cyan"),
            (self.generate_cpu_stats, "CPU", "red"),
            (self.generate_memory_stats, "Memory", "magenta"),
            (self.generate_disk_stats, "Disk", "yellow"),
            (self.generate_processes, "Processes", "default"),
            (self.generate_weather, "Weather", "cyan"),
            (self.generate_quotes, "Quotes", "default"),
            (self.generate_calendar, "Calendar", "blue"),
            (self.generate_file_system, "Files", "yellow"),
            (self.generate_ip_info, "IP Info", "cyan"),
            (self.generate_battery_status, "Battery", "yellow"),
        ]

        # Calculate index based on row and col
        index = row * self.cols + col

        # Return generator, title, and color
        return generators[index]

    def generate_system_info(self) -> List[str]:
        """Generate system information"""
        try:
            output = subprocess.check_output(
                ["system_profiler", "SPSoftwareDataType"], universal_newlines=True
            )
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
            output = subprocess.check_output(
                ["top", "-l", "1", "-n", "0"], universal_newlines=True
            )
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

    def generate_file_system(self) -> List[str]:
        """Generate a file system listing"""
        try:
            output = subprocess.check_output(
                ["ls", "-la", os.environ.get("HOME", "/")], universal_newlines=True
            )
            return output.strip().split("\n")[:10]
        except:
            return ["File System Unavailable"]

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
            output = subprocess.check_output(
                ["pmset", "-g", "batt"], universal_newlines=True
            )
            return output.strip().split("\n")
        except:
            return ["Battery Status Unavailable"]

    def update_cells(self):
        """Update all cells"""
        for row in self.cells:
            for cell in row:
                cell.update()

    def generate_html_output(self):
        """Generate HTML output for the grid"""
        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Terminal Grid Screensaver</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: black;
            color: #33ff33;
            font-family: 'Courier New', monospace;
        }
        #content {
            display: grid;
            grid-template-columns: repeat(%COLS%, 1fr);
            grid-template-rows: repeat(%ROWS%, 1fr);
            width: 100vw;
            height: 100vh;
        }
        .cell {
            border: 1px solid #444;
            padding: 5px;
            overflow: hidden;
            background-color: #111;
            display: flex;
            flex-direction: column;
        }
        .cell-title {
            border-bottom: 1px solid #444;
            padding-bottom: 5px;
            margin-bottom: 5px;
            font-weight: bold;
        }
        .cell-content {
            flex-grow: 1;
            overflow: hidden;
        }
    </style>
</head>
<body>
    <div id="content">
""".replace(
            "%ROWS%", str(self.rows)
        ).replace(
            "%COLS%", str(self.cols)
        )

        # Add each cell's content
        for row in self.cells:
            for cell in row:
                html += cell.get_html_content()

        # Close the HTML
        html += """    </div>
</body>
</html>
"""

        # Write the HTML to the output file
        return html

    def run_once_html(self, rows=3, cols=3, width=800, height=600):
        self.update_cells()
        html = self.generate_html_output()
        return html

    def run(self, interval=5):
        """Run the screensaver"""
        # Hide the cursor

        # Main loop
        first = True
        while self.running:
            try:
                t0 = time.time()

                # Update all cells
                self.update_cells()

                # Generate HTML output if needed
                if self.web_output_path:
                    html = self.generate_html_output()
                    with open(self.web_output_path, "w") as f:
                        f.write(html)

                # Sleep for a bit
                duration = time.time() - t0
                sleep_for = max(0.1, interval - duration)
                print(f"Sleeping for {sleep_for}")
                if not first:
                    time.sleep(sleep_for)
                first = False
            except KeyboardInterrupt:
                self.running = False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Terminal Grid Screensaver")
    parser.add_argument("--rows", type=int, default=3, help="Number of rows")
    parser.add_argument("--cols", type=int, default=3, help="Number of columns")
    parser.add_argument("--interval", type=int, default=5, help="Refresh interval")
    parser.add_argument("--web-output", type=str, help="Path to write HTML output")
    args = parser.parse_args()

    # Run the screensaver
    # curses.wrapper(lambda stdscr: GridScreensaver(stdscr).run(rows=args.rows, cols=args.cols, interval=args.interval))
    # Create and run the screensaver
    screensaver = GridScreensaver(
        web_output_path=args.web_output, rows=args.rows, cols=args.cols
    )
    screensaver.run(interval=args.interval)


if __name__ == "__main__":
    main()
