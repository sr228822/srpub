#!/bin/bash
# Setup script for Terminal Grid Screensaver

# Set script variables
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
INSTALL_DIR="$HOME/.terminal-grid-screensaver"
BIN_DIR="/usr/local/bin"
PYTHON_SCRIPT="terminal_grid_screensaver.py"
LAUNCHER_SCRIPT="launch_screensaver.sh"
PLIST_FILE="com.user.terminal-grid-screensaver.plist"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print header
echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}   Terminal Grid Screensaver Setup      ${NC}"
echo -e "${BLUE}=========================================${NC}"
echo

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3 and try again.${NC}"
    exit 1
fi

# Create installation directory
echo -e "Creating installation directory at ${INSTALL_DIR}..."
mkdir -p "${INSTALL_DIR}"
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to create installation directory.${NC}"
    exit 1
fi

# Copy Python script to installation directory
echo -e "Copying screensaver script..."
cp "${SCRIPT_DIR}/${PYTHON_SCRIPT}" "${INSTALL_DIR}/"
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to copy screensaver script.${NC}"
    exit 1
fi
chmod +x "${INSTALL_DIR}/${PYTHON_SCRIPT}"

# Create the launcher script
echo -e "Creating launcher script..."
cat > "${INSTALL_DIR}/${LAUNCHER_SCRIPT}" << EOF
#!/bin/bash
# Launcher for Terminal Grid Screensaver

# Set terminal to fullscreen
osascript -e 'tell application "Terminal" to set fullscreen of front window to true'

# Change to the screensaver directory
cd "${INSTALL_DIR}"

# Run the screensaver
python3 "${PYTHON_SCRIPT}"

# Exit fullscreen mode when done
osascript -e 'tell application "Terminal" to set fullscreen of front window to false'
EOF
chmod +x "${INSTALL_DIR}/${LAUNCHER_SCRIPT}"

# Create a symbolic link to the launcher script
echo -e "Creating symbolic link in ${BIN_DIR}..."
if [ -w "${BIN_DIR}" ]; then
    ln -sf "${INSTALL_DIR}/${LAUNCHER_SCRIPT}" "${BIN_DIR}/terminal-grid-screensaver"
else
    echo -e "${RED}Cannot create symbolic link in ${BIN_DIR}. You may need to run this script with sudo.${NC}"
    echo -e "You can manually run the screensaver with: ${INSTALL_DIR}/${LAUNCHER_SCRIPT}"
fi

# Create LaunchAgent plist file for screensaver integration
echo -e "Creating LaunchAgent plist file..."
cat > "${INSTALL_DIR}/${PLIST_FILE}" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.terminal-grid-screensaver</string>
    <key>ProgramArguments</key>
    <array>
        <string>${INSTALL_DIR}/${LAUNCHER_SCRIPT}</string>
    </array>
    <key>RunAtLoad</key>
    <false/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>
EOF

# Create LaunchAgents directory if it doesn't exist
mkdir -p "${HOME}/Library/LaunchAgents"

# Copy plist file to LaunchAgents directory
cp "${INSTALL_DIR}/${PLIST_FILE}" "${HOME}/Library/LaunchAgents/"
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to copy plist file to LaunchAgents directory.${NC}"
    exit 1
fi

# Print success message
echo -e "${GREEN}Installation successful!${NC}"
echo
echo -e "You can run the screensaver manually with the command: ${BLUE}terminal-grid-screensaver${NC}"
echo
echo -e "To use this as your screensaver, you'll need to set up a hotkey or use a third-party tool like 'Hammerspoon' to trigger it when the screensaver activates."
echo
echo -e "Example Hammerspoon configuration (add to your init.lua file):"
echo -e "${BLUE}"
echo "-- Terminal Grid Screensaver integration"
echo "local idleTimer = hs.timer.delayed.new(300, function()"
echo "    hs.execute('terminal-grid-screensaver')"
echo "end)"
echo
echo "hs.caffeinate.watcher.new(function(event)"
echo "    if event == hs.caffeinate.watcher.screensaverDidStart then"
echo "        hs.execute('terminal-grid-screensaver')"
echo "    elseif event == hs.caffeinate.watcher.screensaverDidStop then"
echo "        -- Nothing to do here"
echo "    elseif event == hs.caffeinate.watcher.screensaverWillStop then"
echo "        -- Nothing to do here"
echo "    end"
echo "end):start()"
echo
echo "-- Reset idle timer on activity"
echo "activityWatcher = hs.eventtap.new({hs.eventtap.event.types.mouseMoved, hs.eventtap.event.types.keyDown}, function()"
echo "    idleTimer:stop()"
echo "    idleTimer:start()"
echo "    return false"
echo "end)"
echo "activityWatcher:start()"
echo -e "${NC}"
echo
echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}   Setup Complete                       ${NC}"
echo -e "${BLUE}=========================================${NC}"
echo
