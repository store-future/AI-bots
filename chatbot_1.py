'''
Functionality: This code implements a simple chatbot interface that interacts with a local API endpoint to generate responses based on user input. The chatbot maintains the conversation history using the response ID from the API, allowing for a more coherent conversation flow.
trained = NO (answer based upon pre trained llm model)
Commented Code : used to make manual history management currently using default response id to maintain the history .
'''

import requests

url = "http://localhost:1234/api/v1/chat"
model = "google/gemma-3-4b"
# history = "" # you can implement logic to maintain the conversation history if needed
previous_response_id = None

try :     
    while True:
        user_input = input("USER INPUT: ")

        if user_input.lower() in  ["exit","exit()", "quit", "bye"]:
            break

        # history += user_input + "\n" # you can implement logic to append the user input to history if needed
                
        payload = {
            "model" : model,
            # "input" : history, # you can implement logic to send the conversation history as input if needed
            "input" : user_input,
            "previous_response_id" : previous_response_id 
        }

        response = requests.post(url, json=payload)

        if response.status_code == 200:
            data = response.json()  # parse json response data
            reply = data["output"][0]["content"]
            print(F"Assistance : {reply}\n")

            previous_response_id = data["response_id"]  
            # history += reply + "\n"  # you can implement logic to append the reply to history if needed
        else:
            print(F"ERROR :{response.text}")
except KeyboardInterrupt :
    print(F"user manually shutdown loop..")    

# print(history)
