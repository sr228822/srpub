#!/bin/bash
set -e

OS="$(uname)"
if [ "$OS" != "Darwin" ] && [ "$OS" != "Linux" ]; then
    echo "Error: This script supports macOS and Linux only."
    exit 1
fi

SRPUB_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Quick Setup (srpub: $SRPUB_DIR) ==="

# 1. Install packages
echo ""
echo "--- Packages ---"
PACKAGES=(tmux wget jq htop tree)
if [ "$OS" = "Darwin" ]; then
    if command -v brew &>/dev/null; then
        echo "Homebrew already installed."
    else
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    echo "Updating and upgrading brew..."
    brew update
    brew upgrade
    for pkg in "${PACKAGES[@]}"; do
        if brew list "$pkg" &>/dev/null; then
            echo "$pkg already installed, skipping."
        else
            echo "Installing $pkg..."
            brew install "$pkg"
        fi
    done
else
    echo "Updating and upgrading apt packages..."
    sudo apt-get update -qq
    sudo apt-get upgrade -y -qq
    for pkg in "${PACKAGES[@]}"; do
        if dpkg -s "$pkg" &>/dev/null; then
            echo "$pkg already installed, skipping."
        else
            echo "Installing $pkg..."
            sudo apt-get install -y -qq "$pkg"
        fi
    done
fi

# 2. Install Docker
echo ""
echo "--- Docker ---"
if command -v docker &>/dev/null; then
    echo "Docker already installed."
else
    echo "Installing Docker..."
    if [ "$OS" = "Darwin" ]; then
        brew install --cask docker
        echo "Docker Desktop installed. You may need to open it manually to finish setup."
    else
        curl -fsSL https://get.docker.com | sh
        sudo usermod -aG docker "$USER"
        echo "Docker installed. You may need to log out and back in for group changes."
    fi
fi

# 3. Install Miniconda
echo ""
echo "--- Miniconda ---"
if command -v conda &>/dev/null; then
    echo "Conda already installed, skipping."
else
    echo "Installing Miniconda..."
    ARCH=$(uname -m)
    if [ "$OS" = "Darwin" ]; then
        if [ "$ARCH" = "arm64" ]; then
            CONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh"
        else
            CONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
        fi
    else
        if [ "$ARCH" = "aarch64" ]; then
            CONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh"
        else
            CONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
        fi
    fi
    curl -fsSL "$CONDA_URL" -o /tmp/miniconda.sh
    bash /tmp/miniconda.sh -b -p "$HOME/miniconda3"
    rm /tmp/miniconda.sh
    eval "$("$HOME/miniconda3/bin/conda" shell.bash hook)"
fi

# 4. Create samdev conda env
echo ""
echo "--- Conda env: samdev ---"
if conda env list | grep -q "^samdev "; then
    echo "samdev env already exists, skipping."
else
    echo "Creating samdev env from environment.yml..."
    conda env create -f "$SRPUB_DIR/environment.yml"
fi

# 5. Set up shell rc file
if [ "$OS" = "Darwin" ]; then
    SHELL_RC="$HOME/.zshrc"
else
    SHELL_RC="$HOME/.bashrc"
fi

echo ""
echo "--- $SHELL_RC ---"
SRPUB_SOURCE="source $SRPUB_DIR/bashrc"
SECRETS_SOURCE="source ~/.secretsrc"

if [ ! -f "$SHELL_RC" ]; then
    touch "$SHELL_RC"
fi

if grep -qF "$SRPUB_SOURCE" "$SHELL_RC"; then
    echo "srpub bashrc source line already present, skipping."
else
    echo "Adding srpub bashrc source line to $SHELL_RC..."
    echo "$SRPUB_SOURCE" >> "$SHELL_RC"
fi

if grep -qF "$SECRETS_SOURCE" "$SHELL_RC"; then
    echo "secretsrc source line already present, skipping."
else
    echo "Adding secretsrc source line to $SHELL_RC..."
    echo "$SECRETS_SOURCE" >> "$SHELL_RC"
fi

# 6. Copy configs
echo ""
echo "--- Config files ---"
for pair in vimrc:.vimrc condarc:.condarc psqlrc:.psqlrc; do
    src="${pair%%:*}"
    dest="$HOME/${pair#*:}"
    if [ -f "$dest" ]; then
        echo "$dest already exists, skipping."
    else
        echo "Copying $src -> $dest"
        cp "$SRPUB_DIR/other_config/$src" "$dest"
    fi
done

# 7. Configure git hooks
echo ""
echo "--- Git hooks ---"
git -C "$SRPUB_DIR" config core.hooksPath "$SRPUB_DIR/hooks"
echo "Set core.hooksPath to $SRPUB_DIR/hooks"

echo ""
echo "=== Setup complete ==="
