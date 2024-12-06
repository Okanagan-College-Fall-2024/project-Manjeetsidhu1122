import logging
import subprocess
import shutil
import re
from datetime import datetime

# Configure logging
log_filename = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Check if ollama is installed
def check_ollama():
    if not shutil.which("ollama"):
        logging.critical("Ollama is not installed or not in PATH.")
        print("Error: Ollama is not installed or not in PATH. Please install it and try again.")
        exit(1)

# Use case text
use_case_text = """
Bullfighting: Art or Not?
Bullfighting has its roots in rituals dating back many centuries. In its modern Spanish style, 
bullfighting first became a prominent cultural event in the early 18th century. Yet despite its 
cultural significance, bullfighting continues to face increasing scrutiny in light of animal rights 
issues.
Some people consider bullfighting a cruel sport in which the bull suffers a severe and tortuous 
death. Many animal rights activists often protest bullfighting in Spain and other countries, citing 
the needless endangerment of the bull and bullfighter. Some cities around the world where 
bullfighting was once popular, including Coslada (Spain), Mouans-Sartoux (France), and Teocelo 
(Mexico), have even declared themselves to be anti-bullfighting cities. Other places, including 
some towns in Catalonia (Spain), have ceased killing the bull in the fight, but continue bullfighting.
To other people, the spectacle of the bullfight is not mere sport. The event is not only culturally 
significant, but also a fine art in which the bullfighter is trained in a certain style and elicits emotion 
through the act of the fight. Writer Alexander Fiske-Harrison, in his research and training as a 
bullfighter, defends the practice and circumstances of the bull, “In terms of animal welfare, the fighting 
bull lives four to six years whereas the meat cow lives one to two. …Those years are spent free 
roaming…” And others similarly argue that the death of the bull in the ring is more humane than the death 
of animals in a slaughterhouse.
"""

# List of questions
questions = [
    "How is the controversy over bullfighting related to the concept of relativism?",
    "How would a relativist interpret this controversy? How might a pluralist’s perspective differ?",
    "Do you believe that bullfighting is an ethically wrong practice or a justifiable cultural event? Explain your reasoning.",
    "In what ways might ethnocentrism affect your perspective on bullfighting? How would your opinion differ if you were raised in a different culture?",
    "Do you agree that the death of the bull in the ring is more humane than the death of animals in a slaughterhouse? Why or why not? What ethical concerns are raised by both situations?",
]

# Function to query the Ollama model with Plain Text format
def query_ollama(prompt, model="llama2"):
    try:
        result = subprocess.run(
            ["C:\\Users\\Manjeet Singh\\AppData\\Local\\Programs\\Ollama\\ollama.exe", "run", model, "--format", "text"],  # Use 'text' format for plain text output
            input=prompt,
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            raise Exception(result.stderr.strip())
        
        # Clean up any unwanted escape sequences from the output
        cleaned_output = re.sub(r'\x1b\[[0-9;?]*[a-zA-Z]', '', result.stdout.strip())  # Remove escape sequences
        logging.debug(f"Raw plain text output:\n{cleaned_output}")

        return cleaned_output
    except Exception as e:
        logging.error(f"Error querying Ollama: {str(e)}")
        return f"Error: {str(e)}"

# Main processing function
def process_questions(use_case, questions):
    responses = {}
    for question in questions:
        prompt = f"Use Case:\n{use_case}\n\nQuestion:\n{question}"
        logging.info(f"Sending question to model: {question}")
        response = query_ollama(prompt)
        responses[question] = response
        logging.info(f"Response: {response[:100]}...")  # Log the first 100 characters
    return responses

# Save responses to a text file
if __name__ == "__main__":
    check_ollama()
    try:
        responses = process_questions(use_case_text, questions)
        output_filename = "responses.txt"
        
        # Save the responses to a plain text file
        with open(output_filename, "w") as f:
            for question, response in responses.items():
                f.write(f"Question: {question}\n")
                f.write(f"Response: {response}\n\n")
        
        logging.info(f"Responses saved to '{output_filename}'")
        print(f"Responses saved to '{output_filename}'. Logs saved to '{log_filename}'.")
    except Exception as e:
        logging.critical(f"Failed to save responses: {str(e)}")
        print(f"Critical Error: {str(e)}")
