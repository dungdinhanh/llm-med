#!/bin/bash

basefolder="./"
current="./"
cache=$PWD
threshold="50"

cmd="mkdir ${basefolder}"
echo ${cmd}
eval ${cmd}



# cd $PWD
cd ${cache}

cmd="python llava/data/download_images_processing.py --input_path ${basefolder}/data/matched_urls.jsonl --pmc_output_path ${basefolder}/data/pmc_articles/ --images_output_path ${basefolder}/data/images --threshold ${threshold}"
 echo ${cmd}
 eval ${cmd}