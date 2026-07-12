"""Speech-to-text helper with optional Whisper support.

The function accepts a file-like object (Streamlit upload) or a file
path. If `whisper` (openai-whisper) is installed the model will be
used; otherwise a placeholder string is returned.
"""

def _read_bytes(file_obj):
    # If it's already a path string, return None to indicate path usage
    if isinstance(file_obj, str):
        return None
    try:
        file_obj.seek(0)
    except Exception:
        pass
    return file_obj.read()

def speech_to_text(file_obj):
    data = _read_bytes(file_obj)

    try:
        import whisper
        import tempfile
        import os

        model = whisper.load_model("small")

        if data is None and isinstance(file_obj, str):
            src_path = file_obj
        else:
            fd, src_path = tempfile.mkstemp(suffix=".wav")
            os.close(fd)
            with open(src_path, "wb") as f:
                f.write(data)

        try:
            result = model.transcribe(src_path)
            return result.get("text", "")
        finally:
            if data is not None and os.path.exists(src_path):
                try:
                    os.remove(src_path)
                except Exception:
                    pass

    except Exception:
        return "[transcript placeholder]"
