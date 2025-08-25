# MCIT AI Agents Workshop Series - Setup Guide

## Overview

This guide provides comprehensive setup instructions for the MCIT AI Agents workshop series, covering all prerequisites for building production-ready AI agents using the Gemini CLI. Follow this guide before Workshop 1 to ensure a smooth learning experience.

---

## System Requirements

### Hardware Requirements
- **Memory**: 8GB RAM minimum, 16GB recommended
- **Storage**: 10GB free space for tools and dependencies
- **Processor**: Modern multi-core CPU (Intel i5/AMD Ryzen 5 or better)
- **Network**: Stable internet connection for API calls and cloud services

### Operating System Support
- **macOS**: 10.14 (Mojave) or later *(primary setup method)*
- **Linux**: Ubuntu 18.04+, Debian 10+ or equivalent
- **Windows**: Windows 10/11 with WSL2 enabled

---

## Setup Overview

### What This Guide Does
This setup guide will prepare your development environment for the MCIT AI Agents Workshop Series. By the end, you'll have a fully functional environment ready to build and deploy AI agents using the Gemini CLI.

### What You'll Have After Setup
- ✅ **Python 3.9+** development environment
- ✅ **Git** for version control and collaboration  
- ✅ **Node.js 20** via NVM for modern JavaScript tooling
- ✅ **Gemini CLI** connected and ready to use
- ✅ **Development IDE** (VS Code) configured
- ✅ **Workshop environment** verified and tested

### Setup Process (Est. 30-45 minutes)
1. **Discover Terminal** - Find and setup your command line interface
2. **Install VS Code** - Set up your development environment
3. **Create Project Folder** - Organize your workspace
4. **Navigate to Directory** - Learn basic terminal navigation
5. **Install Package Manager** - Set up software installation tools
6. **Install Git** - Set up version control
7. **Clone Repository** - Download workshop materials
8. **Enter Project Folder** - Navigate to workshop directory
9. **Install Python** - Set up Python development environment
10. **Run Verification** - Test your setup so far
11. **Install NVM** - Set up Node.js version management
12. **Install Gemini CLI** - Set up the AI CLI tool

### Before You Start
- Ensure you have administrator access on your machine
- Have a stable internet connection for downloading tools
- Be patient - some installations may take several minutes

---

## Choose Your Operating System

Click your operating system to jump to the appropriate setup instructions:

### 🍎 [macOS Setup](#macos-setup)
### 🪟 [Windows Setup](#windows-setup)  
### 🐧 [Linux Setup](#linux-setup)

---

## macOS Setup

### Step 1: Find and Open Terminal

**Find Terminal using Spotlight:**
1. Click the magnifying glass icon (🔍) in the top-right corner of your screen
2. Type "Terminal"
3. Click on "Terminal" when it appears
4. A black window will open - this is your Terminal

**Alternative method:**
1. Open Finder (folder icon in dock)
2. Go to Applications folder
3. Open Utilities folder
4. Double-click Terminal

**Verify Terminal is open:**
You should see a window with text ending in `$` - this is your command prompt

### Step 2: Setup Shell Profile

**Detect current shell and create appropriate profile:**
```bash
CURRENT_SHELL=$(basename "$SHELL")
if [[ "$CURRENT_SHELL" == "zsh" ]]; then
    PROFILE_FILE="$HOME/.zshrc"
elif [[ "$CURRENT_SHELL" == "bash" ]]; then
    PROFILE_FILE="$HOME/.bashrc"
else
    PROFILE_FILE="$HOME/.profile"
fi

if [[ -f "$PROFILE_FILE" ]]; then
    echo "✅ $CURRENT_SHELL profile already exists: $PROFILE_FILE"
else
    touch "$PROFILE_FILE" && echo "✅ Created $CURRENT_SHELL profile: $PROFILE_FILE"
fi
```
**Expected:** One of these messages:
- `✅ zsh profile already exists: /Users/username/.zshrc` OR
- `✅ Created zsh profile: /Users/username/.zshrc` OR  
- `✅ bash profile already exists: /Users/username/.bashrc` OR
- `✅ Created bash profile: /Users/username/.bashrc`

