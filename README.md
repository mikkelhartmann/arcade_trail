# Arcade Trail
This project uses data from the crowdsourced game discovery and curation platform [Arcade Trail](https://arcadetrail.com/about) to make personalized game reccomendations and classify game genres based on short game descriptions.

## Installing requirements and running the jupyter notebook
The program is written in python 3. I suggest you run this in a virtual python enviromnent.

### Setting up the virtual environment
To create the virtual environment do:

`virtualenv --no-site-packages -p <path/to/python3> env/`

Start the virtual environment:

`source env/bin/activate`

Install the requirements:

`pip3 install -r requirements.txt`

When you are done working, remember to deactivate the virutal environment:

`deactivate`

### Installing NLTK data
For the language analysis we need the data from NLTK. To download the data run:

`python -m nltk.downloader all`

### Running the Jupyter Notebook locally
Once the virtual environment in set up, the Jupyter notebook can be run by doing:

`jupyter notebook classifying_genres_from_description.ipynb`

### How to try out the product
Run try out the classification algorithm on your own game descriptions run the following command in the terminal:

`Make web`

## Example of output code
