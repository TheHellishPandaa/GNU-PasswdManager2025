# GNU-PasswdManager 2025
GNU-PasswdManager is a simple password manager built using Python and Tkinter. It allows users to store, generate, and manage their passwords securely. The passwords are encrypted using the Fernet symmetric encryption method from the `cryptography` library.


## Features
- Password encryption using `cryptography`.
- Graphical interface with `tkinter`.
- Random password generation.
- Secure storage in a JSON file.
- User Registration: We added a registration feature to create new users.
- User Login: Allows users to authenticate with their username and password.
- Authentication and Restricted Access: Each user can only view and manage their own passwords.
  
## Requirements
Install cryptography dependencies using:
```bash
pip install cryptography
```
## Install Python on Windows 10/11:
1. Go to the official Python website: https://www.python.org/downloads/.
2. On the main page, you will see a button to download the latest stable version of Python. Click on the button that says "Download Python X.X.X" (where "X.X.X" is the version number).

# Installing Python on macOS

Follow these steps to install Python on your macOS machine:

## 1. Check if Python is Already Installed

Before installing Python, check if it's already installed on your system. Open the **Terminal** (you can find it by searching in Spotlight or in `Applications > Utilities`), and run the following command:

```bash
python3 --version
```
Step 2: Install Python

Once Homebrew is installed, you can install Python by running the following command in the Terminal:
```
brew install python
```
Homebrew will install the latest version of Python 3 and pip (Python's package installer).

3. Verify the Installation

After the installation is complete, you can verify that Python is installed correctly by checking the version again:
```
python3 --version
```
4. Install and Use pip

pip is the Python package manager used to install libraries and dependencies. If pip is not installed automatically, you can install or upgrade it by running:
````
python3 -m ensurepip --upgrade
````
This should return the version of Python you just installed.

# Installing Python on Linux

Follow these steps to install Python on your Linux system:

## 1. Check if Python is Already Installed

Most Linux distributions come with Python pre-installed. To check if Python is installed, open a **terminal** and run:

```bash
python3 --version
````

## 2. Install Python

Run the following command to install Python 3:

For Debian-based distributions (e.g., Ubuntu):

```
sudo apt install -y python3 python3-pip
````
For Red Hat-based distributions (e.g., Fedora, CentOS):

````
sudo dnf install -y python3 python3-pip
````
## 3. Verify the Installation

Once the installation is complete, verify it by checking the Python version:

````
python3 --version
````
Also, check if pip is installed:

````
pip3 --version
````

## Run the Installer (for Windows 10/11)

Run the installer you downloaded (it will be a .exe file).
    
  1. Click on "Install Now" to start the standard installation.

  2. The installation process will begin. Wait for it to complete. Once finished, you will see a message saying "Setup was successful".
     
## Verify the Installation

 Open the Command Prompt in Windows (you can search for "cmd" in the Start menu).

  Type the following command to verify that Python is installed correctly:
```bash

python --version
```

Or you can also try:
```bash
python3 --version
```
If Python is installed correctly, you should see something like:

Python 3.X.X

 (Where "3.X.X" is the version you installed).
 
 ## Verify pip (Python Package Manager)

pip is the tool used to install Python packages. Check if pip is installed by running:

```bash
pip --version
```
If it shows the version of pip, it is installed correctly. If not, you can install pip manually, but it usually comes installed with Python


## Execute this Script

On Windows 10/11 Open the Command Prompt/PowerShell in Windows (you can search for "cmd" in the Start menu) and put the follow command.
```bash
python GNU-PasswdManager.py
```

## For Spannish Language use the "esp" folder.
```bash
cd esp
```

Then, Execute the script

```bash
python GNU-PasswdManager.py
```

## On linux/Mac

```bash
python3 GNU-PasswdManager.py
```

## LISENCE

This program is released under GNU General Public License 

© 2025 Jaime Galvez Martinez (GNU General Public License)