### Step 3: Install VS Code

**Visit VS Code download page:**
- Go to: https://code.visualstudio.com/download
- Click "Download for macOS"
- Open the downloaded .pkg file
- Follow installation prompts

**Verify VS Code installation:**
```bash
code --version
```
**Expected:** Version number like `1.85.x`

### Step 4: Create Project Folder

**Check if Desktop exists:**
```bash
ls -la ~/Desktop
```
**Expected:** Shows Desktop folder contents OR "No such file or directory"

**Create project directory on Desktop:**
```bash
mkdir ~/Desktop/workshop_mcit_project
```
**Expected:** No output (command succeeds silently)

**Verify folder was created:**
```bash
ls -la ~/Desktop | grep workshop_mcit_project
```
**Expected:** Shows the directory with current timestamp:
```
drwxr-xr-x 2 username username 64 Dec 25 10:35 workshop_mcit_project
```

### Step 5: Navigate to Project Directory

**Change to project directory:**
```bash
cd ~/Desktop/workshop_mcit_project
```

**Verify current location:**
```bash
pwd
```
**Expected:** `/Users/[your-username]/Desktop/workshop_mcit_project`

### Step 6: Install Homebrew

**Check if Homebrew is already installed:**
```bash
brew --version
```
**Expected:** `Homebrew 4.x.x` OR "command not found"

**Install Homebrew if not found:**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
**Expected:** Installation text, password prompt, then "Installation successful!"
**Note:** This may take 5-10 minutes. Terminal may appear frozen - this is normal.

**Add Homebrew to PATH (Apple Silicon Macs only):**
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
```

```bash
eval "$(/opt/homebrew/bin/brew shellenv)"
```

**Verify Homebrew installation:**
```bash
brew --version
```
**Expected:** `Homebrew 4.x.x`

**Test Homebrew is working:**
```bash
brew doctor
```
**Expected:** "Your system is ready to brew." OR suggestions to fix issues

### Step 7: Install Git

**Check if Git is already installed:**
```bash
git --version
```
**Expected:** `git version 2.x.x` OR "command not found"

**Install Git if not found:**
```bash
brew install git
```
**Expected:** Installation messages OR "git is already installed and up-to-date"

**Verify Git installation:**
```bash
git --version
```
**Expected:** `git version 2.x.x`

**Configure Git (replace with your actual name and email):**
```bash
git config --global user.name "Your Name"
```
**Expected:** No output (success)

```bash
git config --global user.email "your.email@example.com"
```
**Expected:** No output (success)

**Verify Git configuration:**
```bash
git config --global --list
```
**Expected:** Shows your settings including:
```
user.name=Your Name
user.email=your.email@example.com
```

### Step 8: Clone Repository

**Clone the workshop repository:**
```bash
git clone https://github.com/justmake-it/workshop_mcit.git
```
**Expected:** `Cloning into 'workshop_mcit'...` followed by progress messages

### Step 9: Enter Project Folder

**Navigate into the cloned repository:**
```bash
cd workshop_mcit
```

**Verify you're in the right place:**
```bash
ls -la
```
**Expected:** List of files including `README.md`, `scripts/`, `credentials/`

**Check current location:**
```bash
pwd
```
**Expected:** Path ending with `/workshop_mcit`

### Step 10: Setup Workshop Credentials

**Get credentials file:**
1. **Visit the credentials URL**: <a href="https://www.dropbox.com/scl/fi/zhbcjoicdhmdtghmswvrk/credentials-gcp.json?rlkey=90vszrlfrgtqdm6b1gej4zhsh&st=ydpxgjuu&dl=0" target="_blank">https://www.dropbox.com/scl/fi/zhbcjoicdhmdtghmswvrk/credentials-gcp.json?rlkey=90vszrlfrgtqdm6b1gej4zhsh&st=ydpxgjuu&dl=0</a>
2. **Enter the password** provided during Workshop 1
3. **Copy the JSON content** from the downloaded file

**Create the credentials file:**
```bash
# Create/edit the credentials file (git-ignored)
nano credentials/credentials.json
```
**Instructions:** Paste the JSON content, then save (Ctrl+O, Enter, Ctrl+X)

**Verify credentials file:**
```bash
ls -la credentials/credentials.json
```
**Expected:** Shows file with content size (not 0 bytes)

### Step 11: Install Python

**Check if Python is already installed:**
```bash
python3 --version
```
**Expected:** `Python 3.x.x` OR "command not found"

**Install Python 3.11 if not found:**
```bash
brew install python@3.11
```
**Expected:** Installation messages ending with success OR "python@3.11 is already installed and up-to-date"
**Note:** May take 3-5 minutes. Terminal may appear frozen - this is normal.

**Verify Python installation:**
```bash
python3 --version
```
**Expected:** `Python 3.11.x`

**Check pip is working:**
```bash
pip3 --version
```
**Expected:** `pip x.x.x from /opt/homebrew/...` (shows pip is available)

### Step 12: Run Verification Script

**Run the verification script:**
```bash
python3 scripts/verify_setup.py
```
**Expected Output:**
```
🔧 MCIT AI Agents Workshop Setup Verification
=======================================================
🐍 Python Environment:
✅ Python 3.11.x
💻 System Tools:
✅ git: git version 2.x.x
❌ NVM not found (this is expected at this stage)
[More checks...]
```

### Step 13: Install NVM

**Check if NVM is already installed:**
```bash
nvm --version
```
**Expected:** `0.x.x` OR "command not found"

**Install NVM if not found:**
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.2/install.sh | bash
```
**Expected:** Installation messages ending with "=> nvm was installed successfully. To load it, open a new terminal..."
**Note:** May take 2-3 minutes

