import re

def extract_callback_number(buffer): # Extracts the callback number from the buffer
    question="Say or use the keypad to enter your callback number?"
    #question = "What is your callback number?" # Define the question to extract the callback number
    start_index = buffer.find(question) + len(question)
    buffer = buffer[start_index:]

    # Extract all sequences of digits from the buffer
    digit_sequences = re.findall(r'\d+', buffer)
    # Join all sequences of digits into a single string
    joined_digits = ''.join(digit_sequences)

    # Find all 10-digit sequences in the joined digits
    matches = re.findall(r'\d{10}', joined_digits)

    if matches:
        # Return the first valid 10-digit phone number formatted correctly
        first_match = matches[0]
        formatted_number = f"({first_match[:3]}) {first_match[3:6]}-{first_match[6:]}"
        return formatted_number

    return None

def extract_is_patient(buffer): # Extracts whether the user is the patient from the buffer
    question = "Are you the patient?"
    start_index = buffer.find(question) + len(question) # Find the start index of the response
    buffer = buffer[start_index:].lower()  # convert buffer to lowercase for case-insensitive matching

    positive_responses = [ # Define possible affirmative responses
        "yes", "yeah", "i'm the patient", "i am the patient", "yep", "yup", "affirmative", "i am",
    ]

    negative_responses = [ # Define possible negative responses
        "no", "nope", "negative", "not the patient", "i am not", "i'm not", "i am not the patient", "i'm not the patient"
    ]

    for response in positive_responses: # Check for affirmative responses
        pattern = rf'\b{re.escape(response)}\b'
        match = re.search(pattern, buffer, re.IGNORECASE)
        if match:
            return "yes"

    for response in negative_responses: # Check for negative responses
        pattern = rf'\b{re.escape(response)}\b'
        match = re.search(pattern, buffer, re.IGNORECASE)
        if match:
            return "no"

    return None


'''def extract_date_of_birth(buffer):
    question = "Could you please provide your date of birth?"
    start_index = buffer.find(question) + len(question)
    buffer = buffer[start_index:].lower()  # Convert to lowercase for case-insensitive matching

    month_to_number = {
        'january': '01', 'february': '02', 'march': '03', 'april': '04',
        'may': '05', 'june': '06', 'july': '07', 'august': '08',
        'september': '09', 'october': '10', 'november': '11', 'december': '12'
    }

    # Expanded Patterns
    patterns = [
        r'\b(\d{1,2})[\s/.,-]+(\d{1,2})[\s/.,-]+(\d{4})\b',      # MM/DD/YYYY or MM-DD-YYYY etc.
        r'\b(\d{4})[\s/.,-]+(\d{1,2})[\s/.,-]+(\d{1,2})\b',      # YYYY/MM/DD or YYYY-MM-DD etc.
        r'\b(' + '|'.join(month_to_number.keys()) + r')\s+(\d{1,2})(st|nd|rd|th)?\s*,?\s+(\d{4})\b',  # Month DD(st/nd/rd/th) YYYY
        r'\b(\d{1,2})\s+(' + '|'.join(month_to_number.keys()) + r')\s+(\d{4})\b',  # DD Month YYYY
        r'the\s+(\d{1,2})(st|nd|rd|th)?\s+of\s+(' + '|'.join(month_to_number.keys()) + r')\s+(\d{4})\b', # The DDth of Month YYYY
    ]

    for pattern in patterns:
        match = re.search(pattern, buffer)
        if match:
            if len(match.groups()) == 3:  # MM/DD/YYYY, YYYY/MM/DD
                if pattern.startswith(r'\b(\d{4})'):  # YYYY/MM/DD format
                    year, month, day = match.groups()
                else:
                    month, day, year = match.groups()
                if month.isdigit():
                    month = int(month)
                else:
                    month = month_to_number[month]
                day = int(re.sub(r'\D', '', day))  # Remove non-digit characters and convert to int
                return f"{month:02d}/{day:02d}/{year}"
            elif len(match.groups()) >= 4:  # Month name formats
                if pattern.startswith(r'the\s+'):
                    day, _, month, year = match.groups()
                elif pattern.startswith(r'\b(\d{1,2})\s+'):
                    day, month, year = match.groups()
                else:
                    month, day, _, year = match.groups()
                month = month_to_number[month]
                day = int(re.sub(r'\D', '', day))  # Remove non-digit characters and convert to int
                return f"{month:02d}/{day:02d}/{year}"

    return None'''
