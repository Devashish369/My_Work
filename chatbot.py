import nltk
from nltk.chat.util import Chat, reflections

# Define patterns and responses
patterns = [
    (r'hi|hello|hey', ['Hi there!', 'Hello!', 'Hey!']),
    (r'how are you', ['I am good, thank you!', 'I am doing well.']),
    (r'what is your name', ['I am a chatbot. You can call me ChatGPT.']),
    # Add more patterns and responses as needed
]

# Define reflections for pronoun swapping
reflections = {
    "I am": "you are",
    "I was": "you were",
    "I": "you",
    "my": "your",
    "you are": "I am",
    "you were": "I was",
    "your": "my",
}

# Create a chatbot using the patterns and reflections
chatbot = Chat(patterns, reflections)

# Define a function to interact with the chatbot
def chat_with_bot():
    print("Hello! I'm your chatbot. Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
        response = chatbot.respond(user_input)
        print("Chatbot:", response)

# Start the conversation
chat_with_bot()