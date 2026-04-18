import argparse
import os
import random
import shutil
from typing import List, Tuple

import yaml

from src.config import PROCESSED_DATA_DIR, RAW_DATA_DIR


def create_yolo_yaml(classes: List[str], output_folder: str):
    train_path = os.path.abspath(os.path.join(output_folder, 'images', 'train'))
    val_path = os.path.abspath(os.path.join(output_folder, 'images', 'val'))
    test_path = os.path.abspath(os.path.join(output_folder, 'images', 'test'))
    
    data = {
        'path': os.path.abspath(output_folder),
        'train': train_path,
        'val': val_path,
        'test': test_path,
        'nc': len(classes), 
        'names': classes
    }
    
    with open(os.path.join(output_folder, 'data.yaml'), 'w') as f:
        yaml.dump(data, f, sort_keys=False)

def create_dataset(input_folder: str, output_folder: str, split_ratios: Tuple[float, float, float] = (0.8, 0.1, 0.1)):
    classes_file = os.path.join(input_folder, 'classes.txt')
    images_folder = os.path.join(input_folder, 'images')
    labels_folder = os.path.join(input_folder, 'labels')
    
    if not (os.path.exists(classes_file) and os.path.exists(images_folder) and os.path.exists(labels_folder)):
        print(f"Error: Required files missing in {input_folder}")
        return
    
    with open(classes_file, 'r') as f:
        classes = [line.strip() for line in f.readlines() if line.strip()]
    
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tif')
    all_images = [f for f in os.listdir(images_folder) if f.lower().endswith(valid_extensions)]

    pairs = []
    for img_file in all_images:
        base_name = os.path.splitext(img_file)[0]
        label_file = base_name + '.txt'
        
        if os.path.exists(os.path.join(labels_folder, label_file)):
            pairs.append((img_file, label_file))
        else:
            print(f"Warning: Label missing for {img_file}")

    if not pairs:
        print("No matching image-label pairs found.")
        return

    if split_ratios[0] <= 0 or split_ratios[1] <= 0 or split_ratios[2] <= 0 or sum(split_ratios) != 1.0:
        print("Error: Split ratios must be positive and sum to 1.0")
        split_ratios = (0.8, 0.1, 0.1)
        print(f"Using default split ratios: {split_ratios}")

    random.shuffle(pairs)
    total_len = len(pairs)
    train_end = int(split_ratios[0] * total_len)
    val_end = int((split_ratios[0] + split_ratios[1]) * total_len)

    train_files = pairs[:train_end]     
    val_files = pairs[train_end:val_end] 
    test_files = pairs[val_end:]       

    print(f"Total: {total_len} | Train: {len(train_files)} | Val: {len(val_files)} | Test: {len(test_files)}")

    
    dirs = {
        'train_imgs': os.path.join(output_folder, 'images', 'train'),
        'train_lbls': os.path.join(output_folder, 'labels', 'train'),
        'val_imgs': os.path.join(output_folder, 'images', 'val'),
        'val_lbls': os.path.join(output_folder, 'labels', 'val'),
        'test_imgs': os.path.join(output_folder, 'images', 'test'),
        'test_lbls': os.path.join(output_folder, 'labels', 'test')
    }
    
    for d in dirs.values():
        os.makedirs(d, exist_ok=True)
    
    print(f"Copying {len(train_files)} training pairs...")
    for image, label in train_files:
        shutil.copy(os.path.join(images_folder, image), os.path.join(dirs['train_imgs'], image))
        shutil.copy(os.path.join(labels_folder, label), os.path.join(dirs['train_lbls'], label))
    
    print(f"Copying {len(val_files)} validation pairs...")
    for image, label in val_files:
        shutil.copy(os.path.join(images_folder, image), os.path.join(dirs['val_imgs'], image))
        shutil.copy(os.path.join(labels_folder, label), os.path.join(dirs['val_lbls'], label))
    
    print(f"Copying {len(test_files)} test pairs...")
    for image, label in test_files:
        shutil.copy(os.path.join(images_folder, image), os.path.join(dirs['test_imgs'], image))
        shutil.copy(os.path.join(labels_folder, label), os.path.join(dirs['test_lbls'], label))

    create_yolo_yaml(classes, output_folder)
    print(f"Done! Dataset created at: {output_folder}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YOLO dataset splitter and YAML generator for bottle sorting system")
    
    parser.add_argument("--val_size", type=float, default=0.1, help="Validation set size (as a fraction of the total dataset)")
    parser.add_argument("--test_size", type=float, default=0.1, help="Test set size (as a fraction of the total dataset)")

    args = parser.parse_args()

    input_folder_path = str(RAW_DATA_DIR)
    output_folder_path = str(PROCESSED_DATA_DIR)

    train_size = 1.0 - args.val_size - args.test_size
    test_size = args.test_size
    val_size = args.val_size

    create_dataset(input_folder_path, output_folder_path, split_ratios=(train_size, val_size, test_size))