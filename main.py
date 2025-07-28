from utils import process_pdf
from classifier import load_classifier
import os
import json
import numpy
import sys

print("✅ PDF Outline Extractor - Adobe Hackathon Round 1A")
print("✅ NumPy version:", numpy.__version__)
print("🐍 Python version:", sys.version)

def main():
    print("🚀 Starting main function...")
    
    # Define paths based on environment
    if os.path.exists("/app/input"):
        INPUT_DIR = "/app/input"
        OUTPUT_DIR = "/app/output"
    else:
        INPUT_DIR = "input"
        OUTPUT_DIR = "output"
    
    print(f"📂 Current working directory: {os.getcwd()}")
    print(f"📁 Checking if {INPUT_DIR} exists: {os.path.exists(INPUT_DIR)}")
    print(f"📁 Checking if {OUTPUT_DIR} exists: {os.path.exists(OUTPUT_DIR)}")
    
    # Load the trained models
    print("🔄 Loading classifier models...")
    clf, label_encoder, font_encoder = load_classifier()
    print("✅ Models loaded successfully.")

    # Get list of PDF files to process
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]
    print(f"📁 Found {len(pdf_files)} PDF file(s) to process.")

    for filename in pdf_files:
        input_path = os.path.join(INPUT_DIR, filename)
        print(f"📄 Processing: {filename}")

        # Extract document structure
        title, outline = process_pdf(input_path, clf, label_encoder, font_encoder)

        # Save results to JSON in simple format
        out_path = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".json"))
        
        # Clean format - only required fields
        clean_outline = []
        for item in outline:
            clean_item = {
                "level": item["level"],
                "page": item["page"]
            }
            # Use either 'heading' or 'text' field for the content
            if "heading" in item:
                clean_item["text"] = item["heading"]
            else:
                clean_item["text"] = item["text"]
            clean_outline.append(clean_item)
        
        result = {
            "title": title,
            "outline": clean_outline
        }
        
        with open(out_path, "w", encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"✅ Results saved to: {filename.replace('.pdf', '.json')}")
    
    print(f"🎉 Processing complete! {len(pdf_files)} file(s) processed.")

if __name__ == "__main__":
    main()
