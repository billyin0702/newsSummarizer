from MainFunctionalities import MainFunctionalities
from datetime import datetime


# *********************** SET UP ***********************
# User input that will dictate the flow of the script.
global_input = ""

main_func = MainFunctionalities()

# *********************** SET UP END ***********************





# *********************** HELPER FUNCTIONS ***********************
def command_prompt():
    print("Please select one of the following commands:")
    print("exit - Exit the program.")
    print("0 - Clear all searched articles")
    print("1 - Get articles from a news website [add to existing articles]")
    print("2 - Download articles searched into the 'articles' folder")
    print("3 - Summarize a selected article searched")
    print("4 - View all articles that have been searched")
    print("")
    
    user_input = input("> ")
    
    return user_input

# ********************** HELPER FUNCTIONS END ***********************



# ********************** Main Function: Run the script from here ###############

while (global_input != "exit"):
    
    global_input = command_prompt()
    
    if global_input == "exit":
        print("Exiting the program...")
        break
    elif global_input == "0":
        main_func.clearArticles()
    elif global_input == "1":
        main_func.getArticles()
    elif global_input == "2":
        main_func.downloadArticles()
    elif global_input == "3":
        main_func.summarizeArticle()
    elif global_input == "4":
        main_func.viewAllSearchedArticles()
    else:
        print("Invalid command, please try again.")
        continue
        
        
        
        
    # End of cycle spacing
    print("\n\n")