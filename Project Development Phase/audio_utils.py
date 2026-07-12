import io


def _reset_file(file_obj):
    try:
        file_obj.seek(0)
    except Exception:
        pass


def load_audio(file_obj, sr=16000):
    import soundfile as sf

    _reset_file(file_obj)
    data, samplerate = sf.read(file_obj)
    _reset_file(file_obj)
    return data, samplerate


def extract_audio_features(file_obj):
    try:
        import numpy as np
    except Exception:
        np = None

    try:
        data, sr = load_audio(file_obj)
        if np is None:
            return {"rms_energy": 0.0, "pause_ratio": 0.0, "filler_ratio": 0.0}
        rms = float(np.sqrt(np.mean(data**2)))
        pause_ratio = float(np.mean(np.abs(data) < 1e-4))
        return {"rms_energy": rms, "pause_ratio": pause_ratio, "filler_ratio": 0.0}
    except Exception:
        return {"rms_energy": 0.0, "pause_ratio": 0.0, "filler_ratio": 0.0}


def save_waveform(file_obj):
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return None

    try:
        data, sr = load_audio(file_obj)
        fig, ax = plt.subplots(figsize=(8, 2.2), facecolor="#0f1726")
        ax.plot(data, color="#38bdf8", linewidth=1.1)
        ax.set_facecolor("#08101f")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_color("#334155")
        ax.spines["left"].set_color("#334155")
        ax.tick_params(colors="#94a3b8")
        ax.set_xticks([])
        ax.set_yticks([])
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
        buf.seek(0)
        plt.close(fig)
        return buf
    except Exception:
        return None