**Reload your shell profile:**
```bash
# Source the appropriate profile based on your shell
if [[ "$SHELL" == *"zsh"* ]]; then
    source ~/.zshrc && echo "✅ Reloaded zsh profile"
elif [[ "$SHELL" == *"bash"* ]]; then
    source ~/.bashrc && echo "✅ Reloaded bash profile"
else
    source ~/.profile && echo "✅ Reloaded profile"
fi
```

**Verify NVM installation:**
```bash
nvm --version
```
**Expected:** `0.40.2`

**Check if Node.js 20 is already installed:**
```bash
node --version
```
**Expected:** `v20.x.x` OR "command not found"

**Install Node.js 20 if not found:**
```bash
nvm install 20
```
**Expected:** `Downloading and installing node v20.x.x...` followed by success message
**Note:** May take several minutes. Terminal might appear to hang - this is normal.

**Set Node 20 as default:**
```bash
nvm alias default 20
```
**Expected:** `default -> 20 (-> v20.x.x)`

**Verify Node.js installation:**
```bash
node --version
```
**Expected:** `v20.x.x`

**Verify npm installation:**
```bash
npm --version
```
**Expected:** `10.x.x` (npm comes with Node.js)

### Step 14: Install Gemini CLI

**Check if Gemini CLI is already installed:**
```bash
gemini --version
```
**Expected:** Version number OR "command not found"

**Install Gemini CLI if not found:**
```bash
npm install -g @google/gemini-cli
```
**Expected:** Installation messages ending with success notification
**Note:** May take 2-3 minutes. Terminal might appear frozen - this is normal.

**Verify Gemini CLI installation:**
```bash
gemini --version
```
**Expected:** Version number like `1.x.x`

**Test Gemini CLI connection:**
```bash
gemini -p "Hello! Please respond with just 'Setup complete!'"
```
**Expected:** Response from Gemini AI saying "Setup complete!" or similar greeting
**Note:** This confirms both CLI installation and API connectivity

