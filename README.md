# YouTube-Video-Transcriber-Summarizer
This project allows users to input a YouTube video URL, download the audio, transcribe the audio using Google Cloud Speech-to-Text API, and summarize the transcription using Natural Language Processing (NLP) via spaCy.

## Features
- **YouTube Audio Download**: Extracts audio from a YouTube video using `yt-dlp`.
- **Google Cloud Transcription**: Transcribes audio files using Google Cloud's Speech-to-Text API.
- **NLP Summarization**: Summarizes the transcription using the `spaCy` library.
- **Web Interface**: Users interact with the system through a simple web interface built with Flask.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/KapilGoudLingala/YouTube-Video-Transcriber-Summarizer.git
   cd YouTube-Video-Transcriber-Summarizer

2. Set Up Google Cloud:

    Create a Google Cloud account and enable the Speech-to-Text API.
    Download your Google Cloud credentials JSON file and save it to your project folder (this file should not be uploaded to GitHub).
    Set the environment variable for your Google Cloud credentials:
    export GOOGLE_APPLICATION_CREDENTIALS="path_to_your_credentials_file.json"

3. Install Dependencies:
Create a virtual environment and install the necessary Python libraries:
bash

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

4. Run the Application:
Start the Flask development server:
bash

python app.py

5. Access the Application:
Open your web browser and go to:
bash

http://127.0.0.1:5000/


Usage

  1.On the homepage, enter a YouTube video URL.
  2.Click the "GET TRANSCRIPTION AND SUMMARY" button.
  3.Wait for the system to process the video and display the transcription and summary on the results page.

Project Structure
bash

.
├── app.py                     # Main Flask application
├── processing.py               # Contains the logic for downloading, transcribing, and summarizing
├── templates/
│   ├── index.html              # Homepage template
│   ├── result.html             # Results page template
├── static/
│   ├── style.css               # CSS for the web pages
├── requirements.txt            # Python dependencies
├── .gitignore                  # Files to be ignored by Git
├── README.md                   # Project documentation
├── LICENSE                     # License information

Technologies Used

    Python: Core programming language
    Flask: Web framework for building the web interface
    yt-dlp: For downloading YouTube videos
    Google Cloud Speech-to-Text: For transcription
    spaCy: For natural language processing and summarization
    HTML/CSS: For creating the frontend



