# VolunteerHub Download and Setup Guide

This guide explains how to download and run the VolunteerHub project on another computer.

## Project Link

```text
https://github.com/Swastik-4752/VMS.git
```

## What This Project Needs

Install these before starting:

- Python 3.10 or newer
- Git
- A code editor such as VS Code
- A web browser such as Chrome, Edge, or Firefox

To check Python and Git installation, open Command Prompt or Terminal and run:

```bash
python --version
git --version
```

On some macOS or Linux systems, use:

```bash
python3 --version
git --version
```

## Method 1: Download Using Git

This is the recommended method.

### Step 1: Open Terminal

On Windows, open Command Prompt, PowerShell, or VS Code Terminal.

### Step 2: Go to the Folder Where You Want the Project

Example:

```bash
cd Desktop
```

### Step 3: Clone the Repository

```bash
git clone https://github.com/Swastik-4752/VMS.git
```

### Step 4: Open the Project Folder

```bash
cd VMS
```

## Method 2: Download as ZIP

Use this method if Git is not installed.

1. Open this link in the browser:

```text
https://github.com/Swastik-4752/VMS
```

2. Click the green `Code` button.
3. Click `Download ZIP`.
4. Extract the ZIP file.
5. Open the extracted folder in VS Code or Terminal.

## Setup on Windows

Run these commands inside the project folder.

### Step 1: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 2: Activate the Virtual Environment

```bash
.venv\Scripts\activate
```

After activation, you should see `(.venv)` at the start of the terminal line.

### Step 3: Install Required Packages

```bash
pip install -r requirements.txt
```

### Step 4: Run the Project

```bash
python app.py
```

### Step 5: Open in Browser

Open this URL:

```text
http://127.0.0.1:5000
```

## Setup on macOS or Linux

Run these commands inside the project folder.

### Step 1: Create a Virtual Environment

```bash
python3 -m venv .venv
```

### Step 2: Activate the Virtual Environment

```bash
source .venv/bin/activate
```

### Step 3: Install Required Packages

```bash
pip install -r requirements.txt
```

### Step 4: Run the Project

```bash
python3 app.py
```

### Step 5: Open in Browser

Open this URL:

```text
http://127.0.0.1:5000
```

## Login Details

The project automatically creates a default admin account.

```text
Username: admin
Password: admin123
```

Admin login page:

```text
http://127.0.0.1:5000/login
```

Volunteer login page:

```text
http://127.0.0.1:5000/volunteer/login
```

Signup page:

```text
http://127.0.0.1:5000/signup
```

## How the Database Works

The project uses SQLite. When the project runs for the first time, it creates the database automatically here:

```text
instance/volunteer_db.sqlite
```

You do not need to create the database manually.

If you want to reset all data:

1. Stop the running server.
2. Delete this file:

```text
instance/volunteer_db.sqlite
```

3. Run the project again:

```bash
python app.py
```

The default sample data and admin account will be created again.

## Useful Commands

Check if the code files have syntax errors:

```bash
python -m compileall app.py models.py
```

Install dependencies again if needed:

```bash
pip install -r requirements.txt
```

Deactivate the virtual environment:

```bash
deactivate
```

## Common Problems and Fixes

### Problem: `python` is not recognized

Install Python from:

```text
https://www.python.org/downloads/
```

During installation on Windows, enable `Add Python to PATH`.

### Problem: `git` is not recognized

Install Git from:

```text
https://git-scm.com/downloads
```

Then close and reopen the terminal.

### Problem: `pip` is not recognized

Try:

```bash
python -m pip install -r requirements.txt
```

On macOS or Linux:

```bash
python3 -m pip install -r requirements.txt
```

### Problem: Port 5000 is already in use

Close the other program using port 5000, or stop the old Flask server and run again:

```bash
python app.py
```

### Problem: Virtual environment does not activate on Windows PowerShell

Run this command:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```bash
.venv\Scripts\activate
```

## Final Checklist

Before saying setup is complete, confirm these are working:

- The project folder is downloaded.
- The virtual environment is activated.
- `pip install -r requirements.txt` completed successfully.
- `python app.py` starts the Flask server.
- `http://127.0.0.1:5000` opens in the browser.
- Admin login works with `admin` and `admin123`.