**Run final verification script:**
```bash
python3 scripts/verify_setup.py
```
**Expected:** All ✅ green checkmarks ending with:
```
🎉 All 7 checks passed! You're ready for the workshop.
🚀 Final test: Try running 'gemini chat "Hello!"' to confirm everything works.
```

---

## Windows Setup

### Step 1: Find and Open PowerShell

**Find PowerShell using Start Menu:**
1. Click the Windows Start button (⊞) in bottom-left corner
2. Type "PowerShell"
3. Click on "Windows PowerShell" when it appears
4. A blue window will open - this is your PowerShell

**Alternative method:**
1. Right-click the Windows Start button (⊞)
2. Select "Windows PowerShell" from the menu

**Verify PowerShell is open:**
You should see a blue window with text ending in `>` - this is your command prompt

**Check PowerShell version:**
```powershell
$PSVersionTable.PSVersion
```
**Expected:** PowerShell version information like:
```
Major  Minor  Build  Revision
-----  -----  -----  --------
5      1      19041  1320
```

**Check if PowerShell profile exists:**
```powershell
Test-Path -Path $PROFILE
```
**Expected:** `True` or `False`

**Create PowerShell profile if it doesn't exist:**
```powershell
if (!(Test-Path -Path $PROFILE)) { New-Item -ItemType File -Path $PROFILE -Force }
```

**Verify profile was created:**
```powershell
Test-Path -Path $PROFILE
```
**Expected:** `True`

### Step 2: Install VS Code

**Visit VS Code download page:**
- Go to: https://code.visualstudio.com/download
- Click "Download for Windows"
- Run the downloaded .exe file
- Follow installation prompts

**Verify VS Code installation:**
```powershell
code --version
```
**Expected:** Version number like `1.85.x`

### Step 3: Create Project Folder

**Check if Desktop exists:**
```powershell
Test-Path "$env:USERPROFILE\Desktop"
```
**Expected:** `True`

**Create project directory on Desktop:**
```powershell
New-Item -ItemType Directory -Path "$env:USERPROFILE\Desktop\workshop_mcit_project"
```
**Expected:** Directory creation confirmation showing path

**Verify folder was created:**
```powershell
Get-ChildItem "$env:USERPROFILE\Desktop" | Where-Object Name -eq "workshop_mcit_project"
```
**Expected:** Shows directory information with creation timestamp

### Step 4: Navigate to Project Directory

**Change to project directory:**
```powershell
Set-Location "$env:USERPROFILE\Desktop\workshop_mcit_project"
```

**Verify current location:**
```powershell
Get-Location
```
**Expected:** Path ending with `\Desktop\workshop_mcit_project`

### Step 5: Install Chocolatey

**Check if Chocolatey is already installed:**
```powershell
choco --version
```
**Expected:** `1.x.x` OR error about "choco" not being recognized

