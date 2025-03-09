from lxml import etree
import os
import requests
import tarfile
import os
import json
import argparse
import glob


# output_dir = "pmc_extracted"
# os.makedirs(output_dir, exist_ok=True)

# for entry in data[:5]:  # Limit to 5 for testing
#     url = entry["pmc_tar_url"]
#     tar_path = os.path.join(output_dir, os.path.basename(url))
    
#     # Download
#     print(f"Downloading {url}")
#     response = requests.get(url, stream=True)
#     with open(tar_path, "wb") as f:
#         f.write(response.content)
    
#     # Extract
#     with tarfile.open(tar_path, "r:gz") as tar:
#         tar.extractall(os.path.join(output_dir, entry["pair_id"]))
#     os.remove(tar_path)  # Clean up tar file

def get_caption(xml_path, image_file, ns = {'xlink': 'http://www.w3.org/1999/xlink'}):
    if not os.path.exists(xml_path):
        print(xml_path)
        print(image_file)
        print("error")
        return None
    
    
    tree = etree.parse(xml_path)
    for fig in tree.xpath("//fig"):
        graphic = fig.xpath(".//graphic/@xlink:href", namespaces=ns)
        if graphic and graphic[0] in image_file:
            caption = fig.xpath(".//caption//text()")
            return " ".join(caption).strip()
    return None

def get_xml_path(image_path):
    image_dir = os.path.dirname(image_path)
    # image_name = os.path.basename(image_path).split(".")[0]
    # last_term = image_name.split("-")[-1]
    nxml_files = glob.glob(os.path.join(image_dir, "*.nxml"))
    if nxml_files:
        return nxml_files[0]
    else:
        print("no nxml file found")
        return None

def main(data, input_path_dir):
    pretrain_data = []
    ns = {'xlink': 'http://www.w3.org/1999/xlink'}
    pmc_path = os.path.join(input_path_dir, "pmc_articles")
    for entry in data:  # Test with 5
        pair_id = entry["pair_id"]
        image_path = os.path.join(pmc_path, entry["image_file_path"])
        xml_path = get_xml_path(image_path)

        # image_path = os.path.join(output_dir, pair_id, entry["image_file_path"])
        caption = get_caption(xml_path, image_path, ns) # Will need to process caption later
        if caption:
            pretrain_data.append({
                "image_path": image_path,
                "text": caption,
                "pair_id": pair_id
            })

    with open(os.path.join(input_path_dir, "pretrain_sample.jsonl"), "w") as f:
        for item in pretrain_data:
            f.write(json.dumps(item) + "\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, default='data/llava_med_image_urls100.jsonl')
    
    args  = parser.parse_args()
    input_path_dir = os.path.dirname(args.input_path)
    output_dir = input_path_dir
    jsonl_path = args.input_path
    with open(jsonl_path) as f:
        data = [json.loads(line) for line in f]
    main(data, input_path_dir)