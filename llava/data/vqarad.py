
import os
import json
from tqdm import tqdm
from datasets import load_dataset

#  Load VQA-RAD dataset
dataset = load_dataset("flaviagiammarino/vqa-rad")


#  Define base directory for images
base_folder = "/hdd/dungda/LM/data/VQA/"
image_folder = os.path.join(base_folder, "images")


#  Create folders if they don’t exist
os.makedirs(image_folder, exist_ok=True)

#  Function to classify medical image type
def get_domain(question):
    domains = {"chest_xray": False, "mri": False, "ct_scan": False, "histology": False, "gross": False}
    question_lower = question.lower()
    
    if "x-ray" in question_lower or "radiograph" in question_lower:
        domains["chest_xray"] = True
    elif "mri" in question_lower:
        domains["mri"] = True
    elif "ct" in question_lower or "computed tomography" in question_lower:
        domains["ct_scan"] = True
    elif "histology" in question_lower or "biopsy" in question_lower:
        domains["histology"] = True
    elif "gross" in question_lower or "specimen" in question_lower:
        domains["gross"] = True
    
    return domains

#  Function to determine answer type
def get_answer_type(question, answer):
    yes_no_words = {"yes", "no"}
    
    # Check if answer is a Yes/No response
    if answer.lower().strip() in yes_no_words:
        return "CLOSED"

    return "OPEN"

#  JSON storage
train_data = []
test_data = []

#  Process dataset (train & test splits)
for split in ["train", "test"]:
    json_list = train_data if split == "train" else test_data

    for idx, item in tqdm(enumerate(dataset[split]), total=len(dataset[split]), desc=f"Processing {split} set"):
        image = item["image"]  # PIL Image
        question = item["question"]
        answer = item["answer"]

        # Save Image
        image_filename = f"{split}_{idx}.jpg"
        image_path = os.path.join(image_folder, image_filename)
        image.save(image_path)

        #  Determine answer type
        answer_type = get_answer_type(question, answer)

        #  Format JSON entry
        json_entry = {
            "id": f"{split}_{idx}",
            "image": image_filename,
            "domain": get_domain(question),
            "answer_type": answer_type,
            "conversations": [
                {"from": "human", "value": f"{question}\n<image>"},
                {"from": "gpt", "value": answer}
            ]
        }

        #  Append to list
        json_list.append(json_entry)

#  Save to JSON files
train_json_path = os.path.join(base_folder, "train.json")
test_json_path = os.path.join(base_folder, "test.json")

with open(train_json_path, "w") as train_file:
    json.dump(train_data, train_file, indent=4)

with open(test_json_path, "w") as test_file:
    json.dump(test_data, test_file, indent=4)

print(f" Images saved in: {image_folder}")
print(f" Train JSON saved as: {train_json_path}")
print(f" Test JSON saved as: {test_json_path}")





# os.makedirs(image_folder, exist_ok=True)

# # ✅ Function to classify medical image type
# def get_domain(question):
#     domains = {"chest_xray": False, "mri": False, "ct_scan": False, "histology": False, "gross": False}
#     question_lower = question.lower()
    
#     if "x-ray" in question_lower or "radiograph" in question_lower:
#         domains["chest_xray"] = True
#     elif "mri" in question_lower:
#         domains["mri"] = True
#     elif "ct" in question_lower or "computed tomography" in question_lower:
#         domains["ct_scan"] = True
#     elif "histology" in question_lower or "biopsy" in question_lower:
#         domains["histology"] = True
#     elif "gross" in question_lower or "specimen" in question_lower:
#         domains["gross"] = True
    
#     return domains

# # ✅ JSON storage
# train_data = []
# test_data = []

# # ✅ Process dataset (train & test splits)
# for split in ["train", "test"]:
#     json_list = train_data if split == "train" else test_data

#     for idx, item in tqdm(enumerate(dataset[split]), total=len(dataset[split]), desc=f"Processing {split} set"):
#         image = item["image"]  # PIL Image
#         question = item["question"]
#         answer = item["answer"]

#         # ✅ Save Image
#         image_filename = f"{split}_{idx}.jpg"
#         image_path = os.path.join(image_folder, image_filename)
#         image.save(image_path)

#         # ✅ Format JSON entry
#         json_entry = {
#             "id": f"{split}_{idx}",
#             "image": image_filename,
#             "domain": get_domain(question),
#             "conversations": [
#                 {"from": "human", "value": f"{question}\n<image>"},
#                 {"from": "gpt", "value": answer}
#             ]
#         }

#         # ✅ Append to list
#         json_list.append(json_entry)

# # ✅ Save to JSON files
# train_json_path = os.path.join(base_folder, "train.json")
# test_json_path = os.path.join(base_folder, "test.json")

# with open(train_json_path, "w") as train_file:
#     json.dump(train_data, train_file, indent=4)

# with open(test_json_path, "w") as test_file:
#     json.dump(test_data, test_file, indent=4)

# print(f"✅ Images saved in: {image_folder}")
# print(f"✅ Train JSON saved as: {train_json_path}")
# print(f"✅ Test JSON saved as: {test_json_path}")