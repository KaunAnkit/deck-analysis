# Deck Analyzer

AI-powered analysis of decks with automated insights and feedback.

## Overview

This tool analyzes PDF pitch decks using OCR and AI to provide structured feedback, identify key elements, and generate actionable insights. It also supports generating personalized cold emails based on deck analysis.

## Features

- PDF pitch deck processing and OCR extraction
- AI-powered analysis using Groq API
- Deck evaluation and scoring
- Visual analysis of slides
- Cold email generation
- REST API for easy integration
- Web-based frontend

## Requirements

- Python 3.8+
- FastAPI
- EasyOCR
- PyMuPDF
- Groq API key

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Create `.env` file with your Groq API key: `GROQ_API_KEY=your_key_here`

## Usage

Start the server:
```
uvicorn main:app --reload
```

Upload a pitch deck via the API:
```
POST /upload
- file: PDF file
- deck_goal: Goal of the pitch deck
- deck_type: Type of deck (e.g., startup, fundraising)
- fund_size: Target fund size (optional)
- growth_focus: Growth focus area (optional)
- deck_timeline: Timeline (optional)
```

## Project Structure

- `main.py` - FastAPI application entry point
- `analysis_pipeline.py` - Core analysis logic
- `deck_judge.py` - Deck evaluation and scoring
- `image_analysis.py` - Visual analysis
- `ocr_pdf.py` - PDF text extraction
- `agents/` - LLM client implementations
- `cold_mail/` - Cold email generation pipeline
- `frontend/` - Web UI
- `reports/` - Generated analysis reports