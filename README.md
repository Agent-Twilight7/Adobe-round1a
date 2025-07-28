# PDF Document Structure Extractor
## Adobe Hackathon Round 1A Submission

A Python-based solution that automatically extracts document structure and outline from PDF files using dynamic font size analysis and machine learning classification.

## 🎯 Approach

Our solution employs a **hybrid approach** combining:

1. **Dynamic Font Size Analysis**: Automatically detects document hierarchy by analyzing font sizes across the document
2. **Machine Learning Classification**: Uses pre-trained models to classify text elements and fonts
3. **Intelligent Text Extraction**: Leverages PyMuPDF for precise text extraction with font metadata

### Key Innovation
- **Adaptive Font Hierarchy Mapping**: Dynamically maps font sizes to heading levels (Title → H1 → H2 → H3 → Body) without requiring fixed thresholds
- **Robust Text Classification**: Handles various document formats and font variations through ML-based classification

## 🛠 Models and Libraries Used

### Core Libraries
- **PyMuPDF (fitz)**: Advanced PDF text extraction and font analysis
- **scikit-learn**: Machine learning models for text and font classification
- **NumPy**: Numerical operations and data processing

### Pre-trained Models
- **model.pkl**: Document structure classifier trained on heading patterns
- **label_encoder.pkl**: Label encoder for heading level classification
- **font_encoder.pkl**: Font characteristic encoder for typography analysis

### Model Architecture
- **Classification Algorithm**: Trained on document structure patterns
- **Feature Extraction**: Font size, font family, text position, and content analysis
- **Training Data**: Curated dataset of academic and technical documents

## 📋 Output Format

The solution produces clean, structured JSON output:

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

## 🚀 How to Build and Run

### Prerequisites
- Docker installed on your system
- PDF files to process

### Building the Container
```bash
# Clone the repository
git clone <repository-url>
cd adobe-round1a

# Build the Docker image
docker build -t pdf-extractor .
```

### Running the Solution
```bash
# Place your PDF files in the 'input' directory
# Run the container
docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output pdf-extractor

# Results will be saved as JSON files in the 'output' directory
```

### Local Development (Optional)
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python main.py
```
