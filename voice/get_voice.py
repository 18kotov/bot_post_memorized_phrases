from gtts import gTTS
from pathlib import Path
from settings import get_logger

logger = get_logger(__name__)


def convert_text_to_speech(text: str):
    try:
        # Create gTTS object and specify the language
        tts = gTTS(text=text, lang="en")
        # Save the audio file
        file_path = Path.cwd() / "voice/output.mp3"
        file_path.unlink(missing_ok=True)
        tts.save(file_path)

    except Exception as error:
        logger.error(error)


if __name__ == '__main__':
    pass
