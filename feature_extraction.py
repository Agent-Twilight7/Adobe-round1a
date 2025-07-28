# extract_features_all.py
import pdfplumber
import pandas as pd
from collections import Counter

# Step 1: Analyze font size frequencies across all training PDFs
font_counter = Counter()

for i in range(1, 6):
    with pdfplumber.open(f"training_doc_{i}.pdf") as pdf:
        for page in pdf.pages:
            words = page.extract_words(extra_attrs=["size"])
            for word in words:
                size = round(float(word["size"]))
                font_counter[size] += 1

# Step 2: Build dynamic label_map
most_common = sorted(font_counter, reverse=True)  # Largest font = highest heading
label_map = {}

if len(most_common) >= 5:
    label_map[most_common[0]] = "Title"
    label_map[most_common[1]] = "H1"
    label_map[most_common[2]] = "H2"
    label_map[most_common[3]] = "H3"
    for size in most_common[4:]:
        label_map[size] = "Body"
else:
    print("⚠️ Not enough distinct font sizes for dynamic mapping. Using fallback labels.")

print("📏 Final Label Map:", label_map)

# Step 3: Extract features + assign labels
def extract_features(pdf_path):
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            words = page.extract_words(extra_attrs=["size", "fontname"])
            for word in words:
                text = word["text"]
                size = round(float(word["size"]))
                fontname = word.get("fontname", "")
                label = label_map.get(size, "Body")  # Default fallback
                rows.append({
                    "text": text,
                    "size": size,
                    "fontname": fontname,
                    "page": page_num,
                    "label": label
                })
    return rows

# Step 4: Run on all training documents
all_rows = []
for i in range(1, 6):
    print(f"🔍 Extracting from training_doc_{i}.pdf...")
    rows = extract_features(f"training_doc_{i}.pdf")
    all_rows.extend(rows)

# Step 5: Save to CSV
df = pd.DataFrame(all_rows)
df.to_csv("heading_training_data.csv", index=False)
print("✅ Saved labeled training data to heading_training_data.csv")


