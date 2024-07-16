<a target="_blank" href="https://colab.research.google.com/github/osome-iu/IC2S2_OSoMe_tutorial_2024">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

# Exploring Emerging Social Media: Acquiring, Processing, and Visualizing Data with Python and OSoMe Web Tools

**Time:** Wed, July 17, 2024, 9:00 AM to 12:30 PM  
**Location:** Irvine: Amado Recital Hall (D), University of Pennsylvania, Philadelphia, PA

Stay ahead in the evolving field of social media research with our tutorial!

With new platforms like Bluesky and Mastodon emerging and established ones restricting data access, we will explore different innovative tools and techniques developed by the Observatory on Social Media (OSoMe) to facilitate the analysis and understanding of these platforms. 

## Tutorial Overview

### Part 1: Data Collection and Analysis with OSoMe
- **Tools:** Botometer-X, Coordiscope, TopFIBers, and more.
- **Simulation:** Generating simulated data using SimSoM.

### Part 2: Preprocessing and Analyzing Social Media Data
- **Languages/Tools:** Python and Jupyter notebooks.
- **Data Sources:** Datasets from Mastodon and Bluesky.
- **Techniques:** Building networks (co-reposts, co-hashtags, co-urls), centrality measures, community detection, and text embedding with sentenceBERT.

### Part 3: Visualization and Narrative Extraction
- **Tool:** Helios-Web for interactive visualization.
- **Techniques:** Natural language processing for narrative extraction.

This tutorial is suited for anyone with an interest in social media analysis, encompassing a wide range of disciplines and expertise. While prior knowledge of Python is desirable, the tutorial is designed to be inclusive and accessible to those with varying levels of technical proficiency. The tutorial will be conducted in Python and use Jupyter notebooks preloaded with datasets and scripts. The OSoMe tools and materials will be open-source, available via the observatory’s website or GitHub, providing participants with a toolkit to kickstart or advance their social media research endeavors.

You can find the tutorial materials and instructions on how to set up your environment on our GitHub page: [GitHub](https://github.com/osome-iu/IC2S2_OSoMe_tutorial_2024).

## Program

### Preparation Session (9:00 AM - 9:10 AM)
- Quick overview of the tutorial.
- Introduce the presenters.
- Demonstration on how to set up the environments and API keys.
- The organizers will help the attendees with the setup process. 

### Demonstration of the OSoMe Tools and Data Acquisition (9:10 AM - 10:00 AM)
- Utilizing OSoMe tools for analyzing and acquiring data, including Botometer-X, network tool, CoordiScope, Top FIBers, and OSoMe Mastodon Search.
- Data acquisition from an emerging platform using OSoMe infrastructure.
- Generate synthetic data from SimSoM, a minimal model that simulates information-sharing on a social media platform.

### Break and Setup (10:00 AM - 10:10 AM)

### Building Networks and Embeddings, Simple Analysis (10:10 AM - 11:00 AM)
- Preprocessing, filtering, cleaning.
- Constructing interaction networks (re-post, reply, mention).
- Building co-hash and co-post networks.
- Generating embeddings of posts using BERT.
- Employing similarity measures to find posts with similar content.
- Illustrating a classification task using embeddings.

### Break (11:00 AM - 11:10 AM)

### Visualization of Networks and LLM Integration to Explore Narratives (11:10 AM - 12:00 PM)
- Using Helios-web for visualizing user networks and post embeddings.
- Demonstrating the use of semantic axes to illustrate polarity.
- Extracting and analyzing communities.
- Identifying and discussing the narratives prevalent in each community, based on their content.

### Q&A and Discussion (12:00 PM - 12:30 PM)

## Organizers
- **Filipi N. Silva**, Research Scientist, Observatory on Social Media
- **Bao Tran Truong**, Ph.D. candidate in Informatics, Observatory on Social Media
- **Wanying Zhao**, Ph.D. candidate in Complex Networks and Systems, Indiana University
- **Kai-Cheng Yang**, Postdoctoral research associate at the Network Science Institute, Northeastern University

[OSoMe tutorial Page](https://osome.iu.edu/events/ic2s2-2024-workshop).

## Datasets
Data collected from Bluesky and Mastodon via streaming covering the period between 2024-06-25 and 2024-07-02. Entries contains any the of following terms: biden, trump, or debate.

Dataset is available on Zenodo:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.12748042.svg)](https://zenodo.org/records/12748042)


## Setting Up Your Environment Locally

We suggest using miniconda to install python packages and setup your environment. You can also use Anaconda, but it is a larger package and may take longer to install. Alternatively, you can also setup your own python environment using pip and virtualenv.

### Step 1: Download the Tutorial Materials
Download the tutorial materials from the github.
 - Click on the green "Code" button and download the zip file.
   - Unzip the file in a folder of your choice.

Alternatively you can clone the repository using git:
```bash
git clone https://github.com/osome-iu/IC2S2_OSoMe_tutorial_2024.git
```

### Step 2: Install Miniconda

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

### Step 3: Create a Conda Environment

Creating a separate environment for your projects is good practice:

1. **Create a New Environment for this course**:
    - Run the command: `conda env create -f environment.yml`. This will create a new environment called ic2s2tutorial with all the necessary packages installed.

2. **Activate the Environment**:
   - Run: `conda activate ic2s2tutorial`.

3. **Launch Jupyter Lab**:
   - Run: `jupyter lab`.
   - This will open Jupyter Lab in your default web browser.

### Step 4: Manually Install Essential Packages

The created environment already includes most of the packages we'll need, but if you need to install any additional packages, here's how:

1. **Installing packages using the requirements.txt **:
   - All the packages used in this tutorial can also be installed using the `requirements.txt` file.
   - Run: `pip install -r requirements.txt`.


2. **Manually Install Packages **:
   - In your activated environment, run: `conda install <name of the package>` to install the packages
   - For example, to install the `scikit-learn` package, run: `conda install scikit-learn`.
   - Alternatively, you can use `pip install <name of the package>` to install packages from PyPI.

### Step 5: Verify Installation

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


