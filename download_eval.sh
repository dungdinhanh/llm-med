#!/bin/bash


basefolder="/hdd/dungda/LM"
current="./"
cache=$PWD


cmd="mkdir ${basefolder}"
echo ${cmd}
eval ${cmd}

cmd="python llava/data/match_data_eval.py --input_urls ${basefolder}/data/llava_med_image_urls.jsonl --input_instruct ${basefolder}/data/eval/llava_med_eval_qa50_qa.jsonl --output_urls ${basefolder}/data/matched_urls_eval.jsonl"
echo ${cmd}
eval ${cmd} 


cmd="python llava/data/download_images_eval.py --input_path ${basefolder}/data/matched_urls_eval.jsonl  --pmc_output_path ${basefolder}/data/pmc_articles_eval/ --images_output_path ${basefolder}/data/images_eval/ "
 echo ${cmd}
 eval ${cmd}

