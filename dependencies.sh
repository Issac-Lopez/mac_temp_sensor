#!/bin/bash

# Check if Homebrew is installed, if not, install Homebrew
if test ! $(which brew); then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Check if Python 3 is installed, if not, install Python 3
if test ! $(which python3); then
    echo "Installing Python 3..."
    brew install python3
fi

# Check if LLVM is installed, if not, install LLVM
if test ! $(which gcc); then
    echo "Installing LLVM and Clang..."
    brew install gcc
fi

# Add GCC to the PATH
echo 'export PATH="/usr/local/opt/gcc/bin:$PATH"' >> ~/.bash_profile
echo 'export PATH="/usr/local/opt/python3/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile

echo "Homebrew, Python 3, and GCC have been installed."