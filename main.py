import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv
import argparse

def list_files_in_directory(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def create_json_file(directory, json_path):
    files = list_files_in_directory(directory)
    if not os.path.exists(json_path):
        data = {file: "" for file in files}
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        print(f"JSON file created at {json_path}. Fill in the text for each file.")
    else:
        print("JSON file already exists. Edit it to add text for the files.")

def read_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

def save_wav(file_name, text, output_directory, api_key, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/wav",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5,
            "style": 0
        },
        "model_id": "eleven_multilingual_v2"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        output_path = os.path.join(output_directory, f"{os.path.splitext(file_name)[0]}.wav")
        with open(output_path, 'wb') as audio_file:
            audio_file.write(response.content)
        print(f"WAV file saved: {output_path}")
    else:
        print(f"Error generating audio for {file_name}: {response.status_code}, {response.text}")

def transcribe_audio_to_text(file_path, openai_client):
    try:
        with open(file_path, "rb") as audio_file:
            response = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            print("Transcription: ", response.text.strip())
            return response.text.strip()
    except Exception as e:
        print(f"Error transcribing {file_path}: {e}")
        return ""

def update_json_with_transcriptions(directory, json_path, openai_client):
    if os.path.exists(json_path):
        data = read_json(json_path)
        for file_name in data.keys():
            file_path = os.path.join(directory, file_name)
            if os.path.exists(file_path):
                transcription = transcribe_audio_to_text(file_path, openai_client)
                if transcription:
                    data[file_name] = transcription

        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        print("JSON file updated with transcriptions.")
    else:
        print("JSON file not found. Please create it first.")

def main():
    parser = argparse.ArgumentParser(description='Process audio files and optionally transcribe them.')
    parser.add_argument('--transcribe', action='store_true', help='Enable transcription of audio files')
    args = parser.parse_args()

    directory = "../sounds/en/"
    json_path = "file_texts.json"
    output_directory = "./output"
    load_dotenv()
    elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
    voice_id = os.getenv('ELEVENLABS_VOICE_ID')
    openai_api_key = os.getenv('OPENAI_API_KEY')

    if not all([elevenlabs_api_key, voice_id, openai_api_key]):
        raise ValueError("Missing required environment variables. Please check your .env file.")

    openai_client = OpenAI(api_key=openai_api_key)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    create_json_file(directory, json_path)

    if os.path.exists(json_path):
        data = read_json(json_path)

        for file_name, text in data.items():
            if text.strip():
                save_wav(file_name, text, output_directory, elevenlabs_api_key, voice_id)
            else:
                print(f"No text provided for {file_name}. Skipping.")

    if args.transcribe:
        update_json_with_transcriptions(directory, json_path, openai_client)

if __name__ == "__main__":
    main()
