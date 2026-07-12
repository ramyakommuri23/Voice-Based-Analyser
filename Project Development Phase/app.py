import io
import os
import tempfile

import streamlit as st

from audio_utils import extract_audio_features, load_audio, save_waveform
from semantic_eval import semantic_similarity
from scoring_engine import evaluate_understanding
from speech_to_text import speech_to_text

TOPIC_CONTENT = {
    "Machine Learning": (
        "Machine Learning is a subset of Artificial Intelligence that enables systems "
        "to learn from data and improve over time without explicit programming."
    ),
    "Artificial Intelligence": (
        "Artificial Intelligence is the broader field of building intelligent machines "
        "that can perform tasks that normally require human intelligence."
    ),
    "Data Analytics": (
        "Data Analytics involves examining raw data to find patterns, draw conclusions, "
        "and support decision-making with actionable insights."
    ),
}


def _cache_data(func):
    if hasattr(st, "cache_data"):
        return st.cache_data(show_spinner=False)(func)
    return st.cache(allow_output_mutation=True)(func)


@_cache_data
def cached_file_bytes(uploaded_audio):
    uploaded_audio.seek(0)
    data = uploaded_audio.read()
    uploaded_audio.seek(0)
    return data


@_cache_data
def cached_transcript(file_bytes):
    try:
        return speech_to_text(io.BytesIO(file_bytes))
    except Exception:
        return "[transcript placeholder]"


@_cache_data
def cached_audio_features(file_bytes):
    return extract_audio_features(io.BytesIO(file_bytes))


@_cache_data
def cached_waveform(file_bytes):
    return save_waveform(io.BytesIO(file_bytes))


@_cache_data
def cached_duration(file_bytes):
    data, samplerate = load_audio(io.BytesIO(file_bytes))
    return len(data) / samplerate if samplerate else 0.0


