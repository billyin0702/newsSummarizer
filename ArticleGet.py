# IMPORTS
import requests
import json
import os

from datetime import date
from datetime import timedelta
from bs4 import BeautifulSoup
from tqdm import tqdm

from summarizer import Summarizer


# This will be an exportable class that we can use for obtaining the articles from the news websites.
class ArticleGet:
    
    def __init__(self):
        
        print("[STARTING] Initializing Start Up Sequence....")
        
        self.articles = []
        self.api_key = "acc674d8efa142fa80bdc9cd72090a1e"
        self.summarize_model = Summarizer()
        self.summary_size = {"short": 3, "medium": 5, "long": 7}
        
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
    
    # FUNCTION 0: Clear all the articles from the search results
    def clearArticles(self):
        self.articles = []
                
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
                print("Error: Request was unsuccessful.")
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
            
            
            
    # FUNCTION 2: DOWNLOAD THE ARTICLES
    def downloadArticles(self):
        
        # Write each file to the articles folder
        for article in tqdm(self.articles, desc="Downloading articles"):
            self.writeToFile(article[3], article[1], article[0], article[2])
            
            
            
    # FUNCTION 3: SUMMARIZE THE SELECTED ARTICLE
    def summarizeArticle(self):
        
        # First, query the user to select an article
        print("\nPlease select an article to summarize:")
        
        for i, article in enumerate(self.articles):
            print(f"{i+1} - [{article[2]}]: {article[0]}]")
            
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
        
            print("\nPlease select the size of the summary: (short, medium, long)")
            user_input = input("> ")
            
            # Check if the input is valid
            if user_input not in self.summary_size:
                print("Invalid input (input not in the selection), please reselect")
                return
            
            user_input_valid = True
        
        # Now summarize the article
        body = article[3]
        body_summary = self.summarize_model(body, num_sentences=self.summary_size[user_input])
        
        # Print out the summary
        print(f"\nSummary for '{article[0]}':")
        print("-------------------------------------------------------------------")
        print(body_summary)
        
        # Wait for user input to continue
        input("\nPress enter to continue...")
        
            
                