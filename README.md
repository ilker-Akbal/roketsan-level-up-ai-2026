# ROKETSAN Level Up AI 2026 — Workshop Practice

Personal study repository containing the exercises, experiments, and workshop implementations I worked on while preparing for and attending the **ROKETSAN Level Up AI 2026** workshop series.

> **Disclaimer:** This is a personal learning repository and is not an official ROKETSAN repository. Secrets, generated model artifacts, large videos, frame sequences, and local caches are intentionally excluded from version control.

## Topics

The repository is organized around three workshop days:

1. **LLM, RAG & AI Agents**
   - Large language model basics
   - Prompting and grounding
   - Embeddings and vector search
   - FAISS retrieval
   - RAG pipelines
   - Tool-using agents and conversation memory

2. **Computer Vision, YOLO & Tracking**
   - Image preprocessing
   - Transfer learning with MobileNetV2
   - YOLO object detection
   - ByteTrack-based multi-object tracking

3. **Sensor Fusion, Navigation & Control**
   - Alpha-Beta filtering
   - Navigation filtering
   - Radar track filtering
   - GPS/INS fusion and localization
   - Coordinate frames
   - PID control
   - A* path planning
   - 1D EKF SLAM

Additional practice material contains local RAG experiments with **Sentence Transformers + FAISS + Ollama** and small YOLO detection/tracking exercises.

## Repository Structure

```text
.
├── day-01-llm-rag-agents/
│   ├── agent.py
│   ├── create_vector.py
│   ├── main.py
│   ├── mil_std_document.py
│   ├── rag.py
│   └── tools.py
├── day-02-computer-vision/
│   ├── config/
│   │   └── bytetrack.yaml
│   ├── data/
│   │   ├── sample.jpg
│   │   └── video_sequence/
│   ├── outputs/
│   ├── classification.py
│   ├── detection_tracking.py
│   └── preprocessing.py
├── day-03-sensor-fusion-navigation/
│   └── notebooks/
├── practice/
│   ├── llm/
│   │   ├── local-rag/
│   │   └── notes/
│   └── yolo/
├── requirements/
├── .env.example
└── .gitignore
```

## Setup

Python 3.10+ is recommended. Create and activate a virtual environment before installing a section's dependencies.

### Day 1 — LLM / RAG / Agents

```bash
pip install -r requirements/day-01.txt
```

Copy the environment template and add your own Google API key:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Then build the local FAISS index before running RAG or the agent:

```bash
cd day-01-llm-rag-agents
python create_vector.py
python rag.py
python agent.py
```

The `faiss_index/` directory is generated locally and ignored by Git.

### Day 2 — Computer Vision / YOLO / Tracking

```bash
pip install -r requirements/day-02.txt
cd day-02-computer-vision
```

Run image preprocessing:

```bash
python preprocessing.py
```

For frame-based vehicle tracking, place JPG frames inside:

```text
day-02-computer-vision/data/video_sequence/
```

Then run:

```bash
python detection_tracking.py
```

Ultralytics can download the YOLO model weights automatically when they are not already available locally. Model weights and generated videos are not committed to this repository.

For transfer-learning classification, place a class-folder dataset under:

```text
day-02-computer-vision/data/Dataset/
```

and run:

```bash
python classification.py
```

### Day 3 — Sensor Fusion / Navigation

```bash
pip install -r requirements/day-03.txt
jupyter notebook day-03-sensor-fusion-navigation/notebooks
```

## Local RAG Practice

The `practice/llm/local-rag/` examples explore a local pipeline based on:

- PyMuPDF for PDF extraction
- multilingual Sentence Transformers embeddings
- FAISS cosine-similarity retrieval
- Ollama for local LLM inference
- simple conversation memory and tool-using agent experiments

Install the dependencies with:

```bash
pip install -r requirements/practice-llm.txt
```

The examples expect a compatible Ollama model to be installed locally. The model name used in the scripts can be changed to match your local installation.

### OpenRAG Bench — actual local FAISS integration

The original six-snippet local FAISS retriever is now also exercised through
**OpenRAG Bench v0.6.0** (the separately published MIT open-source project).
The evaluator captures real Sentence Transformers + FAISS rankings with stable
chunk IDs for two cosine-score thresholds, runs the Guard policy, and creates a
standalone HTML report. **Ollama and Gemini are not needed** for this retrieval
evaluation.

~~~bash
python -m pip install "sentence-transformers==5.1.1" "transformers==4.57.1" "faiss-cpu==1.12.0"
python -m pip install https://github.com/ilker-Akbal/openrag-bench/releases/download/v0.6.0/openrag_bench-0.6.0-py3-none-any.whl
python practice/llm/local-rag/openrag_bench_eval.py --output-dir reports/openrag-faiss-first
~~~

The first run downloads the public embedding model. The test uses a **tiny
author-labeled synthetic corpus** and represents **first-party integration
only**, not independent adoption or real-manual quality evidence. Complete
instructions and CI verification:
[OpenRAG Bench integration](docs/OPENRAG_BENCH_INTEGRATION.md).

## YOLO Practice

Install:

```bash
pip install -r requirements/practice-yolo.txt
```

Place local videos in `practice/yolo/data/` using the filenames referenced by the scripts, or update the paths in the examples.

## Repository Hygiene

The following are intentionally excluded:

- `.env` files and API keys
- Python caches
- generated FAISS indexes
- YOLO/model weight files
- large videos and frame sequences
- generated output media

This keeps the repository small, reproducible, and safe to publish.

## Notes

This repository documents a learning process rather than a production system. Some scripts are intentionally compact so the underlying concepts remain easy to follow.
