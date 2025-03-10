#!/bin/bash



basefolder="/hdd/dungda/LM/"
current="./"
cache=$PWD
threshold="20000"

cmd="mkdir ${basefolder}"
echo ${cmd}
eval ${cmd}

if [[ ${basefolder} != ${current} ]]; then
    rm -r ${basefolder}/data/

    cmd="cp -r data ${basefolder}/"
    echo ${cmd}
    eval ${cmd}
    fi






mkdir ${basefolder}/data/alignment

cd ${basefolder}/data/alignment

wget https://hanoverprod.z21.web.core.windows.net/med_llava/alignment/llava_med_alignment_500k.json

cd ..

mkdir instruct
cd instruct

wget https://hanoverprod.z21.web.core.windows.net/med_llava/instruct/llava_med_instruct_10k.json
wget https://hanoverprod.z21.web.core.windows.net/med_llava/instruct/llava_med_instruct_60k.json
wget https://hanoverprod.z21.web.core.windows.net/med_llava/instruct/llava_med_instruct_60k_inline_mention.json
wget https://hanoverprod.z21.web.core.windows.net/med_llava/instruct/llava_med_instruct_fig_captions.json
cd ..

mkdir eval
cd eval

wget https://hanoverprod.z21.web.core.windows.net/med_llava/eval/llava_med_eval_qa50_qa.jsonl
wget https://hanoverprod.z21.web.core.windows.net/med_llava/eval/llava_med_eval_qa50_fig_captions.json
wget https://hanoverprod.z21.web.core.windows.net/med_llava/eval/llava_med_qa50_instruct_caption_in_text_cleaned-60k-3epoch.json

cd ..

wget https://hanoverprod.z21.web.core.windows.net/med_llava/llava_med_image_urls.jsonl
mkdir pmc_articles
mkdir images

cd ..

pip install tqdm

cd $PWD
cd ${cache}

# match data with generated inline instruction with limit 20k

cmd="python llava/data/match_data.py --input_urls ${basefolder}/data/llava_med_image_urls.jsonl --input_instruct ${basefolder}/data/instruct/llava_med_instruct_60k_inline_mention.json --output_urls ${basefolder}/data/matched_urls.jsonl \
--output_instruct ${basefolder}/data/instruct/matched_instruct.json"
echo ${cmd}
eval ${cmd} 

# Only download matched data

cmd="python llava/data/download_images_processing.py --input_path ${basefolder}/data/matched_urls.jsonl --instruct_path ${basefolder}/data/instruct/matched_instruct.json --pmc_output_path ${basefolder}/data/pmc_articles/ --images_output_path ${basefolder}/data/images --threshold ${threshold}"
 echo ${cmd}
 eval ${cmd}

