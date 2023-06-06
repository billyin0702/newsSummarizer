# IMPORTS
print("[IMPORT] Importing necessary libraries...")

import requests
import json
import os
import openai
import pickle

from datetime import date
from datetime import timedelta
from bs4 import BeautifulSoup
from tqdm import tqdm
from summarizer import Summarizer

import tensorflow as tf
import tensorflow_hub as hub


print("[IMPORT] Imported necessary libraries.")


# This will be an exportable class that we can use for obtaining the articles from the news websites.
class ArticleGet:
    
    def __init__(self):
        
        print("[STARTING] Initializing Start Up Sequence....")
        
        # First, see if pickle file exists with the articles list, if it does, load it
        self.articles = []
        
        if os.path.exists("articles.pickle"):
            print("Loading articles from pickle file...")
            with open("articles.pickle", "rb") as file:
                self.articles = pickle.load(file)
        
        self.api_key = "acc674d8efa142fa80bdc9cd72090a1e"
        self.summarize_model = Summarizer()
        self.summary_size = {"short": 3, "medium": 5, "long": 7}
        
        self.openai_max_tokens = {"short": 100, "medium": 200, "long": 300}
        self.openai_temperature_user = 0.3 
        self.openai_key = os.getenv("OPENAI_TOKEN")
        self.openai_model_name = 'text-davinci-003'
        self.openai_presence_penalty = 0.5
        
        self.use_module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
        self.use_model = hub.load(self.use_module_url)        
        
        print("[STARTING] Start Up Sequence Complete.")
    
    # [HELPER] Parse the keywords, they will be passed in as a dictionary denoting each's importance
    # 0: Not important
    # 1: Important
    def formatKeywords(self, keywords):
        
        ret = ""
        
        if "," not in keywords:
            ret = keywords
            return ret
        
        # split the words by comma if there is more than one term
        keywords = keywords.split(",")

        # Now parse keywords array into a string
        for word in keywords:
            ret += word + ","
        
        ret = ret[:-1] # Remove the last comma
                
        return ret
    
    
    # [HELPER] Prepare the articles folder for writing
    def prepForWrite(self):
        # Now write each article into a file in a folder called "articles"
        # Make sure to create the folder first if it does not exist
        if os.path.isdir("articles") == False or os.path.exists("articles") == False:
            print("Creating articles folder...")
            os.mkdir("articles")
        else:
            # Check to see there are no files in the folder
            if len(os.listdir("articles")) != 0:
                
                print("Directories is not empty, deleting all files in the articles folder...")
                
                # Delete all the files in the folder
                for file in os.listdir("articles"):
                    os.remove(f"articles/{file}")
                
                print("Deleted all files in the articles folder.")
        
    
    # [HELPER] Write the content to article files
    def writeToFile(self, content, author, title, source):
        
        # Edit the title to exclude "/", and replace with "-"
        title = title.replace("/", "-")
        
        # Now write the content to a file in the folder "articles"
        with open(f"articles/{title}.txt", "w") as file:
            file.write(f"Title: {title}\n")
            file.write(f"Author: {author}\n")
            file.write(f"Source: {source}\n\n")
            file.write("Content:\n")
            file.write(content)
    
    
    # [HELPER] Format the parameters for the HTTP request
    def formatParams(self, keywords, domains, date_from, date_to, sortBy, lang):
        

        # Create the params dictionary
        params = {
            'apiKey': self.api_key
        }
        
        # Now insert the parameters into the params dictionary if they are not empty
        if len(keywords) != 0:
            params['q'] = self.formatKeywords(keywords)
        else:
            params['q'] = ""
            
        if lang != "":
            params['language'] = lang
        else:
            params['language'] = "en"
        
        if sortBy != "":
            params['sortBy'] = sortBy
        else:
            params['sortBy'] = "relevancy"
            
        if domains != "":
            params['domains'] = domains.replace(" ", "")
        
        if date_from != "":
            params['from'] = date_from
        else:
            temp = date.today() - timedelta(days=1)
            params['from'] = temp.strftime('%Y-%m-%d')
            
        if date_to != "":
            params['to'] = date_to
        else:
            temp = date.today()
            params['to'] = temp .strftime('%Y-%m-%d')
            
        # Manual setting for searching scope
        params['searchIn'] = "title"
            
        return params
        
    
    # [HELPER] Fetch the articles' URL from the new website using HTTP requests using the NewsAPI
    def fetchArticleAllUrl(self, keywords, domains, date_from, date_to, sortBy, lang):
        
        # Construct the URL and params for the HTTP request
        url = "https://newsapi.org/v2/everything"
        params = self.formatParams(keywords, domains, date_from, date_to, sortBy, lang)
        
        print("Request Parameters:")
        print(params)
        
        # Make the HTTP request
        response = requests.get(url, params=params)
        
        # Check if the request was successful
        if response.status_code != 200:
            print("ERROR: Request was unsuccessful.")
            print("ERROR: " + response.json()['message'])
            return [], [], [], []

        # Parse the response into a JSON object
        response = response.json()
        content = response['articles']
        
        # Now get all the urls from the content
        urls = []
        authors = []
        titles = []
        sources = []
        
        
        for article in content:
            urls.append(article['url'])
            authors.append(article['author'])
            titles.append(article['title'])
            sources.append(article['source']['name'])

        return urls, authors, titles, sources
    
    # [HELPER] Naive summarizer using sentence similarity analysi from USE
    def naiveSummarizer(self, title, content, n):
        
        # First split content by sentences
        sentences = content.split(".")
        sentences_with_scores = []
        ret = ""
        
        # Now, analyze the similarity between the title and each sentence
        for sentence in sentences:
            
            # Get the similarity score
            embeddings = self.use_model([sentence, title])
            similarity = tf.keras.losses.cosine_similarity(embeddings[0], embeddings[1]).numpy() * -1
            
            # Add the sentence and score to the list
            sentence = sentence.strip()
            sentences_with_scores.append((sentence, similarity))
            
        # Now sort the sentences by their similarity score
        sentences_with_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Now get the top sentences
        for item in sentences_with_scores[:n]:
            ret += item[0] + ". "
            
        # Remove the white space
        ret = ret.lstrip(" ")
            
        return ret
    
    
    # FUNCTION 0: Clear all the articles from the search results
    def clearArticles(self):
        self.articles = []
        
        # remove the pickle file on clear if it exists
        if os.path.exists("articles.pickle"):
            print("Removing articles.pickle file...")
            os.remove("articles.pickle")
        
                
    # FUNCTION 1: Fetch the articles content from the new website using HTTP requests by scrapping the URL
    def fetchArticleAllContent(self, keywords, domains, date_from, date_to, sortBy="relevancy", lang="en"):
        
        urls, authors, titles, sources = self.fetchArticleAllUrl(keywords, domains, date_from, date_to, sortBy, lang)
        
        if len(urls) == 0 and len(authors) == 0 and len(titles) == 0 and len(sources) == 0:
            print("No articles found...")
            return
        
        # Create folder or delete all files in the folder depending on the situation   
        self.prepForWrite()
        
        # Now, for each url, make a HTTP request and get the content, and scrape it
        for i in tqdm(range(len(urls)), desc="Searching for articles"):
            
            # Get the url, author, title, and source
            url = urls[i]
            author = authors[i]
            title = titles[i]
            source = sources[i]
            
            # Make the HTTP request
            resposne = requests.get(url)
            
            # Check if the request was successful
            if resposne.status_code != 200:
                print(f"Error: Request was unsuccessful to {url}")
                continue
            
            # Now parse the response into a BeautifulSoup object
            soup = BeautifulSoup(resposne.content, 'html.parser')
            
            # Now get the content of the article
            content_elements = soup.find_all('p')
            
            # Now get the content from the elements
            content = ""
            
            for element in content_elements:
                content += element.text + " "
                
            # Now write each article into a file in a folder called "articles"
            self.articles.append([title, author, source, content])
            
        # Lastly, add the data to pickle file
        with open("articles.pickle", "wb") as file:
            pickle.dump(self.articles, file)
            
            
            
    # FUNCTION 2: DOWNLOAD THE ARTICLES
    def downloadArticles(self):
        
        # Write each file to the articles folder
        for article in tqdm(self.articles, desc="Downloading articles"):
            self.writeToFile(article[3], article[1], article[0], article[2])
            
            
            
    # FUNCTION 3: SUMMARIZE THE SELECTED ARTICLE
    def summarizeArticle(self):
        
        # First, query the user to select an article
        print("\nPlease select an article to summarize by entering its number:")
        
        for i, article in enumerate(self.articles):
            print(f"{i+1} - [{article[2]}]: {article[0]}")
            
        # Now get the user input
        user_input = input("> ")
        
        # Check if the input is valid
        if user_input.isdigit() == False:
            print("Invalid input (is not a digit), exiting...")
            return
        
        # Check if the input is within range
        if int(user_input) < 1 or int(user_input) > len(self.articles):
            print("Invalid input (input out of range), exiting...")
            return
        
        # Now get the article
        article = self.articles[int(user_input) - 1]
        
        # User input for number of sentences they would like the summary to be
        user_input_valid = False
        user_input = ""
        
        while not user_input_valid:
        
            print("\n\nPlease select the size of the summary: (short, medium, long)")
            user_input = input("> ")
            
            # Check if the input is valid
            if user_input not in self.summary_size:
                print("Invalid input (input not in the selection), please reselect")
                return
            
            user_input_valid = True
            
        body = article[3] # Get the body of the article
            
        # Now summarize the article using the naive summarizer
        body_summary = self.naiveSummarizer(article[0], body, n=self.summary_size[user_input])
        
        # Print out the summary [naive]
        print(f"\nSummary for '{article[0]}' using naive summarizer:")
        print("---------------------------------------------------------------------------------")
        print(body_summary)
        
        # Now summarize the article using BERT
        body_summary = self.summarize_model(body, num_sentences=self.summary_size[user_input])
        body_summary = "".join(body_summary)
        
        # Print out the summary [BERT]
        print(f"\n\nSummary for '{article[0]}' using BERT:")
        print("---------------------------------------------------------------------------------")
        print(body_summary)
        
        # Now summarize the article using OpenAI
        if self.openai_key != None:
            
            # modify body for OPENAI summarizer
            body += "\nTl:dr"
            
            openai.api_key = self.openai_key # Set the API key
            output = openai.Completion.create(
                        engine=self.openai_model_name,
                        prompt=body,
                        max_tokens=self.openai_max_tokens[user_input],
                        temperature=self.openai_temperature_user,
                        n=1,
                        stop=None,
                        presence_penalty=self.openai_presence_penalty,
                    )
            
                    # Print out the summary
            print(f"\n\nSummary for '{article[0]}' using OPENAI's {self.openai_model_name}:")
            print("---------------------------------------------------------------------------------")
            print(output.choices[0].text.strip())
            
        else:
            print("\n\nOpenAI API key is not set, skipping OpenAI summary... (please use your own API key)")
            
        # Wait for user input to continue
        input("\nPress enter to continue...")
        
        
    # FUNCTION 4: VIEW ALL SEARCHED ARTICLES
    def viewAllSearchedArticles(self):
        
        if len(self.articles) == 0:
            print("No articles have been searched yet...")
            return
        
        for i, article in enumerate(self.articles):
            print(f"{i+1} - [{article[2]}]: {article[0]}")
        
            
                