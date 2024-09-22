# processing.py

from google.cloud import storage
from google.cloud import speech_v1p1beta1 as speech
from pydub import AudioSegment
import subprocess
import os
import yt_dlp
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

# Set up Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"path_to_your_credentials_file.json"

def download_audio_from_youtube(video_url, output_path="audio.wav"):
    try:
        command = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "wav",
            "--output", output_path,
            video_url
        ]
        subprocess.run(command, check=True)
        
        audio = AudioSegment.from_file(output_path)
        audio = audio.set_frame_rate(44100)  # Set sample rate if needed
        audio = audio.set_channels(1)  # Convert to mono
        audio.export(output_path, format="wav")
        
        return output_path
    except Exception as e:
        print(f"Error downloading or processing audio: {e}")
        return None

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        return f"gs://{bucket_name}/{destination_blob_name}"
    except Exception as e:
        print(f"Error uploading to GCS: {e}")
        return None

def download_from_gcs(bucket_name, source_blob_name, destination_file_name):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        return destination_file_name
    except Exception as e:
        print(f"Error downloading from GCS: {e}")
        return None

def transcribe_audio_from_gcs(gcs_uri):
    try:
        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(uri=gcs_uri)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code="en-IN",  # Adjust language as needed
        )
        operation = client.long_running_recognize(config=config, audio=audio)
        response = operation.result(timeout=360)
        
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript + '\n'
        
        return transcript
    except Exception as e:
        print(f"Error transcribing audio from GCS: {e}")
        return ""

def get_video_summary(transcript):
    try:
        result = transcript
        
        stopwords = list(STOP_WORDS)
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(result)
        
        tokens = [token.text for token in doc]
        word_freq = {}
        for word in doc:
            if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
                if word.text not in word_freq.keys():
                    word_freq[word.text] = 1
                else:
                    word_freq[word.text] += 1
        
        max_freq = max(word_freq.values(), default=1)
        for word in word_freq.keys():
            word_freq[word] = word_freq[word] / max_freq
        
        sent_tokens = [sent for sent in doc.sents]
        sent_scores = {}
        for sent in sent_tokens:
            for word in sent:
                if word.text in word_freq.keys():
                    if sent not in sent_scores.keys():
                        sent_scores[sent] = word_freq[word.text]
                    else:
                        sent_scores[sent] += word_freq[word.text]
        
        select_len = max(int(len(sent_tokens) * 0.2), 1)  # Ensure at least one sentence is selected
        summary = nlargest(select_len, sent_scores, key=sent_scores.get)
        final_summary = [sent.text for sent in summary]
        summary_text = " ".join(final_summary)
        
        return summary_text
    except Exception as e:
        print(f"Error summarizing transcript: {e}")
        return ""
