import requests

# Function to get a summary about a topic from the Wikipedia API
def tell_me_about(topic):
    try:
        # Access Wikipedia's summary for the topic
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
        response = requests.get(url)
        
        # Check for successful response
        if response.status_code == 200:
            data = response.json()
            summary = data.get("extract")
            
            # If a summary is returned, display it; otherwise, show a default message
            if summary:
                return summary[:500] + "..." if len(summary) > 500 else summary
            else:
                return f"Sorry, I couldn't find a summary for '{topic}' on Wikipedia."
        else:
            return f"Sorry, I couldn't retrieve information on '{topic}' due to an error."
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Sorry, I encountered an error while searching for information."