**Install Chocolatey if not found:**
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```
**Expected:** Installation messages ending with "Chocolatey (choco.exe) is now ready."
**Note:** May take 5-10 minutes. PowerShell may appear frozen - this is normal.

**Verify Chocolatey installation:**
```powershell
choco --version
```
**Expected:** `1.x.x` (version number confirming installation)

### Step 2: Install VS Code via Chocolatey

**Check if VS Code is already installed:**
```powershell
code --version
```
**Expected:** Version number like `1.85.x` OR error about "code" not being recognized

**Install VS Code via Chocolatey if not found:**
```powershell
choco install vscode -y
```
**Expected:** Installation messages ending with "vscode has been installed successfully"

**Verify VS Code installation:**
```powershell
code --version
```
**Expected:** Version number like `1.85.x`

### Step 3: Install Git via Chocolatey

**Check if Desktop exists:**
```powershell
Test-Path "$env:USERPROFILE\Desktop"
```
**Expected:** `True`

**Create project directory on Desktop:**
```powershell
New-Item -ItemType Directory -Path "$env:USERPROFILE\Desktop\workshop_mcit_project"
```
**Expected:** Directory creation confirmation showing path

**Verify folder was created:**
```powershell
Get-ChildItem "$env:USERPROFILE\Desktop" | Where-Object Name -eq "workshop_mcit_project"
```
**Expected:** Shows directory information with creation timestamp

### Step 4: Navigate to Project Directory

**Change to project directory:**
```powershell
Set-Location "$env:USERPROFILE\Desktop\workshop_mcit_project"
```

**Verify current location:**
```powershell
Get-Location
```
**Expected:** Path ending with `\Desktop\workshop_mcit_project`

### Step 5: Install Chocolatey

**Check if Chocolatey is already installed:**
```powershell
choco --version
```
**Expected:** `1.x.x` OR error about "choco" not being recognized

**Install Chocolatey if not found:**
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```
**Expected:** Installation messages ending with "Chocolatey (choco.exe) is now ready."
**Note:** May take 5-10 minutes. PowerShell may appear frozen - this is normal.

**Verify Chocolatey installation:**
```powershell
choco --version
```
**Expected:** `1.x.x` (version number confirming installation)

### Step 6: Install Git

**Check if Git is already installed:**
```powershell
git --version
```
**Expected:** `git version 2.x.x` OR error about "git" not being recognized

**Install Git if not found:**
```powershell
choco install git -y
```
**Expected:** Installation messages ending with "git has been installed successfully"

**Restart PowerShell to recognize Git:**
1. Close current PowerShell window
2. Open new PowerShell window (Start → type "PowerShell")
3. Navigate back to project directory:
```powershell
Set-Location "$env:USERPROFILE\Desktop\workshop_mcit_project"
```

**Verify Git installation:**
```powershell
git --version
```
**Expected:** `git version 2.x.x`

**Configure Git (replace with your actual name and email):**
```powershell
git config --global user.name "Your Name"
```
**Expected:** No output (success)

```powershell
git config --global user.email "your.email@example.com"
```
**Expected:** No output (success)

**Verify Git configuration:**
```powershell
git config --global --list
```
**Expected:** Shows your settings including:
```
user.name=Your Name
user.email=your.email@example.com
```

### Step 7: Clone Repository

**Clone the workshop repository:**
```powershell
git clone https://github.com/justmake-it/workshop_mcit.git
```
**Expected:** `Cloning into 'workshop_mcit'...` followed by progress

### Step 8: Enter Project Folder

**Navigate into the repository:**
```powershell
Set-Location workshop_mcit
```

