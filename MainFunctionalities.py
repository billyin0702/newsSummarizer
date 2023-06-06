from datetime import datetime
from ArticleGet import ArticleGet
import spacy

class MainFunctionalities:
    
    def __init__(self):
        self.ag = ArticleGet()
        self.apiKey = "acc674d8efa142fa80bdc9cd72090a1e"
        # self.nlp = spacy.load('en_core_web_sm')
        
    def test(self):
        self.ag.test()
        
    # Function toget all the articles from the news website
    def get_articles_input(self):
        # Get all the neccesary parameters from the user, with sanity checks
        # Language
        is_lang_valid = False
        lang = ""
        
        while not is_lang_valid:
            print("Please enter the language you want to search for: (e.g. 'en'), default is english")
            lang = input("> ")
            
            # Check if input is empty
            if lang == "":
                break
            
            # Sanity check
            valid_langs = ["ar", "de", "en", "es", "fr", "he", "it", "nl", "no", "pt", "ru", "sv", "ud", "zh"]
            
            if lang not in valid_langs:
                print("Invalid language, please try again.")
                continue
            
            is_lang_valid = True
        
        
        # Keywords
        # Implement this using summarizer to see if you are able to extract keywords from a prompt
        
        either_keywords_or_query = False
        
        ### OLD ####
        print("\nPlease enter the keywords you want to search for: (e.g. 'tech, hospitality')")
        keywords = input("> ")
        
        if keywords != "":
            either_keywords_or_query = True
        
        # #### NEW ####
        # print("\nPlease enter a short query for the news you want to search for: (e.g. 'Apple's WWDC annoucement, and new computer')")
        # keywords_input = input("> ")
        
        # if keywords_input != "":

        #     doc = self.nlp(keywords_input)        

        #     either_keywords_or_query = True # note down that keywords has been entered

        #     candidate_pos = ['NOUN', 'PROPN', 'VERB']
        #     keywords = []

        #     for sent in doc.sents:
        #         selected_words = []
        #         for token in sent:
        #             if token.pos_ in candidate_pos and token.is_stop is False:
        #                 selected_words.append(token)
        #         keywords.append(selected_words)

        #     keywords = keywords[0]
        
        # else:
        #     keywords = []
        
        
        
        # News Domains
        print("\nPlease enter the news domains you would like to search (e.g. bbc.co.uk, techcrunch.com, cnn.com), none means all")
        domains = input("> ")
        
        if domains != "":
            either_keywords_or_query = True # note down that domains has been entered
            
        # Check if either keywords or query are enterd
        if not either_keywords_or_query:
            print("\n [E] ERROR: Please enter either keywords or a query, restarting...")
            return None
        
        

        # Date from
        is_date_valid = False
        date_from = ""
        
        while not is_date_valid:
            print("\nPlease enter the date from which you want to search for: (e.g. '2018-01-01'), empty means yesterday")
            date_from = input("> ")
            
            # Check if input is empty
            if date_from == "":
                break
            
            # Check if input can be converted to date
            if datetime.strptime(date_from, '%Y-%m-%d') == date_from:
                print("Invalid date format, please try again.")
                continue
            
            is_date_valid = True
            
        # Date to
        is_date_valid = False
        date_to = ""
        
        while not is_date_valid:
            print("\nPlease enter the date to which you want to search for: (e.g. '2018-01-01'), empty means today")
            date_to = input("> ")
            
            # Check if input is empty
            if date_to == "":
                break
            
            # Check if input can be converted to date
            if datetime.strptime(date_to, '%Y-%m-%d') == date_to:
                print("Invalid date format, please try again.")
                continue
            
            is_date_valid = True
                
        # Sort by
        is_sort_by_valid = False
        sort_by = ""
        
        while not is_sort_by_valid:
            print("\nPlease enter the sort by method you want to use: (relevancy, popularity, nearest), default relevancy")
            sort_by = input("> ")
            
            # Check if input is empty
            if sort_by == "":
                break
            
            # Sanity check
            if sort_by != "relevancy" and sort_by != "popularity" and sort_by != "nearest":
                print("Invalid sort by method, please try again.")
                continue
            
            is_sort_by_valid = True
            
        # Construct the params dictionary
        params = {
            'keywords': keywords,
            'domains': domains,
            'date_from': date_from,
            'date_to': date_to,
            'sort_by': sort_by,
            'lang': lang
        }
        
        return params

    # [0] Function for clearing all the articles from the search results
    def clearArticles(self):
        self.ag.clearArticles()

    # [1] Function for getting the articles from the news website
    def getArticles(self):
        
        params = self.get_articles_input() # Get the parameters from the user
        
        if params == None:
            print("Invalid parameters, exiting...")
            return
        
        # Now fetch the articles
        self.ag.fetchArticleAllContent(params['keywords'], params['domains'], params['date_from'], params['date_to'], params['sort_by'], params['lang'])
       
    # [2] Function for downloading the articles from the news website 
    def downloadArticles(self):
        self.ag.downloadArticles()
        
    # [3] Function for summarizing the articles from the news website
    def summarizeArticle(self):
        self.ag.summarizeArticle()  
        
    # [4] View all articles that have been searched
    def viewAllSearchedArticles(self):
        self.ag.viewAllSearchedArticles()