'''
Functionality: This chatbot is trained on a custom dataset no vector database or embeddings is being used.Instead of that it is a keyword-matching retrieval + LLM response system. which gives the response based on the keyword matching from the custom dataset.
trained = YES (trained based on custom given dataset)
chatbot level - keyboard matching chatbot
what you will learn -Retrieval-Augmented Prompting system without embedding and without vector database
steps = Load Database > User → keyword match → context → send to model → response

working:
✔ Load dataset as sentences
✔ Split user input into words
✔ Match keywords
✔ Join matched lines as context
✔ Send context + question to model


'''

import requests

# ------------ LOAD CUSTOM DATA ------------------
with open("custom_Dataset.txt", "r", encoding="utf-8") as f:
    custom_data_line = f.readlines()   # keep sentences full line not word level chunking
    # print(custom_data_line)

# ------------ SEARCH FUNCTIONALITY ------------------
def retrieve_context(question, custom_dataset):
    question_chunk = question.split()  # making chunk list for each word in the user input
    # print(f"DEBUG : question chunked into words: {question_chunk}")

    result = set()
    for line in custom_dataset:
        for word in question_chunk:
            print(f"DEBUG : checking if '{word}' is in line '{line.strip()}'")
            if word.lower() in line.lower().split():  # check for whole word match
                result.add(line)
    
    context = '\n'.join(result)  # join the matched lines to form the context as string
    return context if context else "No relevant information found in the dataset."

# ------------ ChatBot Function (chat loop) ------------------
def chatbot(model,url):
    try :
        while True:
            user_input = input("ASK IT : " )

            if user_input.strip().lower() in ["exit", "quit"] :
                print("\n\t *** USer exit form chat ***")
                break

            # using the search function to retrieve the context based on user input and custom dataset
            context = retrieve_context(user_input, custom_data_line)
            print(f"-----\nContext retrieved: {context}\n----")

            payload = {
                "model" : model,
                "input" : f"Context: {context}\nQuestion: {user_input}",  # you can format the input as needed for your model
            }

            # making api request with context and question to the model
            try : 
                response = requests.post(url, json = payload)
      
                if response.status_code == 200:
                    data = response.json()
                    reply = data['output'][0]['content']
                    print(F"Assistance : {reply}\n")
                else : 
                    print(f"Error: Received status code {response.status_code} from the API")

            except requests.RequestException as e:
                print(f"Error making API request: {e}")

            
    except KeyboardInterrupt :
        print("\n\t *** user close chat manually***")


model = "google/gemma-3-4b"
url = "http://localhost:1234/api/v1/chat"


if __name__ == "__main__":
    chatbot(model,url)












