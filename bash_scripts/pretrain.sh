#!/bin/bash

# WinKawaks/vit-tiny-patch16-224
export NCCL_P2P_DISABLE=1 
export NCCL_IB_DISABLE=1


basefolder="/hdd/dungda/LM/"

cmd="torchrun --nnodes=1 --nproc_per_node=4 --master_port=25001 \
    llava/train/train_mem.py \
    --model_name_or_path meta-llama/Llama-3.2-1B \
    --data_path ${basefolder}/data/instruct/matched_instruct.json \
    --image_folder ${basefolder}/data/images \
    --vision_tower  openai/clip-vit-base-patch16 \
    --tune_mm_mlp_adapter True \
    --mm_vision_select_layer -2 \
    --mm_use_im_start_end \
    --bf16 True \
    --output_dir ${basefolder}/checkpoints/llava-med-1b-pretrain_20k_lr4e3/ \
    --num_train_epochs 1 \
    --per_device_train_batch_size 2 \
    --per_device_eval_batch_size 4 \
    --gradient_accumulation_steps 2 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 2400 \
    --save_total_limit 1 \
    --learning_rate 4e-3 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --tf32 True \
    --model_max_length 2048 \
    --gradient_checkpointing True \
    --lazy_preprocess True \
    --report_to none\
    --cache_dir ${basefolder}/Llama-3.2-1B/.cache/"
echo ${cmd}
eval ${cmd}
