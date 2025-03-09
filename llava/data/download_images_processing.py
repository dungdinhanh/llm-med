import os
import json
import shutil
from tqdm import tqdm
import tarfile
import argparse
from urllib.error import HTTPError
import urllib.request

def main(args):
    input_data = []
    with open(args.input_path) as f:
        for line in f:
            input_data.append(json.loads(line))
    input_data = input_data[:args.threshold]
    
    # Process each PMC article
    for sample in tqdm(input_data, desc="Processing articles"):
        tar_path = os.path.join(args.pmc_output_path, os.path.basename(sample['pmc_tar_url']))
        
        # Download tar file
        try:
            print(f"Downloading: {sample['pmc_tar_url']}")
            urllib.request.urlretrieve(sample['pmc_tar_url'], tar_path)
        except HTTPError:
            print(f"Error downloading: {sample['pmc_tar_url']}")
            continue
        
        # Extract tar file
        try:
            with tarfile.open(tar_path, "r:gz") as tar:
                tar.extractall(args.pmc_output_path)
        except tarfile.TarError:
            print(f"Error extracting: {tar_path}")
            continue
        
        # Remove all other images except the required one
        extracted_folder = os.path.join(args.pmc_output_path, os.path.dirname(sample['image_file_path']))
        image_path = os.path.join(args.pmc_output_path, sample['image_file_path'])
        
        for root, dirs, files in os.walk(extracted_folder):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path != image_path:
                    os.remove(file_path)  # Remove unwanted images
        
        # Copy required image to destination
        if os.path.exists(image_path):
            dst = os.path.join(args.images_output_path, sample['pair_id'] + '.jpg')
            shutil.copyfile(image_path, dst)
        else:
            print(f"Image not found: {image_path}")
        
        # Remove the tar file after processing
        os.remove(tar_path)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, default='data/llava_med_image_urls.jsonl')
    parser.add_argument('--pmc_output_path', type=str, default='data/pmc_articles/')
    parser.add_argument('--images_output_path', type=str, default='data/images/')
    parser.add_argument('--threshold', default=20000, type=int, help="threshold for cutting the download")
    args = parser.parse_args()
    main(args)
