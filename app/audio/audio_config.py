import os

# Kokoro downloads its model and voices through Hugging Face.  Keep both those
# files and generated WAVs outside the project checkout so deployment does not
# depend on the old Piper installation or on a particular PythonAnywhere user.
KOKORO_HOME = os.path.expanduser(os.environ.get("KOKORO_HOME", "~/.cache/happyenglish/kokoro"))

# Hugging Face reads HF_HOME when its package is imported.  english.py imports
# this module before importing Kokoro, so this default is applied consistently
# for the web app and for local development.  An explicit environment variable
# still takes precedence.
HF_HOME = os.environ.setdefault(
    "HF_HOME",
    os.path.join(KOKORO_HOME, "huggingface"),
)

CACHE_DIR = os.path.expanduser(
    os.environ.get(
        "KOKORO_AUDIO_CACHE_DIR",
        os.path.join(KOKORO_HOME, "audio"),
    )
)

os.makedirs(CACHE_DIR, exist_ok=True)
