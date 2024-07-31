# This file contains the prompts that the user will be asked during the call.
import re

# List of questions to ask the user
questions= ["Say or use the keypad to enter your callback number?", "Are you the patient?", "Please directly say or use the key pad and provide your date of birth?", "Got it. Are you a biological male or female?", "What state are you in right now? ", "Perfect. In a few words, please tell me your main symptom or reason for the call today."]

def extract_yes_or_no(buffer): # used for confirming the information is correct
    """Extracts a yes or no response from the buffer."""

    # Define possible affirmative and negative responses
    positive_responses = ["yes", "yeah", "yep", "yup", "correct", "right", "affirmative", "1", "one"]
    negative_responses = ["no", "nope", "incorrect", "wrong", "negative", "2", "two"]

    # Use any() for concise checking
    if any(re.search(rf"\b{re.escape(response)}\b", buffer, re.IGNORECASE) for response in positive_responses):
        return "yes"
    elif any(re.search(rf"\b{re.escape(response)}\b", buffer, re.IGNORECASE) for response in negative_responses):
        return "no"
    else:
        return None


def delete_last_line(filename): # Function to delete the last line from a file, used if info is incorrect
    """Deletes the last line from the given file."""
    with open(filename, "r") as f:
        lines = f.readlines()
    with open(filename, "w") as f:
        f.writelines(lines[:-1])  # Write all lines except the last one

