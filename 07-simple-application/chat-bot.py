# Use Groq
from groq import Groq

# Read the key from the file
f = open(r"E:\Lenovo Ideapad 330\company-material\ai-upskill\key-vault\groq\groq-api-key.txt", "r")
api_key = f.read().strip()
f.close()

# Intialize the Groq client
client = Groq(api_key=api_key)

# Select a model
MODEL = "llama-3.1-8b-instant"

# Create a function to generate responses from the model
def chat():
    pass

# Launch the model
if __name__ == "__main__":
    chat()