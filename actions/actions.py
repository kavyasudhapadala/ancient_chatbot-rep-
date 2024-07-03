# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"



# actions.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import http.client
import json

class ActionGetAiStory(Action):

    def name(self) -> Text:
        return "action_get_ai_response"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the user's name, friends' names, and scenario from slots
        user_name = tracker.get_slot('name')
       
        event = tracker.get_slot('event')

        # Create the prompt for the AI API
        prompt = f"Hello{user_name}, here your information {event} "

        # Set up the connection and headers for the API call
        conn = http.client.HTTPSConnection("chatgpt-42.p.rapidapi.com")
        payload = json.dumps({
            "messages": [{"role": "user", "content": prompt}],
            "system_prompt": "",
            "temperature": 0.9,
            "top_k": 5,
            "top_p": 0.9,
            "image": "",
            "max_tokens": 256
        })
        headers = {
            'x-rapidapi-key':   "20af294f58mshc78be4a439c9fd9p1a73a5jsn3cc0faf18b8c",
            'x-rapidapi-host': "chatgpt-42.p.rapidapi.com",
            'Content-Type': "application/json"
        }

        # Make the API request
        conn.request("POST", "/matag2", payload, headers)
        res = conn.getresponse()
        data = res.read()

        # Print the raw response for debugging
        print("Raw API response:", data.decode("utf-8"))

        # Parse the JSON response
        response_data = json.loads(data.decode("utf-8"))

        # Print the parsed response for debugging
        print("Parsed API response:", response_data)
                # Extract the AI response
        ai_response = response_data.get("result", "I'm sorry, I couldn't find an answer to your question.")

        # Send the AI response back to the user
        dispatcher.utter_message(text=ai_response)

        return []

