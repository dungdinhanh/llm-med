import json
import random
import argparse
import os

def load_instruct_data(file_path):
    """Load and shuffle instruction data."""
    with open(file_path, "r", encoding="utf-8") as f:
        instruct_data = json.load(f)
    random.shuffle(instruct_data)
    return instruct_data

def load_image_url_data(file_path):
    """Load image URL data from JSONL format."""
    image_url_dict = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            image_data = json.loads(line.strip())
            image_url_dict[image_data["pair_id"]] = image_data
    return image_url_dict

def match_data(instruct_data, image_url_dict, limit=20000):
    """Match instruction IDs with image URLs."""
    matched_data = []
    instruct_custom_selected = []
    count = 0

    for entry in instruct_data:
        image_id = entry["id"]
        if image_id in image_url_dict:
            matched_data.append(image_url_dict[image_id])
            instruct_custom_selected.append(entry)
            count += 1
            if count >= limit:
                break
        else:
            print("Image ID not found in image URL dictionary:", image_id)
    
    return matched_data, instruct_custom_selected

def save_results(matched_data, instruct_custom_selected, output_instruct, output_urls):
    """Save matched results to specified output paths."""
    os.makedirs(os.path.dirname(output_instruct), exist_ok=True)
    os.makedirs(os.path.dirname(output_urls), exist_ok=True)
    
    with open(output_urls, "w", encoding="utf-8") as f:
        for entry in matched_data:
            f.write(json.dumps(entry) + "\n")

    with open(output_instruct, "w", encoding="utf-8") as f:
        json.dump(instruct_custom_selected, f, indent=4)

    print("Matching complete! Results saved in:")
    print(f"- {output_instruct}")
    print(f"- {output_urls}")

def main():
    parser = argparse.ArgumentParser(description="Match instruction data with image URLs.")
    parser.add_argument("--input_instruct", type=str, help="Path to the input instruction JSON file.", default="data/instruct/llava_med_instruct_60k_inline_mention.json")
    parser.add_argument("--input_urls", type=str, help="Path to the input image URLs JSONL file.", default="data/llava_med_image_urls.jsonl")
    parser.add_argument("--output_instruct", type=str, help="Path to the output instruction JSON file.", default="data/instruct/matched_instruct.json")
    parser.add_argument("--output_urls", type=str, help="Path to the output matched image URLs JSONL file.", default="data/matched_urls.jsonl")
    
    args = parser.parse_args()
    
    instruct_data = load_instruct_data(args.input_instruct)
    image_url_dict = load_image_url_data(args.input_urls)
    matched_data, instruct_custom_selected = match_data(instruct_data, image_url_dict)
    save_results(matched_data, instruct_custom_selected, args.output_instruct, args.output_urls)

if __name__ == "__main__":
    main()


# import json
# import random

# # Load the instruction file (list of dictionaries)
# with open("data/instruct/llava_med_instruct_60k_inline_mention.json", "r", encoding="utf-8") as f:
#     instruct_data = json.load(f)
# random.shuffle(instruct_data)  # Shuffle the data

# # Load the image URLs file (JSONL format) into a dictionary
# image_url_dict = {}
# with open("data/llava_med_image_urls.jsonl", "r", encoding="utf-8") as f:
#     for line in f:
#         image_data = json.loads(line.strip())  # Read each line as JSON
#         image_url_dict[image_data["pair_id"]] = image_data

# # Match IDs from instruct data to image URL dictionary
# matched_data = []
# instruct_custom_selected = []
# count = 0

# for entry in instruct_data:
#     image_id = entry["id"]
#     if image_id in image_url_dict:
#         matched_data.append(image_url_dict[image_id])
#         instruct_custom_selected.append(entry)
#         count += 1
#         if count >= 20000:
#             break
#     else:
#         print("Image ID not found in image URL dictionary:", image_id)
        

# # Save matched results
# with open("data/matched_results.json", "w", encoding="utf-8") as f:
#     # json.dump(matched_data, f, indent=4)
#     for entry in matched_data:
#         f.write(json.dumps(entry) + "\n")

# with open("data/matched_instruct.json", "w", encoding="utf-8") as f:
#     json.dump(instruct_custom_selected, f, indent=4)

# print("Matching complete! Results saved in matched_results.json")