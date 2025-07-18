#!/bin/bash
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Downloading NLTK data..."
python -c "import nltk; nltk.download('stopwords')"