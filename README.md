# Your Naïve News Article Summarizer
### By: Bill Yin

## Introduction
When starting, please install all dependencies by running the following line in your project directory...
```
pip install -r requirements.txt
```

If this command does not work, please try running the following line in your project directory to install the packages one by one...
```
pip install openai pickle bs4 requests tqdm bert-extractive-summarizer tensorflow tensorflow_hub 
```

## Running the program
To run the program, please run the following line in your project directory...
```
python3 main.py
```

On startup, you will have 4 options:
1. Fetch articles from the web
2. Download articles from the web as txt files into the `articles` folder
3. Summarize articles from the `articles` folder
4. List out the article you currently have

Please ensure you have articles that you can summarize first by running the 4th command. If there are no articles present on the terminal, please fetch articles first before summarizing.

## Some notes
#### OpenAI Model Usage
In order to see data from the OpenAI model, you will need to have your own OpenAI API key. You can get one by signing up for the beta [here](https://platform.openai.com/overview). Then, store the key in an enviornment variable called `OPENAI_TOKEN`. You can do this by running the following line in your terminal...
```
export OPENAI_TOKEN=<your key here>
```


#### Quest details
- To activate the virtual environment, run ```conda activate bill_news```
- To deactivate the virtual environment, run ```conda deactivate```
- On Quest, computation is exponentially slower compared to my local machine. So for the summary to compute, you may have to wait a while, especially when using the bert-extractive-summarizer model