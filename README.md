# Local Answering System

## Overview
Welcome to the Local Answering System repository. This project builds upon previous answering systems by integrating Twilio's APIs for messaging and gathering responses. It is a Python Flask application designed to manage incoming calls, collect caller responses, and store validated data in a local SQLite database. The system is designed to handle patient calls efficiently, capturing and validating key information before transferring the call to an appropriate healthcare provider.

### Features
- **Twilio API Integration:** Utilizes Twilio's APIs to manage incoming calls, gather responses, and handle DTMF (Dual-Tone Multi-Frequency) input and voice responses.
- **Database Integration:** Stores call data in a local SQLite database using SQLAlchemy, including caller information and their validated responses.
- **Error Handling:** Tracks errors during the response validation process, transferring the caller to a live agent if issues persist.
- **Voice Interaction:** Uses Twilio's VoiceResponse to interact with callers, asking questions and capturing their responses.

### How It Works
- **Ngrok Webhooks:** The application is deployed locally using ngrok to expose webhooks that handle Twilio's inbound call requests.
- **Database Entry:** A new row is created in the local SQLAlchemy database using the caller's SID (Session Identifier) when a call is received.
- **Question-Response Sequence:** The caller is asked a series of questions over the phone, and their responses are captured using Twilio's Gather feature, which accepts both DTMF input and voice responses depending on the question.
- **Data Validation:** Responses are processed using methods from `extraction.py`, validated, and then standardized before being stored in the database.

### Improvements and Further Development
- **Enhanced Transcript Management:** Implement logic to write and analyze the entire call transcript in the database, associating each transcript with the respective CallSid. This improvement will enhance the system's ability to handle large volumes of calls, providing better organization and retrieval of call data.
- **Deployment Optimization:** The enhanced transcript management will facilitate smoother deployment of the application, especially when scaling to handle large numbers of simultaneous calls.

### Project Structure
- **app.py:** Manages the main application flow, including call handling, question-response logic, and database operations.
- **extraction.py:** Contains methods for extracting and validating responses from the caller's input.
- **prompt.py:** Contains the list of questions asked by the Twilio API during the call.
- **config.py:** Sets up environment variables and configuration settings for Twilio's API credentials.

### Future Work
- **Enhanced Data Validation:** Improve the validation process with additional checks and user confirmation steps.
- **Twilio Service Integration:** Expand the application to use more Twilio services, potentially adding features like automated message follow-ups.
- **Deployment:** Deploy the application to a cloud platform for broader accessibility and scalability.