**Verify location:**
```powershell
Get-ChildItem
```
**Expected:** List including `README.md`, `scripts\`, `credentials\`

### Step 9: Setup Workshop Credentials

**Get credentials file:**
1. **Visit the credentials URL**: <a href="https://www.dropbox.com/scl/fi/zhbcjoicdhmdtghmswvrk/credentials-gcp.json?rlkey=90vszrlfrgtqdm6b1gej4zhsh&st=ydpxgjuu&dl=0" target="_blank">https://www.dropbox.com/scl/fi/zhbcjoicdhmdtghmswvrk/credentials-gcp.json?rlkey=90vszrlfrgtqdm6b1gej4zhsh&st=ydpxgjuu&dl=0</a>
2. **Enter the password** provided during Workshop 1
3. **Copy the JSON content** from the downloaded file

**Create the credentials file:**
```powershell
# Create/edit the credentials file (git-ignored)
notepad credentials\credentials.json
```
**Instructions:** Paste the JSON content, then save (Ctrl+S) and close

**Verify credentials file:**
```powershell
Get-Item credentials\credentials.json
```
**Expected:** Shows file with content size (not 0 bytes)

### Step 10: Install Python

**Check if Python is already installed:**
```powershell
python --version
```
**Expected:** `Python 3.x.x` OR error about "python" not being recognized

**Install Python if not found:**
```powershell
choco install python -y
```
**Expected:** Installation messages ending with "python has been installed successfully"
**Note:** May take 5-7 minutes. PowerShell may appear frozen - this is normal.

**Restart PowerShell to recognize Python:**
1. Close current PowerShell window
2. Open new PowerShell window
3. Navigate back to workshop directory:
```powershell
Set-Location "$env:USERPROFILE\Desktop\workshop_mcit_project\workshop_mcit"
```

**Verify Python installation:**
```powershell
python --version
```
**Expected:** `Python 3.x.x`

**Check pip is working:**
```powershell
pip --version
```
**Expected:** `pip x.x.x from C:\...` (shows pip is available)

### Step 11: Run Verification Script

**Run verification:**
```powershell
python scripts\verify_setup.py
```
**Expected:** Verification results with some ✅ and some ❌ (missing items)

### Step 12: Install NVM for Windows

**Check if NVM is already installed:**
```powershell
nvm version
```
**Expected:** `1.x.x` OR error about "nvm" not being recognized

**Install NVM for Windows if not found:**
```powershell
choco install nvm -y
```
**Expected:** Installation messages ending with "nvm has been installed successfully"

**Restart PowerShell to recognize NVM:**
1. Close current PowerShell window
2. Open new PowerShell window
3. Navigate back to workshop directory:
```powershell
Set-Location "$env:USERPROFILE\Desktop\workshop_mcit_project\workshop_mcit"
```

**Verify NVM installation:**
```powershell
nvm version
```
**Expected:** `1.x.x`

**Check if Node.js 20 is already installed:**
```powershell
node --version
```
**Expected:** `v20.x.x` OR error about "node" not being recognized

**Install Node.js 20 if not found:**
```powershell
nvm install 20.0.0
```
**Expected:** `Downloading node v20.0.0...` followed by installation messages

**Use Node.js 20:**
```powershell
nvm use 20.0.0
```
**Expected:** `Now using node v20.0.0 (64-bit)`

**Verify Node installation:**
```powershell
node --version
```
**Expected:** `v20.0.0`

**Verify npm installation:**
```powershell
npm --version
```
**Expected:** `10.x.x` (npm comes with Node.js)

### Step 13: Install Gemini CLI

**Check if Gemini CLI is already installed:**
```powershell
gemini --version
```
**Expected:** Version number OR error about "gemini" not being recognized

**Install Gemini CLI if not found:**
```powershell
npm install -g @google/gemini-cli
```
**Expected:** Installation messages ending with success notification
**Note:** May take 2-3 minutes. PowerShell might appear frozen - this is normal.

**Verify Gemini CLI installation:**
```powershell
gemini --version
```
**Expected:** Version number like `1.x.x`

**Test Gemini CLI connection:**
```powershell
gemini -p "Hello! Please confirm you're working and ready for the workshop."
```
**Expected:** Response from Gemini AI confirming the connection works
**Note:** This confirms both CLI installation and API connectivity

**Final verification:**
```powershell
python scripts\verify_setup.py
```
**Expected:** All ✅ green checkmarks ending with:
```
🎉 All 7 checks passed! You're ready for the workshop.
```

---

## Linux Setup

### Step 1: Find and Open Terminal

**Find Terminal using keyboard shortcut:**
1. Press `Ctrl + Alt + T` simultaneously
2. A terminal window should open

**Alternative method:**
1. Click on Activities (top-left corner)
2. Type "Terminal"
3. Click on Terminal when it appears

**Verify Terminal is open:**
You should see a window with text ending in `$` - this is your command prompt

**Setup shell profile (smart detection):**
```bash
# Detect current shell and create appropriate profile
CURRENT_SHELL=$(basename "$SHELL")
if [[ "$CURRENT_SHELL" == "zsh" ]]; then
    PROFILE_FILE="$HOME/.zshrc"
elif [[ "$CURRENT_SHELL" == "bash" ]]; then
    PROFILE_FILE="$HOME/.bashrc"