def extract_date_of_birth(buffer): # Extracts the date of birth from the buffer
    question = "Please directly say or use the key pad and provide your date of birth?"
    start_index = buffer.find(question) + len(question) # Find the start index of the date of birth
    buffer = buffer[start_index:]

    month_to_number = { # Define a mapping of month names to month numbers
        'january': '01', 'february': '02', 'march': '03', 'april': '04',
        'may': '05', 'june': '06', 'july': '07', 'august': '08',
        'september': '09', 'october': '10', 'november': '11', 'december': '12'
    }
    # Check for date in format MM/DD/YYYY or MM-DD-YYYY
    match = re.search(r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b', buffer)
    if match:
        month, day, year = match.groups()
        return f"{int(month)}/{int(day)}/{year}"

    # Check for date in format Month DD, YYYY
    match = re.search(r'\b(\d{1,2}),\s?(\d{1,3}),\s?(\d{1,4})\b', buffer)
    if match:
        month, day, year = match.groups()
        if len(day) == 1 and len(year) == 4: # Check if the day is in the format D and year is in the format YYYY
            return f"{int(month)}/{int(day)}/{year}"
        elif len(day) == 3 and day[1] == '1' and day[2] == '2': # Check if the day is in the format DDth
            return f"{int(month)}/21/{year}"
        else:
            return f"{int(month)}/{int(day)}/{year}"

    # Check for date in format Month DDth, YYYY
    match = re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})(st|nd|rd|th)?,?\s+(\d{4})\b', buffer, re.IGNORECASE)
    if match:
        month, day, _, year = match.groups()
        month_number = month_to_number[month.lower()] # Convert the month name to a month number
        return f"{int(month_number)}/{int(day)}/{year}"

    # Check for date in format Month DD, YYYY
    match = re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})\s+(\d{4})\b', buffer, re.IGNORECASE)
    if match:
        month, day, year = match.groups()
        month_number = month_to_number[month.lower()] # Convert the month name to a month number
        return f"{int(month_number)}/{int(day)}/{year}"

    # Check for date in format MM/DD/YY
    match = re.search(r'\b(\d{1})(\d{2})(\d{4})\b', buffer)
    if match:
        month, day, year = match.groups()
        if year[0] in ['1', '2']: # Check if the year is in the 21st or 22nd century
            return f"{int(month)}/{int(day)}/{year}" # Return the date in MM/DD/YYYY format

    return None

def extract_gender(buffer): # Extracts gender from the buffer
    question = "Got it. Are you a biological male or female?"
    start_index = buffer.find(question) + len(question)
    buffer = buffer[start_index:]

    male_pattern = r'\b(male|boy|man)\b'
    female_pattern = r'\b(female|girl|woman)\b'

    male_matches = re.findall(male_pattern, buffer, re.IGNORECASE)
    female_matches = re.findall(female_pattern, buffer, re.IGNORECASE)

    if female_matches:
        return "female"
    elif male_matches:
        return "male"

    return None

def extract_state(buffer): # Extracts the state from the buffer
    question = "What state are you in right now?"
    start_index = buffer.find(question) + len(question)
    buffer = buffer[start_index:]

    states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
              "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
              "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
              "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
              "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
              "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
              "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

    for state in states: # Check for each state in the buffer
        if re.search(r'\b' + re.escape(state) + r'\b', buffer, re.IGNORECASE):
            return state
    return None


def extract_symptom(buffer): # Extracts the main symptom from the buffer
    question = "Perfect. In a few words, please tell me your main symptom or reason for the call today."
    start_index = buffer.find(question) + len(question)
    symptom = buffer[start_index:].strip()

    if symptom:  # Check if there is any non-whitespace text
        return symptom
    else:
        return None  # Indicate that no symptom was provided



