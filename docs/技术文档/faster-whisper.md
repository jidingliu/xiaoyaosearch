https://hf-mirror.com/Systran/faster-whisper-base

# Whisper base model for CTranslate2
This repository contains the conversion of openai/whisper-base to the CTranslate2 model format.

This model can be used in CTranslate2 or projects based on CTranslate2 such as faster-whisper.

## Example
```
from faster_whisper import WhisperModel

model = WhisperModel("base")

segments, info = model.transcribe("audio.mp3")
for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

```