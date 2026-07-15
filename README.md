# 🎙️ Voice-Based Concept Understanding Analyzer (VBCUA)

## 📌 Project Overview
The Voice-Based Concept Understanding Analyzer (VBCUA) is an AI-powered educational assessment system that evaluates a student's conceptual understanding through spoken explanations. The application converts speech into text, compares the explanation with reference content using semantic similarity, analyzes speech quality metrics, and generates a detailed PDF report.

---

## 🚀 Features

- 🎤 Audio upload and speech recording
- 📝 Speech-to-text transcription using OpenAI Whisper
- 🧠 Semantic similarity evaluation using Sentence-BERT
- 📊 Audio quality analysis
  - Filler Word Ratio
  - Pause Ratio
  - RMS Energy (Confidence)
- 📈 Final understanding score calculation
- 📄 Automatic PDF report generation
- 🌊 Waveform visualization
- 💻 Interactive Streamlit interface

---

## 🛠️ Technologies Used

- Python
- Streamlit
- OpenAI Whisper
- Sentence-BERT (SBERT)
- Librosa
- NumPy
- SQLite
- ReportLab
- Matplotlib

---

## 📂 Project Structure

```
VOICE-BASE-ANALYSER/
│
├── __pycache__/              # Python cache files
├── .venv/                    # Virtual environment
├── venv/                     # Another virtual environment (optional)
│
├── .gitignore                # Files/folders ignored by Git
├── app.py                    # Main Streamlit application
├── app_backup.py             # Backup of the main application
├── audio_utils.py            # Audio loading and feature extraction
├── speech_to_text.py         # Speech-to-text using Whisper
├── semantic_eval.py          # Semantic similarity evaluation (Sentence-BERT)
├── scoring_engine.py         # Final score and understanding level calculation
├── report_generator.py       # PDF report generation
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

---

## ⚙️ Workflow

1. User uploads an audio file.
2. Audio is converted into text using Whisper.
3. Speech features are extracted.
4. Transcript is compared with reference content using SBERT.
5. Semantic similarity and speech metrics are calculated.
6. Final understanding score is generated.
7. A detailed PDF report is created for the user.

---

## 📊 Evaluation Metrics

- Semantic Similarity Score
- Filler Word Ratio
- Pause Ratio
- RMS Energy
- Final Understanding Score
- Understanding Level (Strong / Moderate / Poor)

---

## 📄 Output

The application generates:

- Speech Transcript
- Waveform Visualization
- Evaluation Metrics
- Understanding Level
- Downloadable PDF Report

---

## ▶️ Run the Project

Create and activate a virtual environment (optional), then install the required packages.

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

---

