import json
import os
import random

def filter_and_sample_json(input_json_path, output_json_path, image_folder, max_dicts=10000):
    """
    Read a JSON file with a list of dicts, filter out dicts with non-existent image paths,
    shuffle the list, and save up to max_dicts entries to a new JSON file.
    
    Args:
        input_json_path (str): Path to the input JSON file
        output_json_path (str): Path to the output JSON file
        max_dicts (int): Maximum number of dictionaries to save (default: 10000)
    """
    # Check if input file exists
    if not os.path.exists(input_json_path):
        print(f"Error: Input file '{input_json_path}' does not exist")
        return

    try:
        # Read the JSON file
        with open(input_json_path, 'r') as f:
            data = json.load(f)
        
        # Ensure data is a list
        if not isinstance(data, list):
            print(f"Error: JSON content in '{input_json_path}' is not a list")
            return

        # Filter out dicts where image path doesn't exist
        filtered_data = []
        for item in data:
            if not isinstance(item, dict):
                print(f"Warning: Skipping non-dict item: {item}")
                continue
            # Assuming 'image' is the key for the image path; adjust if different
            image_path = os.path.join(image_folder, item.get('image'))
            if image_path is None:
                print(f"Warning: Skipping dict with missing 'image' key: {item}")
                continue
            if not os.path.exists(image_path):
                print(f"Warning: Skipping dict with non-existent image path: {image_path}")
                continue
            filtered_data.append(item)

        # Log the number of valid entries
        print(f"Found {len(filtered_data)} valid dictionaries with existing image paths")

        # Shuffle the filtered list
        random.shuffle(filtered_data)

        # Select up to max_dicts entries
        sampled_data = filtered_data[:min(max_dicts, len(filtered_data))]
        print(f"Saving {len(sampled_data)} dictionaries to '{output_json_path}'")

        # Write to the output JSON file
        with open(output_json_path, 'w') as f:
            json.dump(sampled_data, f, indent=4)

    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON from '{input_json_path}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
if __name__ == "__main__":
    input_file = "/hdd/dungda/LM/data/instruct/matched_instruct.json"  # Replace with your input JSON file path
    output_file = "/hdd/dungda/LM/data/instruct/matched_instruct_10k.json"  # Replace with your desired output JSON file path
    image_folder="/hdd/dungda/LM/data/images/"
    filter_and_sample_json(input_file, output_file, image_folder)