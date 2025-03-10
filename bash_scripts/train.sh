#!/bin/bash

# WinKawaks/vit-tiny-patch16-224

basefolder="/hdd/dungda/LM/"
export NCCL_P2P_DISABLE=1 
export NCCL_IB_DISABLE=1
export CUDA_VISIBLE_DEVICES=0,1,2,3
# hyper-parameters
GPUS=1
model_name_or_path=${basefolder}/checkpoints/llava-med-1b-pretrain/
output_dir=${basefolder}/checkpoints/llava-med-1b-train/
data_path=${basefolder}/data/instruct/matched_instruct_50.json
image_folder=${basefolder}/data/images 
vision_tower=openai/clip-vit-base-patch16 # microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224 
accumulation_steps=1
mm_vision_select_layer="-1"

############### Option 1 to run code with one single GPU ###############

# export CUDA_VISIBLE_DEVICES=0 
# python llava/train/train.py --model_name_or_path ${model_name_or_path} --data_path ${data_path} --image_folder ${image_folder} --tune_mm_mlp_adapter True --output_dir ${output_dir} --vision_tower ${vision_tower} --mm_vision_select_layer -2 --mm_use_im_start_end True --bf16 True --num_train_epochs 1 --per_device_train_batch_size 1 --per_device_eval_batch_size 1 --gradient_accumulation_steps ${accumulation_steps} --evaluation_strategy "no" --save_strategy "steps" --save_steps 1000 --save_total_limit 3 --learning_rate 2e-3 --weight_decay 0. --warmup_ratio 0.03 --lr_scheduler_type "cosine" --logging_steps 1 --tf32 True --model_max_length 1024 --lazy_preprocess True --gradient_checkpointing True --dataloader_num_workers 8 --report_to wandb

############### Option 2 to run code with multi-GPU ###############

cmd="torchrun --nnodes=1 --nproc_per_node=${GPUS} --master_port=25001 llava/train/train_mem.py --model_name_or_path ${model_name_or_path} \
--data_path ${data_path} --image_folder ${image_folder} --tune_mm_mlp_adapter True --output_dir ${output_dir} --vision_tower ${vision_tower} \
--mm_vision_select_layer ${mm_vision_select_layer} --mm_use_im_start_end True --bf16 True --num_train_epochs 10 --per_device_train_batch_size 1 \
--per_device_eval_batch_size 3 --gradient_accumulation_steps ${accumulation_steps} --evaluation_strategy "no" --save_strategy "steps"\
 --save_steps 1000 --save_total_limit 3 --learning_rate 2e-3 --weight_decay 0.0 --warmup_ratio 0.03 --lr_scheduler_type "cosine" --logging_steps 1 --tf32 True --model_max_length 1024 \
  --lazy_preprocess True --gradient_checkpointing True --dataloader_num_workers 8 --report_to none --cache_dir ${basefolder}/Llama-3.2-1B/.cache/ --tokenizer_1B True"
echo ${cmd}
eval ${cmd}
