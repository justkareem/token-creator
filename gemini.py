import os
import google.generativeai as genai
from typing_extensions import TypedDict
import uuid
import json
import requests

# Configure Gemini API
genai.configure(api_key="***************")


class MemeCoinAnalysis(TypedDict):
    meme_level: float  # Assuming it's a float between 1-10    ticker: str  # Ticker symbol for the coin
    coin_name: str  # Name of the coin
    ticker: str  # Ticker symbol for the coin
    coin_description: str  # Description of the coin


# Function to upload files to Gemini
def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    try:
        file = genai.upload_file(path, mime_type=mime_type)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file
    except Exception as e:
        print(f"Error uploading file to Gemini: {e}")
        return None


# Create the Gemini model
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
    "response_schema": MemeCoinAnalysis,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)


# Function: Analyze tweet with Gemini API, including images
def analyze_tweet_with_gemini(tweet_details, media_urls):
    """Analyze a tweet with Gemini, including text and image(s)."""
    uploaded_files = []
    for url in media_urls:
        try:
            image_response = requests.get(url)
            image_response.raise_for_status()
            file_path = f"temp_image_{uuid.uuid4().hex}.jpg"
            with open(file_path, "wb") as img_file:
                img_file.write(image_response.content)

            uploaded_file = upload_to_gemini(file_path, mime_type="image/jpeg")
            if uploaded_file:
                uploaded_files.append(uploaded_file)

            os.remove(file_path)
        except requests.RequestException as re:
            print(f"Error downloading image {url}: {re}")
        except Exception as e:
            print(f"Error uploading or handling image {url}: {e}")

    # Start chat session with Gemini
    chat_session = model.start_chat()
    text = f"""Tweet Analysis:
    Text: {tweet_details['text']}
    Author: {tweet_details['author_name']} (@{tweet_details['author_screen_name']})
    Likes: {tweet_details['likes']}
    Retweets: {tweet_details['retweets']}
    Replies: {tweet_details['replies']}
    Language: {tweet_details['lang']}
    Tweet created at: {tweet_details['created_at']}
    Tweet scraped at: {tweet_details['time']}
    Media: Attached
    Quote Tweet: {tweet_details.get('quote_tweet_text', 'None')}

    Evaluate Tweet Quality:
    - Engagement potential (e.g., likes, retweets)
    - Relevance and sentiment
    - Suitability for generating a coin
    - Meme level from 1-10 (be very critical)
    - Suggested coin name (max 3 words)
    All output should be based on crypto and memecoin trends and culture. Use crypto/memecoin lingo. 5/10 is my pass mark for creating a coin(rate accordinly)"""
    message_parts = uploaded_files + [text]

    try:
        response = chat_session.send_message({"role": "user", "parts": message_parts})
        structured_response = json.loads(response.text)  # Adjust this based on API's response format
        print(structured_response)
        return structured_response
    except KeyError as ke:
        print(f"Unexpected response format: {ke}")
        return None
    except Exception as e:
        print(f"Error analyzing tweet with Gemini: {e}")
        return None
