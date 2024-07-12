# Introduction
<a target="_blank" href="https://colab.research.google.com/github/osome-iu/IC2S2_OSoMe_tutorial_2024">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

[OSoMe tutorial at IC2S2 2024](https://osome.iu.edu/events/ic2s2-2024-workshop).

# Datasets

## Setting Up Your Environment using Google Colab

## Setting Up Your Environment Locally

We suggest using miniconda to install python packages and setup your environment. You can also use Anaconda, but it is a larger package and may take longer to install. Alternatively, you can also setup your own python environment using pip and virtualenv.

### Step 1: Install Miniconda

Miniconda is a minimal installer for Conda, a package manager and an environment manager. Here’s how to install it:

1. **Download Miniconda**:
   - Visit the [Miniconda download page](https://docs.conda.io/en/latest/miniconda.html).
   - Choose the version suitable for your operating system (Windows, macOS, or Linux).
   - Download the appropriate installer (Python 3.x is recommended).

2. **Install Miniconda**:
   - **Windows**: Run the downloaded `.exe` file and follow the on-screen instructions.
   - **macOS/Linux**: Open a terminal, navigate to the folder containing the downloaded file, and run `bash Miniconda3-latest-MacOSX-x86_64.sh` (adjust the filename as needed).

3. **Verify the Installation**:
   - Open a new terminal window.
   - Type `conda list`. If Miniconda is installed correctly, you'll see a list of installed packages.

### Step 2: Create a Conda Environment

Creating a separate environment for your projects is good practice:

1. **Create a New Environment for this course**:
    - Run the command: `conda env create -f environment.yml`. This will create a new environment called networktutorial with all the necessary packages installed.

2. **Activate the Environment**:
   - Run: `conda activate networktutorial`.

3. **Launch Jupyter Lab**:
   - Run: `jupyter lab`.
   - This will open Jupyter Lab in your default web browser.

### Step 3: Manually Install Essential Packages

The created environment already includes most of the packages we'll need, but if you need to install any additional packages, here's how:

1. **Manually Install Packages **:
   - In your activated environment, run: `conda install <name of the package>` to install the packages
   - For example, to install the `scikit-learn` package, run: `conda install scikit-learn`.
   - Alternatively, you can use `pip install <name of the package>` to install packages from PyPI.

### Step 4: Verify Installation

Make sure everything is installed correctly:

1. **Open a New Notebook in Jupyter Lab**:
   - In Jupyter Lab, create a new notebook.

2. **Test the Packages**:
   - Try importing the packages: `import numpy as np`, `import pandas as pd`, `import matplotlib.pyplot as plt`.
   - If there are no errors, the packages are installed correctly.

### Additional Tips

- **Updating Conda**: Keep Conda and your packages updated with `conda update conda` and `conda update --all`.
- **Managing Environments**: View your environments with `conda env list` and switch between them using `conda activate <env_name>`.
- **Finding Packages**: To find available packages, use `conda search <package_name>`.
- **Conda Cheat Sheet**: For more commands, see the [Conda Cheat Sheet](https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html).