else
    PROFILE_FILE="$HOME/.profile"
fi

if [[ -f "$PROFILE_FILE" ]]; then
    echo "✅ $CURRENT_SHELL profile already exists: $PROFILE_FILE"
else
    touch "$PROFILE_FILE" && echo "✅ Created $CURRENT_SHELL profile: $PROFILE_FILE"
fi
```
**Expected:** One of these messages:
- `✅ bash profile already exists: /home/username/.bashrc` OR
- `✅ Created bash profile: /home/username/.bashrc` OR  
- `✅ zsh profile already exists: /home/username/.zshrc` OR
- `✅ Created zsh profile: /home/username/.zshrc`

### Step 2: Install VS Code

**For Ubuntu/Debian - download .deb package:**
- Visit: https://code.visualstudio.com/download
- Download .deb for Linux
- Install with:

```bash
sudo dpkg -i ~/Downloads/code_*_amd64.deb
```

**Verify installation:**
```bash
code --version
```
**Expected:** Version number

### Step 3: Create Project Folder

**Check if Desktop exists:**
```bash
ls -la ~/Desktop
```
**Expected:** Shows Desktop folder contents OR "No such file or directory"

**Create Desktop if it doesn't exist:**
```bash
mkdir -p ~/Desktop
```

**Create project directory on Desktop:**
```bash
mkdir ~/Desktop/workshop_mcit_project
```
**Expected:** No output (command succeeds silently)

**Verify folder was created:**
```bash
ls -la ~/Desktop | grep workshop_mcit_project
```
**Expected:** Shows directory with timestamp

### Step 4: Navigate to Directory

**Change directory:**
```bash
cd ~/Desktop/workshop_mcit_project
```

**Verify location:**
```bash
pwd
```
**Expected:** Path ending with `/Desktop/workshop_mcit_project`

### Step 5: Update Package Manager

**Update package lists:**
```bash
sudo apt update
```
**Expected:** Package list update messages

### Step 6: Install Git

**Check if Git is already installed:**
```bash
git --version
```
**Expected:** `git version 2.x.x` OR "command not found"

**Install Git if not found:**
```bash
sudo apt install git -y
```
**Expected:** Installation messages ending with successful installation

**Verify Git installation:**
```bash
git --version
```
**Expected:** `git version 2.x.x`

**Configure Git (replace with your actual name and email):**
```bash
git config --global user.name "Your Name"
```
**Expected:** No output (success)

```bash
git config --global user.email "your.email@example.com"
```
**Expected:** No output (success)

**Verify Git configuration:**
```bash
git config --global --list
```
**Expected:** Shows your settings including:
```
user.name=Your Name
user.email=your.email@example.com
```

### Step 7: Clone Repository

**Clone repository:**
```bash
git clone https://github.com/justmake-it/workshop_mcit.git
```
**Expected:** Cloning progress messages

### Step 8: Enter Project Folder

**Navigate to repository:**
```bash
cd workshop_mcit
```

**Verify contents:**
```bash
ls -la
```
**Expected:** Repository files listed

### Step 9: Setup Workshop Credentials

**Get credentials file:**
1. **Visit the credentials URL**: <a href="https://www.dropbox.com/scl/fi/zhbcjoicdhmdtghmswvrk/credentials-gcp.json?rlkey=90vszrlfrgtqdm6b1gej4zhsh&st=ydpxgjuu&dl=0" target="_blank">https://www.dropbox.com/scl/fi/zhbcjoicdhmdtghmswvrk/credentials-gcp.json?rlkey=90vszrlfrgtqdm6b1gej4zhsh&st=ydpxgjuu&dl=0</a>
2. **Enter the password** provided during Workshop 1
3. **Copy the JSON content** from the downloaded file

**Create the credentials file:**
```bash
# Create/edit the credentials file (git-ignored)
nano credentials/credentials.json
```
**Instructions:** Paste the JSON content, then save (Ctrl+O, Enter, Ctrl+X)

**Verify credentials file:**
```bash
ls -la credentials/credentials.json
```
**Expected:** Shows file with content size (not 0 bytes)

### Step 10: Install Python

**Check if Python is already installed:**
```bash
python3 --version
```
**Expected:** `Python 3.x.x` OR "command not found"

**Install Python 3.11 if not found or old version:**
```bash
sudo apt install python3.11 python3.11-pip python3.11-venv -y
```
**Expected:** Installation messages ending with successful installation
**Note:** May take 3-5 minutes depending on your internet connection

**Verify Python installation:**
```bash
python3 --version
```
**Expected:** `Python 3.11.x`

**Check pip is working:**
```bash
pip3 --version
```
**Expected:** `pip x.x.x from /usr/lib/python3...` (shows pip is available)

### Step 11: Run Verification Script

**Run verification:**
```bash
python3 scripts/verify_setup.py
```
**Expected:** Partial verification results

### Step 12: Install NVM

**Check if NVM is already installed:**
```bash
nvm --version
```
**Expected:** `0.x.x` OR "command not found"

**Install NVM if not found:**
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.2/install.sh | bash
```
**Expected:** Installation messages ending with "=> nvm was installed successfully. To load it, restart your terminal..."
**Note:** May take 2-3 minutes

