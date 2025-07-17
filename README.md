# OCR Terminal Utility

A simple Python utility to perform Optical Character Recognition (OCR) on a screen capture directly from your terminal. It uses the Windows Snipping Tool, detects the new screenshot, sends it to the Nanonets API for text extraction, and copies the result to your clipboard.


## Prerequisites

  * Python 3.12+
  * A [Nanonets OCR API Key](https://www.google.com/search?q=https://app.nanonets.com/%23/keys)
  * (Optional) [uv](https://github.com/astral-sh/uv) - An extremely fast Python package installer and resolver.


## Installation and Setup

Follow these steps to get the utility up and running.

### 1\. Clone the Repository

First, clone this repository to your local machine.

```bash
git clone <your-repository-url>
cd <repository-directory>
```


### 3\. Install Dependencies

You can use either `uv` (recommended) or `pip` to install the required packages.

#### Option A: Using `uv` (Recommended)

`uv` will create a virtual environment and install dependencies from `requirements.txt` in a single, fast step.

```bash
uv pip sync
```

#### Option B: Using `pip`

If you don't have `uv`, you can use `pip` and `venv` to set up your environment.

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 4\. Configure API Key

Create a file named `.env` in the root of the project directory and add your Nanonets API key to it.

```
API_KEY="YOUR_NANONETS_API_KEY_HERE"
```

-----

## Usage

To make the script easily accessible from anywhere in your terminal, you can add a custom function to your PowerShell `$PROFILE`.

### 1\. Edit Your PowerShell Profile

Open your PowerShell profile file for editing. If you're not sure where it is, run `echo $PROFILE` in PowerShell to find the path.

```powershell
code $PROFILE
```

### 2\. Add the `ocr` Function

Copy the function that matches your installation method (`uv` or `pip`) into your profile file and **update the `$projectPath` variable** to point to the cloned repository's directory.

#### For `uv` Users

```powershell
function ocr() {
    Push-Location "C:\path\to\your\cloned_repository"
    uv run main.py
    Pop-Location
}
```

#### For `pip` Users

This function directly calls the Python executable inside your project's virtual environment.

```powershell
function ocr() {
    $projectPath = "C:\path\to\your\cloned_repository"
    $pythonExe = Join-Path $projectPath ".venv\Scripts\python.exe"
    $scriptPath = Join-Path $projectPath "main.py"
    & $pythonExe $scriptPath
}
```

### 3\. Launch the Utility

Save your profile file and restart your terminal. You can now run the utility from any directory.

```powershell
ocr
```

The script will launch the Windows Snipping Tool. After you take a snip, it will perform OCR and copy the extracted text to your clipboard.