# GraphRAG OCR Demo

This project demonstrates a Graph-based Retrieval Augmented Generation (GraphRAG) system with Optical Character Recognition (OCR) capabilities. It processes PDF documents, extracts text using OCR, and builds a knowledge graph for intelligent querying.

## Features

- PDF document processing with OCR
- Knowledge graph construction for enhanced retrieval
- Streamlit-based user interface for querying the system
- Integration with Neptune database for graph storage

## Setup


1. Download required models:
   ```
   python download_models_hf.py
   ```

2. Process PDF documents:
   ```
   python converter.py
   ```

3. Launch the Streamlit client:
   ```
   cd streamlint-client
   streamlit run app.py
   ```

## Project Structure

- `converter.py`: Converts PDFs to text using OCR
- `download_models_hf.py`: Downloads required Hugging Face models
- `knowledge-base-prompt.md`: Prompt templates for knowledge base interaction
- `output/`: Directory containing processed OCR output
- `streamlint-client/`: Streamlit web application
