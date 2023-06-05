# ############### HOW TO SUMMARIZE A GIVEN ARTICLE ###############
# from summarizer import Summarizer

# body = "Apple's WWDC annoucement related to the new Macbook Pro and the new Macbook Air."
# model = Summarizer()
# output = model(body)

# print("Finished")
# print(output)




# ############## SEMANTIC SEARTCHING ##############
# from sentence_transformers import SentenceTransformer, util
# model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

# query_embedding = model.encode('How big is London')
# passage_embedding = model.encode(['London has 9,787,426 inhabitants at the 2011 census',
#                                   'London is known for its finacial district'])

# print("Similarity:", util.dot_score(query_embedding, passage_embedding))





# # ############## KEYWORDS EXTRACTION ##############
# import spacy
# nlp = spacy.load('en_core_web_sm')

# content = "wwdc"

# doc = nlp(content)

# candidate_pos = ['NOUN', 'PROPN', 'VERB']
# sentences = []

# for sent in doc.sents:
#     selected_words = []
#     for token in sent:
#         if token.pos_ in candidate_pos and token.is_stop is False:
#             selected_words.append(token)
#     sentences.append(selected_words)

# print(sentences[0])
# print(type(sentences[0][0]))
# print(str(sentences[0][0]))
# print(type(str(sentences[0][0])))
# print(sentences[0][0].lemma_)
# print(type(sentences[0][0].lemma_))




# ############## REQUEST TESTING ##############
# import requests

# params = {'apiKey': 'acc674d8efa142fa80bdc9cd72090a1e', 'q': 'sony', 'language': 'en', 'sortBy': 'relevancy', 'domains': 'cnet.com', 'from': '2023-06-03', 'to': '2023-06-04'}

# response = requests.get("https://newsapi.org/v2/everything", params=params)

# print(response.json())


# ############## OPENAI TESTING ##############

# import openai
# import os

# prompt = "The sun was setting, casting a warm golden glow across the horizon. The waves gently lapped against the sandy shore. Seagulls soared overhead, their cries echoing in the salty air."

# max_tokens = 100
# temperature_user = 0.7

# print(os.getenv("OPENAI_TOKEN"))

# openai.api_key = os.getenv("OPENAI_TOKEN")
# model_name = 'text-davinci-003'

# output = openai.Completion.create(
#   engine=model_name,
#   prompt=prompt,
#   max_tokens=max_tokens,
#   temperature=temperature_user,
#   n=1,
#   stop=None
# )

# paragraph = output.choices[0].text.strip()

# print(paragraph)

# ############## NAIVE SIMILARITY TESTING ##############

# import tensorflow as tf
# import tensorflow_hub as hub

# # Load the Universal Sentence Encoder
# module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
# model = hub.load(module_url)

# # Define two example sentences
# sentence1 = "This is the first sentence."
# sentence2 = "This is the second sentence."

# # Encode the sentences
# embeddings = model([sentence1, sentence2])
# similarity = tf.keras.losses.cosine_similarity(embeddings[0], embeddings[1]).numpy() * -1

# print("Similarity:", similarity)
