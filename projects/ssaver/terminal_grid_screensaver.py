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
import psutil
import sys
from typing import List, Callable

# Add parent directory to path for importing srutils and dfs
sys.path.append(os.path.expanduser("~/srpub"))
import subway
import dfs
import weather

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


def create_bar(percent, width=30):
    """Create a text-based percentage bar"""
    filled_width = int(width * percent / 100)
    bar = "#" * filled_width + "_" * (width - filled_width)
    return f"[{bar}] {percent:.1f}%"


class CellConfig:
    """Configuration for a terminal cell"""

    def __init__(
        self,
        generator: Callable,
        title: str,
        color: str = "default",
        row_span: int = 1,
        col_span: int = 1,
    ):
        """
        Initialize a cell configuration

        Args:
            generator: Function that generates content for the cell
            title: The title to display at the top of the cell
            color: The color scheme to use
            row_span: Number of rows the cell should span
            col_span: Number of columns the cell should span
        """
        self.generator = generator
        self.title = title
        self.color = color
        self.row_span = row_span
        self.col_span = col_span


class TerminalCell:
    """A single cell in the terminal grid"""

    def __init__(self, config: CellConfig):
        """
        Initialize a terminal cell

        Args:
            config: The configuration for this cell
        """
        self.title = config.title
        self.content_generator = config.generator
        self.color = config.color
        self.content_lines = []
        self.max_lines = 40  # Default for web output
        self.max_cols = 300  # Default for web output
        self.row_span = config.row_span
        self.col_span = config.col_span

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
        # Add grid-row and grid-column span if needed
        grid_style = ""
        if self.row_span > 1:
            grid_style += f"grid-row: span {self.row_span};"
        if self.col_span > 1:
            grid_style += f"grid-column: span {self.col_span};"

        html = f'<div class="cell" style="color: {HTML_COLORS.get(self.color, "#FFFFFF")};{grid_style}">\n'
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
        self.cell_map = {}  # Track which positions are filled due to spanning cells

        for i in range(rows):
            row_cells = []
            for j in range(cols):
                # Skip positions that are already filled by spanning cells
                if self.cell_map.get((i, j)):
                    row_cells.append(None)
                    continue

                # Get cell configuration
                config = self.get_cell_configuration(i, j)

                # Create the cell
                cell = TerminalCell(config)
                row_cells.append(cell)

                # Mark positions this cell spans as filled
                for r in range(i, min(i + config.row_span, rows)):
                    for c in range(j, min(j + config.col_span, cols)):
                        if r > i or c > j:  # Don't mark the cell's own position
                            self.cell_map[(r, c)] = True

            self.cells.append(row_cells)

    def get_cell_configuration(self, row: int, col: int) -> CellConfig:
        """
        Get the configuration for a cell

        Args:
            row: The row of the cell
            col: The column of the cell

        Returns:
            A CellConfig object
        """
        # Define cell configurations with their properties
        configs = [
            CellConfig(self.generate_system_info, "System Info", "default"),
            CellConfig(self.generate_clock, "Clock", "default"),
            CellConfig(self.gen_systemstats, "System Stats", "default"),
            # Make subway span 2 rows
            CellConfig(self.generate_subway, "Subway", "default", row_span=2),
            # CellConfig(self.generate_network_stats, "Network", "default"),
            # CellConfig(self.generate_cpu_stats, "CPU", "default"),
            # CellConfig(self.generate_memory_stats, "Memory", "default"),
            # CellConfig(self.generate_disk_stats, "Disk", "default"),
            CellConfig(self.generate_processes, "Processes", "default"),
            CellConfig(self.generate_weather, "Weather", "default"),
            CellConfig(self.generate_empty, "Empty", "default"),
            CellConfig(self.generate_quotes, "Quotes", "default"),
            CellConfig(self.generate_calendar, "Calendar", "default"),
            # CellConfig(self.generate_file_system, "Files", "default"),
            CellConfig(self.generate_ip_info, "IP Info", "default"),
            # CellConfig(self.generate_battery_status, "Battery", "default"),
        ]

        # Calculate index based on row and col
        index = row * self.cols + col

        # If the index exceeds the number of configurations, use the first one
        if index >= len(configs):
            return configs[0]

        return configs[index]

    def generate_empty(self) -> List[str]:
        return [""]

    def generate_system_info(self) -> List[str]:
        """Generate system information"""
        try:
            output = subprocess.check_output(
                ["system_profiler", "SPSoftwareDataType"], universal_newlines=True
            )
            return output.strip().split("\n")[:10]
        except Exception as e:
            return ["System Info Unavailable", str(e)]

    def generate_clock(self) -> List[str]:
        """Generate a clock display with multiple time zones"""
        import datetime
        import pytz

        # Define time zones we want to display (name, timezone)
        timezones = [
            ("Local", None),  # Use None for local timezone
            ("SFO", "America/Los_Angeles"),
            ("New York", "America/New_York"),
            ("London", "Europe/London"),
            ("UTC", "UTC"),
            ("Tokyo", "Asia/Tokyo"),
        ]

        # Get current UTC time
        utc_now = datetime.datetime.now(datetime.timezone.utc)

        # Format for local time
        local_now = datetime.datetime.now()
        local_date = local_now.date()
        date_str = local_now.strftime("%A, %B %d, %Y")

        output = []
        output.append(f"Date: {date_str}")
        output.append("")
        output.append("Time Zones:")

        # Find max length of timezone names for padding
        max_name_length = max(len(name) for name, _ in timezones)

        # Add line for each timezone
        for name, tz_name in timezones:
            if tz_name is None:
                # Local time
                current_time = local_now
            else:
                # Convert UTC time to the target timezone
                try:
                    tz = pytz.timezone(tz_name)
                    current_time = utc_now.astimezone(tz)
                except Exception:
                    output.append(f"  {name.ljust(max_name_length)}: Error")
                    continue

            # Check if date is different from local date
            different_date = current_time.date() != local_date
            date_indicator = " *" if different_date else ""

            # Format the time in both 24h and 12h formats
            time_24h = current_time.strftime("%H:%M:%S")
            time_12h = current_time.strftime("%I:%M %p")

            # Use HTML-safe formatting with non-breaking spaces
            padded_name = name + "&nbsp;" * (max_name_length - len(name))
            output.append(f"  {padded_name} : {time_24h} ({time_12h}){date_indicator}")

        output.append("")
        output.append("* Different date than local")

        return output

    def gen_systemstats(self):
        output = []

        # CPU usage
        try:
            cpu_times = psutil.cpu_times_percent(interval=0.5)
            user = cpu_times.user
            system = cpu_times.system
            idle = cpu_times.idle
            output.append(
                f"CPU usage: {user:.2f}% user, {system:.2f}% sys, {idle:.2f}% idle"
            )

            # CPU percentage bar
            used_cpu = user + system
            cpu_bar = create_bar(used_cpu)
            output.append(f"  {cpu_bar}")
        except Exception as e:
            output.append(f"CPU stats unavailable: {str(e)}")

        # Memory usage
        try:
            memory = psutil.virtual_memory()
            output.append(f"Memory: {memory.percent:.2f}% used")

            # Memory percentage bar
            memory_bar = create_bar(memory.percent)
            output.append(f"  {memory_bar}")
        except Exception as e:
            output.append(f"Memory stats unavailable: {str(e)}")

        # Disk usage - using dfs module
        try:
            # Use the dfs module from srutils
            usage = dfs.get_disk_usage("/")

            # Convert to GB for display
            total_gb = usage.total / (1024**3)
            used_gb = usage.used / (1024**3)
            free_gb = usage.free / (1024**3)

            output.append(
                f"Disk: total={total_gb:.1f}GB used={used_gb:.1f}GB free={free_gb:.1f}GB"
            )

            disk_bar = create_bar(usage.percent)
            output.append(f"  {disk_bar}")
        except Exception as e:
            output.append(f"Disk stats unavailable: {str(e)}")

        # Battery stats
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                power_plugged = battery.power_plugged
                status = "Charging" if power_plugged else "Discharging"

                # Format time remaining if discharging
                if (
                    not power_plugged
                    and battery.secsleft != psutil.POWER_TIME_UNLIMITED
                ):
                    m, s = divmod(battery.secsleft, 60)
                    h, m = divmod(m, 60)
                    time_left = f"{h:d}:{m:02d}"
                    output.append(
                        f"Battery: {percent}% ({status}, {time_left} remaining)"
                    )
                else:
                    output.append(f"Battery: {percent}% ({status})")

                # Battery percentage bar
                battery_bar = create_bar(percent)
                output.append(f"  {battery_bar}")
            else:
                output.append("Battery: Not detected")
        except Exception as e:
            output.append(f"Battery stats unavailable: {str(e)}")

        # Network stats
        try:
            net_io = psutil.net_io_counters()
            sent_mb = net_io.bytes_sent / (1024**2)
            recv_mb = net_io.bytes_recv / (1024**2)
            output.append(f"Network: ↑ {sent_mb:.2f}MB sent ↓ {recv_mb:.2f}MB received")
        except Exception as e:
            output.append(f"Network stats unavailable: {str(e)}")

        return output

    def generate_network_stats(self) -> List[str]:
        """Generate network statistics"""
        try:
            output = subprocess.check_output(["netstat", "-i"], universal_newlines=True)
            return output.strip().split("\n")[:10]
        except Exception as e:
            return ["Network Stats Unavailable", str(e)]

    def generate_cpu_stats(self) -> List[str]:
        """Generate CPU statistics"""
        try:
            output = subprocess.check_output(
                ["top", "-l", "1", "-n", "0"], universal_newlines=True
            )
            cpu_lines = [line for line in output.split("\n") if "CPU usage" in line]
            return ["CPU Statistics:"] + cpu_lines
        except Exception as e:
            return ["CPU Stats Unavailable", str(e)]

    def generate_subway(self) -> List[str]:
        try:
            # Use the HTML version for web output
            output = subway.get_subway_status_formatted(as_html=True, linelimit=1)
            return output.split("\n")
        except Exception as e:
            return ["Subway status unavailable", str(e)]

    def generate_memory_stats(self) -> List[str]:
        """Generate memory statistics"""
        try:
            output = subprocess.check_output(["vm_stat"], universal_newlines=True)
            return output.strip().split("\n")[:10]
        except Exception as e:
            return ["Memory Stats Unavailable", str(e)]

    def generate_disk_stats(self) -> List[str]:
        """Generate disk statistics"""
        try:
            output = subprocess.check_output(["df", "-h"], universal_newlines=True)
            return output.strip().split("\n")[:10]
        except Exception as e:
            return ["Disk Stats Unavailable", str(e)]

    def generate_processes(self) -> List[str]:
        """Generate a list of processes"""
        try:
            output = subprocess.check_output(["ps", "-ef"], universal_newlines=True)
            return output.strip().split("\n")[:10]
        except Exception as e:
            return ["Process List Unavailable", str(e)]

    def generate_weather(self) -> List[str]:
        """Generate real weather information using the weather module"""
        # Use the imported weather module to get real weather data
        return weather.get_weather()

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
        except Exception as e:
            return ["Calendar Unavailable", str(e)]

    def generate_file_system(self) -> List[str]:
        """Generate a file system listing"""
        try:
            output = subprocess.check_output(
                ["ls", "-la", os.environ.get("HOME", "/")], universal_newlines=True
            )
            return output.strip().split("\n")[:10]
        except Exception as e:
            return ["File System Unavailable", str(e)]

    def generate_ip_info(self) -> List[str]:
        """Generate IP information"""
        try:
            output = subprocess.check_output(["ifconfig"], universal_newlines=True)
            ip_lines = []
            for line in output.strip().split("\n"):
                if "inet " in line and "127.0.0.1" not in line:
                    ip_lines.append(line.strip())
            return ["IP Addresses:"] + ip_lines[:10]
        except Exception as e:
            return ["IP Info Unavailable", str(e)]

    def generate_battery_status(self) -> List[str]:
        """Generate battery status"""
        try:
            output = subprocess.check_output(
                ["pmset", "-g", "batt"], universal_newlines=True
            )
            return output.strip().split("\n")
        except Exception as e:
            return ["Battery Status Unavailable", str(e)]

    def update_cells(self):
        """Update all cells"""
        for row in self.cells:
            for cell in row:
                if cell:  # Skip None cells (those filled by spanning cells)
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
            font-size: 14px;
        }
        #content {
            display: grid;
            grid-template-columns: repeat(%COLS%, 1fr);
            grid-template-rows: repeat(%ROWS%, 1fr);
            width: 100vw;
            height: 100vh;
            gap: 5px;
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
                if cell:  # Skip None cells (those filled by spanning cells)
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