**Reload your shell profile:**
```bash
# Source the appropriate profile based on your shell
if [[ "$SHELL" == *"zsh"* ]]; then
    source ~/.zshrc && echo "✅ Reloaded zsh profile"
elif [[ "$SHELL" == *"bash"* ]]; then
    source ~/.bashrc && echo "✅ Reloaded bash profile"
else
    source ~/.profile && echo "✅ Reloaded profile"
fi
```

**Verify NVM installation:**
```bash
nvm --version
```
**Expected:** `0.40.2`

**Check if Node.js 20 is already installed:**
```bash
node --version
```
**Expected:** `v20.x.x` OR "command not found"

**Install Node.js 20 if not found:**
```bash
nvm install 20
```
**Expected:** `Downloading and installing node v20.x.x...` followed by success message
**Note:** May take several minutes. Terminal might appear to hang - this is normal.

**Set Node 20 as default:**
```bash
nvm alias default 20
```
**Expected:** `default -> 20 (-> v20.x.x)`

**Verify Node installation:**
```bash
node --version
```
**Expected:** `v20.x.x`

**Verify npm installation:**
```bash
npm --version
```
**Expected:** `10.x.x` (npm comes with Node.js)

### Step 13: Install Gemini CLI

**Check if Gemini CLI is already installed:**
```bash
gemini --version
```
**Expected:** Version number OR "command not found"

**Install Gemini CLI if not found:**
```bash
npm install -g @google/gemini-cli
```
**Expected:** Installation messages ending with success notification
**Note:** May take 2-3 minutes. Terminal might appear frozen - this is normal.

**Verify Gemini CLI installation:**
```bash
gemini --version
```
**Expected:** Version number like `1.x.x`

### Step 14: Test Gemini Connection

**Test Gemini CLI with credentials:**
```bash
gemini -p "Hello! Please confirm you're working and ready for the workshop."
```
**Expected:** Response from Gemini AI confirming the connection works

**Final verification:**
```bash
python3 scripts/verify_setup.py
```
**Expected:** All ✅ green checkmarks ending with:
```
🎉 All 7 checks passed! You're ready for the workshop.
```


---

## Success Criteria

After completing setup, you should be able to:

1. **Run Python code** with version 3.9 or higher
2. **Use Git** for version control 
3. **Access Gemini models** via the CLI
4. **Develop code** in VS Code

**Final Test:**
Your verification script should show:
```
🎉 All 7 checks passed! You're ready for the workshop.
```

If this command returns a response from Gemini, you're ready for the workshop! 🚀

---

Welcome to the MCIT AI Agents Workshop Series!