def local_css():
    st.markdown(
        """
        <style>
        .appview-container, .main, .block-container { background: #060c18; color: #e2e8f0; }
        .stApp { background: #060c18; }
        .block-container { padding-top: 1.8rem; padding-bottom: 1.8rem; }
        .header-title { margin: 0; font-size: clamp(2rem, 3vw, 3.4rem); font-weight: 800; letter-spacing: -0.04em; }
        .header-subtitle { margin-top: 0.6rem; color: #94a3b8; max-width: 780px; line-height: 1.6; }
        .section-card { background: #0f1726; border: 1px solid rgba(148, 163, 184, 0.12); border-radius: 24px; padding: 24px; box-shadow: 0 24px 60px rgba(15, 23, 42, 0.18); }
        .section-title { margin-bottom: 0.75rem; font-size: 1.35rem; font-weight: 700; }
        .metric-card { background: #0b1220; border: 1px solid rgba(148, 163, 184, 0.12); border-radius: 20px; padding: 20px; margin-bottom: 18px; }
        .metric-row { display: flex; justify-content: space-between; gap: 16px; align-items: center; margin-bottom: 14px; }
        .metric-label { color: #cbd5e1; font-size: 0.95rem; }
        .metric-value { color: #f8fafc; font-size: 1.05rem; font-weight: 600; }
        .stButton>button { background-color: #2563eb !important; color: white !important; border-radius: 999px !important; padding: 0.9rem 1.8rem !important; border: 1px solid rgba(255,255,255,0.08) !important; box-shadow: 0 18px 45px rgba(37, 99, 235, 0.18) !important; }
        .stFileUploaderDropzone, .stAudio, textarea, .stTextArea>div, .stTextArea>div>div { background: #0f1726 !important; color: #e2e8f0 !important; border-radius: 18px !important; border: 1px solid rgba(148, 163, 184, 0.18) !important; }
        textarea, .stTextArea>div>div>div { min-height: 170px !important; }
        .stTextArea>div>div>textarea { color: #e2e8f0 !important; }
        .stFileUploader label, .stFileUploader span, .stSelectbox>div, .stSelectbox>label { color: #f8fafc !important; }
        .stAlert { border-radius: 18px !important; }
        .stAudio audio { background: #0f1726 !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_metric(label, value):
    st.markdown(
        f"<div class='metric-row'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div></div>",
        unsafe_allow_html=True,
    )


def write_pdf_report(report_data, waveform_buf):
    try:
        from report_generator import generate_pdf_report
    except Exception:
        return None

    tmp_file = None
    tmp_path = None
    try:
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        tmp_path = tmp_file.name
        tmp_file.close()
        generate_pdf_report(report_data, waveform_buf, tmp_path)
        with open(tmp_path, "rb") as f:
            return f.read()
    except Exception:
        return None
    finally:
        if tmp_path is not None:
            try:
                os.remove(tmp_path)
            except Exception:
                pass


def main():
    st.set_page_config(page_title="Voice-Based Concept Understanding", layout="wide")
    local_css()

    st.markdown(
        """
        <div style='padding-bottom: 1rem;'>
            <h1 class='header-title'>Voice-Based Concept Understanding Analyzer</h1>
            <p class='header-subtitle'>Analyze students' spoken responses with transcription, semantic similarity, and audio metrics in a fast, clean interface.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    control_left, control_right = st.columns([1.35, 0.95], gap="large")

    with control_left:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Upload Audio</div>", unsafe_allow_html=True)
        st.write("Choose a WAV, MP3, M4A, or OGG file and click Analyze to start.")
        uploaded_audio = st.file_uploader("", type=["wav", "mp3", "m4a", "ogg"], label_visibility="collapsed")
        if uploaded_audio is not None:
            uploaded_audio.seek(0)
            st.audio(uploaded_audio)
        st.markdown("</div>", unsafe_allow_html=True)

    with control_right:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Reference Concept</div>", unsafe_allow_html=True)
        topic = st.selectbox("Select Topic", list(TOPIC_CONTENT.keys()))
        reference = st.text_area("", value=TOPIC_CONTENT[topic], height=200, label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

    analyze = st.button("Analyze Concept Understanding")

    if analyze:
        if uploaded_audio is None:
            st.warning("Please upload an audio file before analysis.")
            return

        file_bytes = cached_file_bytes(uploaded_audio)

        with st.spinner("Analyzing concept understanding..."):
            transcript = cached_transcript(file_bytes)
            audio_features = cached_audio_features(file_bytes)
            similarity = semantic_similarity(reference, transcript)
            score, level, color = evaluate_understanding(
                similarity,
                audio_features.get("filler_ratio", 0.0),
                audio_features,
            )
            duration_sec = cached_duration(file_bytes)
            waveform_buf = cached_waveform(file_bytes)

        st.success("Analysis Completed Successfully!")

        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        result_left, result_right = st.columns([1.4, 1], gap="large")

        with result_left:
            st.markdown("<div class='section-title'>Transcript</div>", unsafe_allow_html=True)
            st.write(transcript or "No transcript was generated.")
            if waveform_buf is not None:
                st.markdown("<div class='section-title' style='margin-top: 1.5rem;'>Audio Waveform</div>", unsafe_allow_html=True)
                st.image(waveform_buf, width=640)

        with result_right:
            st.markdown("<div class='score-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>Final Evaluation</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 3rem; font-weight: 800; margin: 0;'> {score}/100</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 1rem; margin-top: 0.4rem; color: {color}; font-weight: 700;'>{level}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            render_metric("Semantic Similarity", f"{similarity:.2f}")
            render_metric("Duration", f"{duration_sec:.2f} sec")
            render_metric("RMS Energy", f"{audio_features.get('rms_energy', 0.0):.4f}")
            render_metric("Pause Ratio", f"{audio_features.get('pause_ratio', 0.0):.4f}")
            render_metric("Filler Ratio", f"{audio_features.get('filler_ratio', 0.0):.4f}")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        pdf_bytes = write_pdf_report(
            {
                "Reference": reference,
                "Transcript": transcript,
                "Semantic Similarity": f"{similarity:.2f}",
                "Filler Word Ratio": f"{audio_features.get('filler_ratio', 0.0):.4f}",
                "Pause Ratio": f"{audio_features.get('pause_ratio', 0.0):.4f}",
                "Confidence (Energy)": f"{audio_features.get('rms_energy', 0.0):.5f}",
                "Final Score": score,
                "Understanding Level": level,
            },
            waveform_buf,
        )

        if pdf_bytes:
            st.download_button(
                "Download PDF report",
                data=pdf_bytes,
                file_name="understanding_report.pdf",
                mime="application/pdf",
            )
        else:
            st.info("PDF report generation is unavailable. Install reportlab and report_generator support.")


if __name__ == "__main__":
    main()
