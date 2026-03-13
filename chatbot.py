import requests

def flower_chatbot(user_input):
    # URL of the n8n webhook
    webhook_url = "https://krithi2509.app.n8n.cloud/webhook/3ee79fd6-553f-4c04-9417-78ff604a4125/chat"

    try:
        # Send POST request to n8n webhook
        response = requests.post(webhook_url, json={"message": user_input}, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes

        # Assuming the webhook returns JSON with a "response" key
        data = response.json()
        return data.get("response", "Sorry, I couldn't get a response from the chatbot.")

    except requests.exceptions.RequestException as e:
        return f"Sorry, there was an error connecting to the chatbot: {str(e)}"