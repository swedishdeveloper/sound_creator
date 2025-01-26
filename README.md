# Robot Vacuum Cleaner Sound Manager

A Python tool for managing and creating sound files for robot vacuum cleaners. The tool can both generate new sound files from text and transcribe existing audio files.

## Features

- Generates WAV files from text using ElevenLabs Text-to-Speech API
- Transcribes existing audio files using OpenAI Whisper
- Manages a JSON file that maps sound filenames to their text content
- Supports multiple languages through ElevenLabs multilingual v2 model

## Installation

1. Clone the project

2. Install ffmpeg:
   - On Ubuntu/Debian: `sudo apt-get install ffmpeg`
   - On macOS: `brew install ffmpeg`
   - On Windows: Download from https://ffmpeg.org/download.html

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with the following variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   ELEVENLABS_VOICE_ID=your_elevenlabs_voice_id
   ```

## Directory Structure

The tool expects the following directory structure:

```
.
├── sounds/
│   └── en/         # Source directory for input audio files
├── output/         # Generated WAV files
├── main.py
├── .env
└── file_texts.json # Generated mapping file
```

## Usage

### Generate Text-to-Speech Files

```bash
python main.py
```

This will:
1. Create a JSON file mapping all files in `sounds/en/` directory
2. Generate WAV files for any text entries in the JSON file
3. Save the generated files to the `output/` directory

### Transcribe Existing Audio Files

```bash
python main.py --transcribe
```

This will:
1. Read audio files from the `sounds/en/` directory
2. Transcribe them using OpenAI Whisper
3. Update the JSON file with the transcriptions

## Voice Settings

The generated audio uses the following ElevenLabs settings:
- Stability: 0.5
- Similarity Boost: 0.5
- Style: 0
- Model: eleven_multilingual_v2
- Output format: 16-bit PCM WAV, 16kHz, mono

## Requirements

- Python 3.x
- ffmpeg (for audio conversion)
- OpenAI API key (for Whisper transcriptions)
- ElevenLabs API key and voice ID (for text-to-speech)
- Internet connection for API calls
