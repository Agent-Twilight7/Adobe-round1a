import os
import pickle

def load_classifier():
    dir_path = os.path.dirname(__file__)

    with open(os.path.join(dir_path, "model.pkl"), "rb") as f:
        model = pickle.load(f)

    with open(os.path.join(dir_path, "label_encoder.pkl"), "rb") as f:
        label_encoder = pickle.load(f)

    with open(os.path.join(dir_path, "font_encoder.pkl"), "rb") as f:
        font_encoder = pickle.load(f)

    return model, label_encoder, font_encoder
