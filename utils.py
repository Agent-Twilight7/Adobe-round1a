import fitz  # PyMuPDF
from sklearn.preprocessing import LabelEncoder

def process_pdf(pdf_path, clf, label_encoder, font_encoder):
    """
    Process PDF to extract document structure using dynamic font size classification.
    Returns title and outline in simple format.
    """
    doc = fitz.open(pdf_path)
    
    # Extract all text with fonts and positions
    lines_with_features = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")
        
        for block in blocks["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if text:
                            lines_with_features.append({
                                "text": text,
                                "font_size": span["size"],
                                "font": span["font"],
                                "page": page_num + 1
                            })
    
    if not lines_with_features:
        doc.close()
        return "No Title", []
    
    # Sort by font size to identify hierarchy
    lines_with_features.sort(key=lambda x: x["font_size"], reverse=True)
    
    # Get unique font sizes and assign levels dynamically
    unique_sizes = sorted(list(set(item["font_size"] for item in lines_with_features)), reverse=True)
    
    # Create font size to level mapping
    size_to_level = {}
    if len(unique_sizes) == 1:
        size_to_level[unique_sizes[0]] = "Body"
    else:
        # Map largest to Title, then H1, H2, H3, rest to Body
        level_names = ["Title", "H1", "H2", "H3"]
        for i, size in enumerate(unique_sizes):
            if i < len(level_names):
                size_to_level[size] = level_names[i]
            else:
                size_to_level[size] = "Body"
    
    # Find title (largest font size, typically first occurrence)
    title = "Document"
    title_candidates = [item for item in lines_with_features if size_to_level[item["font_size"]] == "Title"]
    if title_candidates:
        title = title_candidates[0]["text"]
    
    # Build outline
    outline = []
    for item in lines_with_features:
        level = size_to_level[item["font_size"]]
        
        # Skip title in outline if it's the document title
        if level == "Title" and item["text"] == title:
            continue
            
        # Determine if this is a heading or body text
        is_heading = level in ["H1", "H2", "H3"]
        
        outline_item = {
            "page": item["page"],
            "level": level
        }
        
        if is_heading:
            outline_item["heading"] = item["text"]
        else:
            outline_item["text"] = item["text"]
            
        outline.append(outline_item)

    doc.close()
    
    return title, outline
