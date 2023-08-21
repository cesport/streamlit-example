# Welcome to the draft for the ADL US T&T dashboard! ✈️

## Data processing
Because of the size of the data, it is not recommended to upload the complete BTS dataset on the virtual machine. Data processing is performed in a separate Python notebook. I personally used Google Colab to run it on the Cloud but you can use Jupyter or whatever you prefer. 💅

My data processing notebook is in this repo and it is named "TT.ipynb". All data needed for the dashboard is outputted in a TXT file named "sample.txt". This file can be overwritten when a new module or graph is added. 🚀

## Dashboard
Edit `/streamlit_app.py` to customize the dashboard app to your heart's desire. :heart:

## Deployment
The easiest way to deploy the dashboard on a public domain is to create an account on Streamlit and sync it with a GitHub account. Then, make sure to include the following files in your repo:
- `streamlit_app.py` for the dashboard code
- `requirements.txt` for all the packages required to run the python code on streamlit_app.py
- Other files that are read by your dashboard code

If you have any questions, checkout the [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io). Also feel free to contact me, Cesar Portocarrero, my email is cportoca@stanford.edu 
