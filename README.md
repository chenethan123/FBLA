# MAC INSTALLATION AND RUNNING GUIDE
## Step 1: Install Homebrew
Homebrew is a package manager for macOS that makes it easy to install software. Open Terminal and run:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

(Copy and paste the entire line)
Follow the on-screen instructions to complete the installation.
## Step 2: Install Python
Once Homebrew is installed, you can easily install Python:
brew install python

This will install Python and pip (Python’s package installer), which you can use to install other Python libraries.
## Step 3: Verify Python Installation
To verify Python has been installed correctly, run:

python3 --version

This should display the Python version number.
## Step 4: Install Tkinter
Tkinter should come pre-installed with Python's standard library for Python versions 3.1 and above. If for any reason Tkinter is not installed, it can usually be installed via Python itself:
python3 -m tkinter

A small window should open, indicating Tkinter is installed. If not, you might need to reinstall Python from python.org, where Tkinter is included.
## Step 5: Download the GitHub File or Repository
Navigate to the GitHub page containing the file or repository you wish to download. Click on the green “Code” button, then select “Download ZIP.” Once downloaded, unzip the file in your desired location.
## Step 6: Navigate to the Project Directory
Open Terminal, and navigate to the project directory using the cd command. For example, if your project is located in Downloads folder and named project-folder, run:
cd ~/Downloads/FBLA

## Step 7: Run the Python File
Once in the correct directory, run the Python file using:
python3 main.py


# WINDOWS GUIDE

## Step 1: Install Python
Download Python Installer:
Visit the official Python website and click on the "Downloads" tab. Choose the latest version of Python for Windows and download the installer.
Run the Installer:
Double-click on the downloaded installer file (e.g., python-3.x.x.exe) to run the Python installer.
Check "Add Python to PATH":
During the installation process, make sure to check the box that says "Add Python to PATH." This option is important as it allows you to use Python from the command line.
Complete Installation:
Follow the on-screen instructions to complete the installation. Click "Install Now" when prompted.
Verify Installation:
Open a Command Prompt and type python --version or python -V to check that Python has been installed successfully.
## Step 2: Check if Tkinter is installed 
Tkinter should come pre-installed with Python's standard library for Python versions 3.1 and above. If for any reason Tkinter is not installed, it can usually be installed via Python itself:
python3 -m tkinter

A small window should open, indicating Tkinter is installed. If not, you might need to reinstall Python from python.org, where Tkinter is included.

## Step 3: Download the GitHub File or Repository
Navigate to the GitHub page containing the file or repository you wish to download. Click on the green “Code” button, then select “Download ZIP.” Once downloaded, unzip the file in your desired location.
Step 4: Navigate to the Project Directory
Open Terminal, and navigate to the project directory using the cd command. For example, if your project is located in Downloads folder and named project-folder, run:
cd ~/Downloads/FBLA

## Step 5: Run the Python File
Once in the correct directory, run the Python file using:
python3 main.py












