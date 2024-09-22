# app.py

from flask import Flask, request, jsonify, render_template
from processing import download_audio_from_youtube, upload_to_gcs, transcribe_audio_from_gcs, get_video_summary

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_video():
    video_url = request.form.get('video_url')
    bucket_name = request.form.get('bucket_name', 'chin1')  # Default to 'chin1' if not provided

    if not video_url:
        return jsonify({'error': 'No video URL provided'}), 400
    
    # Step 1: Download audio from YouTube
    audio_file_path = download_audio_from_youtube(video_url)
    
    if not audio_file_path:
        return jsonify({'error': 'Failed to download audio from YouTube'}), 500
    
    # Step 2: Upload audio to GCS
    destination_blob_name = "audio/audio.wav"
    gcs_uri = upload_to_gcs(bucket_name, audio_file_path, destination_blob_name)
    
    if not gcs_uri:
        return jsonify({'error': 'Failed to upload audio to GCS'}), 500
    
    # Step 3: Transcribe audio from GCS
    transcript = transcribe_audio_from_gcs(gcs_uri)
    
    if not transcript:
        return jsonify({'error': 'Failed to transcribe audio'}), 500
    
    # Step 4: Summarize the transcription
    summary = get_video_summary(transcript)
    
    return render_template('result.html', transcription=transcript, summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
