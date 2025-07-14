#app/services/ai/audio_generator.py

import os
import torch
import re
import tempfile
import shutil
from openvoice.api import ToneColorConverter
from openvoice import se_extractor
from melo.api import TTS
from pydub import AudioSegment

# Load the models once at module level for efficiency
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# NLTK resources are now properly installed

# Tone color converter (OpenVoice V2)
CONVERTER_PATH = "/Users/sbrsh/Code/OpenVoice/checkpoints_v2/converter"
tone_color_converter = ToneColorConverter(f'{CONVERTER_PATH}/config.json', device=device)
tone_color_converter.load_ckpt(f'{CONVERTER_PATH}/checkpoint.pth')

# MeloTTS will be initialized when needed

# Available voice styles for OpenVoice V2
VOICE_STYLES = {
    'default': 'neutral',
    'whispering': 'soft, quiet, secretive',
    'shouting': 'loud, excited, urgent',
    'excited': 'energetic, enthusiastic, animated',
    'cheerful': 'happy, upbeat, positive',
    'terrified': 'scared, frightened, nervous',
    'angry': 'frustrated, upset, mad',
    'sad': 'melancholy, sorrowful, down',
    'friendly': 'warm, welcoming, kind'
}

def analyze_story_emotion(text):
    """
    Analyze story text to determine appropriate voice style.
    Returns the best matching voice style for the content.
    """
    text_lower = text.lower()
    
    # Emotion keywords mapping
    emotion_keywords = {
        'cheerful': ['happy', 'joy', 'laugh', 'smile', 'fun', 'wonderful', 'amazing', 'magical', 'bright', 'sunny', 'delight', 'giggle', 'dance', 'sing'],
        'excited': ['wow', 'amazing', 'incredible', 'fantastic', 'adventure', 'explore', 'discover', 'magic', 'special', 'extraordinary', 'thrilling'],
        'sad': ['sad', 'cry', 'tear', 'miss', 'lonely', 'alone', 'sorry', 'regret', 'heart', 'broken', 'sorrow', 'melancholy'],
        'angry': ['angry', 'mad', 'furious', 'upset', 'frustrated', 'annoyed', 'grumpy', 'cross', 'irritated'],
        'terrified': ['scared', 'afraid', 'frightened', 'terrified', 'nervous', 'worried', 'anxious', 'fear', 'monster', 'dark', 'shadow'],
        'whispering': ['secret', 'whisper', 'quiet', 'soft', 'gentle', 'hush', 'silent', 'mysterious', 'magical'],
        'friendly': ['friend', 'kind', 'gentle', 'warm', 'welcome', 'help', 'care', 'love', 'hug', 'comfort'],
        'shouting': ['loud', 'shout', 'yell', 'call', 'urgent', 'emergency', 'help', 'danger', 'warning']
    }
    
    # Count emotion keywords in text
    emotion_scores = {}
    for style, keywords in emotion_keywords.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        emotion_scores[style] = score
    
    # Find the style with highest score
    if emotion_scores:
        best_style = max(emotion_scores, key=emotion_scores.get)
        if emotion_scores[best_style] > 0:
            return best_style
    
    # Default to cheerful for children's stories if no strong emotion detected
    return 'cheerful'

def add_story_pauses(text):
    """
    Add natural pauses to story text for better audio narration.
    Inserts pauses at sentence boundaries and key moments.
    """
    # Add pauses after sentences
    text = re.sub(r'([.!?])\s+', r'\1 ... ', text)
    
    # Add pauses for dramatic effect
    text = re.sub(r'([,;:])\s+', r'\1 ... ', text)
    
    # Add longer pauses for paragraph breaks
    text = re.sub(r'\n\s*\n', r' ... ... ... ', text)
    
    # Add pauses for character dialogue
    text = re.sub(r'"([^"]*)"', r'"\1" ... ', text)
    
    return text

def split_story_segments(text):
    """
    Split story into segments (sentences or paragraphs) for per-segment style analysis.
    Returns a list of (segment_text, segment_type) tuples.
    """
    # Split by double newlines (paragraphs)
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    segments = []
    for para in paragraphs:
        # Further split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', para)
        for sent in sentences:
            if sent.strip():
                segments.append((sent.strip(), 'sentence'))
    return segments

def generate_audio_from_text(text, output_path, speaker_wav=None, language="en", voice_style=None):
    """
    Generate audio from text using OpenVoice V2 with MeloTTS as base speaker.
    For each segment, detect emotion and generate audio with the corresponding style.
    Concatenate all segments into a single MP3 file.
    """
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Prepare temp directory for segment audio files
    with tempfile.TemporaryDirectory() as temp_dir:
        segments = split_story_segments(text)
        segment_audio_paths = []
        model = TTS(language='EN', device=device)
        speaker_ids = model.hps.data.spk2id
        speaker_key = list(speaker_ids.keys())[0]
        speaker_id = speaker_ids[speaker_key]
        
        for idx, (segment_text, _) in enumerate(segments):
            # Detect style for this segment
            seg_style = voice_style or analyze_story_emotion(segment_text)
            if seg_style not in VOICE_STYLES:
                seg_style = 'cheerful'
            # Add natural pauses to the segment
            enhanced_text = add_story_pauses(segment_text)
            temp_wav_path = os.path.join(temp_dir, f'segment_{idx}.wav')
            # Generate audio for this segment
            print(f"[Segment {idx}] Style: {seg_style} | Text: {enhanced_text}")
            model.tts_to_file(enhanced_text, speaker_id, temp_wav_path, speed=1.0)
            segment_audio_paths.append(temp_wav_path)
        
        # Concatenate all segments using pydub
        combined = AudioSegment.empty()
        for seg_path in segment_audio_paths:
            seg_audio = AudioSegment.from_wav(seg_path)
            combined += seg_audio
        # Export to temp WAV
        final_wav_path = os.path.join(temp_dir, 'final_story.wav')
        combined.export(final_wav_path, format='wav')
        
        # Convert to MP3 using ffmpeg
        import subprocess
        subprocess.run([
            'ffmpeg', '-i', final_wav_path, 
            '-acodec', 'libmp3lame', '-ab', '128k', 
            output_path, '-y'
        ], check=True, capture_output=True)
    
    print(f"Dynamic expressive audio generated at {output_path}")
    return output_path

def get_available_voice_styles():
    """
    Get list of available voice styles with descriptions.
    
    Returns:
        Dict mapping style names to descriptions
    """
    return VOICE_STYLES.copy()