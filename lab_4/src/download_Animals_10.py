import os
import random
from collections import defaultdict
from datasets import load_dataset

# Load dataset split
print("Loading dataset...")
dataset = load_dataset("Rapidata/Animals-10", split="train")

# Map class indices to string labels
label_names = dataset.features["label"].names

# Group dataset indices by species label
species_indices = defaultdict(list)
for idx, item in enumerate(dataset):
    label_idx = item["label"]  # type: ignore
    species_name = label_names[label_idx]
    species_indices[species_name].append(idx)

# Download and save 10 random images per species, all in one folder
base_dir = "lab_4/assets/Animals-10/original"
os.makedirs(base_dir, exist_ok=True)
print("Starting to download random images for each species...")

for species_name, indices in species_indices.items():
    # Sample up to 10 unique indices randomly
    num_samples = min(10, len(indices))
    random_indices = random.sample(indices, k=num_samples)

    print(f"Saving {num_samples} images for species: '{species_name}'")

    for count, idx in enumerate(random_indices, start=1):
        img = dataset[idx]["image"]
        image_path = os.path.join(base_dir, f"{species_name}_{count}.png")
        img.save(image_path)

print("All done! Check your 'lab_4/assets/Animals-10/original' folder.")
