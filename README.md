A small repo holding:
* dotfiles
* helper scripts
* code samples

Probably not of much interest to others.

# Linting/Formatting
Linted with pyfmt (black==22.12.0)

# Conda Setup
## Intel mac
curl -OL "https://repo.continuum.io/miniconda/Miniconda3-py38_4.12.0-MacOSX-x86_64.sh"
bash Miniconda3-py38_4.12.0-MacOSX-x86_64.sh -p ~/miniconda3 -b

## ARM mac
curl -OL "https://repo.continuum.io/miniconda/Miniconda3-py38_4.12.0-MacOSX-arm64.sh"
bash Miniconda3-py38_4.12.0-MacOSX-arm64.sh -p ~/miniconda3 -b

## Linux
wget https://repo.continuum.io/miniconda/Miniconda3-py38_4.12.0-Linux-x86_64.sh;
bash Miniconda3-py38_4.12.0-Linux-x86_64.sh -p ~/miniconda3 -b

## Create environment from yaml
conda env create -f environment.yml

