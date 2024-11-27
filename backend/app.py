from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import re
import io
import PyPDF2
import docx

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 

HUGGING_FACE_API_URL = # Add your model api 
HUGGING_FACE_API_KEY =  # Add your Hugging Face API key

def get_video_id(url):
    if not url:
        print("Error: URL is None or empty.")
        return None
    try:
        pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})' 
        match = re.search(pattern, url)
        return match.group(1) if match else None
    except Exception as e:
        print(f"Error extracting video ID: {e}")
    return None

def fetch_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # print(" ".join([t["text"] for t in transcript]))
        return " ".join([t["text"] for t in transcript])
    except Exception as e:
        return e

def summarize_text(text, max_length=800, min_length=525):
    """
    Summarizes a given text using the Hugging Face API.
    """
    try:
        headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
        print(f"Sending text to Hugging Face: {text[:400]}...")  # Log first 300 chars
        response = requests.post(
            HUGGING_FACE_API_URL,
            headers=headers,
            json={
                "inputs": text[:3000],  # Hugging Face API supports up to ~3000 tokens
                "parameters": {
                    "max_length": max_length,
                    "min_length": min_length,
                    "length_penalty": 2.0,
                    "no_repeat_ngram_size": 3
                }
            }
        )
        print(f"API Response: {response.status_code}, {response.text}")  # Log response
        if response.status_code == 200:
            summary = response.json()[0]["summary_text"]
            return summary
        else:
            print("Error from API:", response.json())
            return None
    except Exception as e:
        print(f"Error in summarize_text: {e}")
        return None


def chunk_text(text, chunk_size=400, overlap=50):
    """
    Splits text into chunks with overlapping words for better context retention.
    """
    words = text.split()
    for i in range(0, len(words), chunk_size - overlap):
        yield " ".join(words[i:i + chunk_size])

def summarize_large_text(text):
    """
    Summarizes a large text by chunking it, summarizing chunks, and combining results.
    """
    try:
        chunk_summaries = []
        for chunk in chunk_text(text):
            print(f"Summarizing chunk: {chunk[:100]}...")  # Log first 100 chars of each chunk
            summary = summarize_text(chunk, max_length=850, min_length=625)
            if summary:
                chunk_summaries.append(summary)
            else:
                print("Failed to summarize chunk.")
        
        combined_summary = " ".join(chunk_summaries)
        print(f"Combined chunk summary: {combined_summary[:150]}...")  # Log combined result

        # Summarize the combined chunk summaries into a detailed summary
        detailed_summary = summarize_text(combined_summary, max_length=800, min_length=625)
        return detailed_summary
    except Exception as e:
        print(f"Error in summarize_large_text_detailed: {e}")
        return None

def clean_format_paragraph(paragraph):
    # Remove extra spaces and newlines
    paragraph = re.sub(r'\s+', ' ', paragraph).strip()
    
    # Split the paragraph into sentences
    sentences = re.split(r'(?<=[.!?]) +', paragraph)
    
    # Create bullet points
    bullet_points = ['- ' + sentence for sentence in sentences]
    
    # Join the bullet points into a formatted string
    formatted_paragraph = '\n \n \n'.join(bullet_points)
    
    return formatted_paragraph

def extract_text_from_file(file):
    if file.filename.endswith('.txt'):
        return file.read().decode('utf-8')
    elif file.filename.endswith('.pdf'):
        reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif file.filename.endswith('.docx'):
        doc = docx.Document(io.BytesIO(file.read()))
        text = ""
        for para in doc.paragraphs:
            text += para.text
        return text
    else:
        return "Unsupported file format."
    

@app.route('/summary/all',methods=['POST'])
def summarizeAll():
    try:
        data=request.json
        text = data.get('text')
        video_url = data.get('video_url')
        file = request.files.get('file')

        if not text or not video_url or not file:
            return jsonify({"Error" : "Input field is required"}),400
        
        video_id = get_video_id(video_url)
        transcript = fetch_transcript(video_id)
        textFile = extract_text_from_file(file)

        combined_text = text + "\n \n"  + transcript +"\n \n"+ textFile

        summary = summarize_large_text(combined_text)
        if not summary:
            return jsonify({"error": "Could not generate summary"}), 500
        
        # Clean the format for the summary
        summaryPretty = clean_format_paragraph(summary)
        return jsonify({"summary": summaryPretty})

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@app.route('/summary/combined', methods=['POST'])
def summarize_combined():
    try:
        data = request.json
        text = data.get('text')
        video_url = data.get('video_url')

        if not text or not video_url:
            return jsonify({"error": "Both text and video URL are required"}), 400

        video_id = get_video_id(video_url)
        transcript = fetch_transcript(video_id)

        if not transcript:
            return jsonify({"error": "Could not retrieve transcript from YouTube"}), 400

        # Combine text and transcript
        combined_text = text + "\n \n" + "##### URL Content #####"+"\n \n" + transcript

        # Summarize combined text
        summary = summarize_large_text(combined_text)
        if not summary:
            return jsonify({"error": "Could not generate summary"}), 500
        
        # Clean the format for the summary
        summaryPretty = clean_format_paragraph(summary)
        return jsonify({"summary": summaryPretty})

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route('/summary/file', methods=['POST'])
def summarize_file():
    try:
        file = request.files.get('file')
        if not file:
            return jsonify({"error": "No file provided"}), 400

        # Extract text from file
        text = extract_text_from_file(file)
        if not text:
            return jsonify({"error": "Could not extract text from file"}), 400

        # Summarize the extracted text
        summary = summarize_large_text(text)
        if not summary:
            return jsonify({"error": "Could not generate summary"}), 500
        
        # Clean the format for the summary
        summaryPretty = clean_format_paragraph(summary)
        return jsonify({"summary": summaryPretty})

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500



@app.route('/summary/text', methods=["POST"])
def summarize_Text():
    try:
        data = request.json
        text = data.get('text')
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        # Summarize the provided text
        summary = summarize_large_text(text)
        if not summary:
            return jsonify({"error": "Could not generate summary"}), 500
        
        # Clean the format for the summary
        summaryPretty = clean_format_paragraph(summary)
        return jsonify({"summary": summaryPretty})

    except Exception as e:
        print(f"Error: {e}")  # Log the exception
        return jsonify({"error": "Internal server error", "details": str(e)}), 500




@app.route('/summary/youtube', methods=['POST'])
def summarize_video():
    try:
        data = request.json
        print(f"Received data: {data}")  # Log the incoming request
        video_url = data.get('video_url')
        if not video_url:
            return jsonify({"error": "No YouTube URL provided"}), 400
        
        video_id = get_video_id(video_url)
        print(f"Extracted video ID: {video_id}")  # Log extracted video ID

        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400
        
        transcript = fetch_transcript(video_id)
        print(f"Transcript: {transcript[:100]}")  # Log the first 100 characters of the transcript

        if not transcript:
            return jsonify({"error": "Could not retrieve transcript"}), 400

        summary = summarize_large_text(transcript)
        summaryPretty = clean_format_paragraph(summary)
        print(f"Summary: {summaryPretty}")  # Log the summary

        if not summary:
            return jsonify({"error": "Could not generate summary"}), 500

        return jsonify({"summary": summaryPretty})

    except Exception as e:
        print(f"Error: {e}")  # Log the exception
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
