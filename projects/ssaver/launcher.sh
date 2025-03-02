#!/bin/bash
# Improved launcher for Terminal Grid Screensaver

# Path to the screensaver script
SCREENSAVER_DIR="$HOME/.terminal-grid-screensaver"
SCREENSAVER_SCRIPT="terminal_grid_screensaver.py"

# Create a new Terminal window and make it fullscreen
osascript <<EOF
tell application "Terminal"
    # Activate Terminal
    activate
    
    # Create a new window
    do script ""
    
    # Get the ID of the current window
    set currentWindow to front window
    
    # Set properties for better appearance
    set background color of currentWindow to {0, 0, 0}
    set normal text color of currentWindow to {50000, 50000, 50000}
    set custom title of currentWindow to "Terminal Grid Screensaver"
    
    # Go fullscreen - more reliable method
    tell application "System Events"
        keystroke "f" using {command down, control down}
    end tell
    
    # Small delay to ensure fullscreen completes
    delay 0.5
end tell
EOF

# Execute the screensaver in the new Terminal window
osascript <<EOF
tell application "Terminal"
    # Run the screensaver in the frontmost window
    do script "cd '${SCREENSAVER_DIR}' && python3 '${SCREENSAVER_SCRIPT}'" in front window
end tell
EOF

# Keep this script running until user exits the screensaver
# The terminal will close automatically when the Python script exits
wait
