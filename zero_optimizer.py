# encoding=utf-8

import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForSeq2Seq
from datasets import Dataset

MODEL_PATH = "/root/ds_math7b/"

# 循环100条伪造数据，每条都很短，确保跑得快
def get_dummy_dataset():
    data = [{"text": "Hello, world! " * 10} for _ in range(100)]
    return Dataset.from_list(data)

def main():
    # 加载Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # 数据预处理
    dataset = get_dummy_dataset()

    def process(examples):
        inputs = tokenizer(examples["text"], max_length=512, truncation=True, padding="max_length")
        inputs["labels"] = inputs["input_ids"]
        return inputs

    encoded_dataset = dataset.map(process, batched=True)

    # 加载模型 (这里不要调用.cuda()因为DeepSpeed会接管)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        dtype=torch.bfloat16,  # 4090支持bf16
        trust_remote_code=True,
        use_cache=False  # 训练时关掉cache
    )

    # 训练参数 (DeepSpeed的核心入口)
    training_args = TrainingArguments(
        output_dir="./output_demo",
        per_device_train_batch_size=1,  # 设置小一点方便观察
        gradient_accumulation_steps=1,
        num_train_epochs=1,
        learning_rate=2e-5,
        logging_steps=1,
        save_strategy="no",
        bf16=True,  # 开启bf16
        deepspeed=os.environ.get("DS_CONFIG"),  # 从环境变量中读取json路径
        gradient_checkpointing = True if os.environ.get("USE_GC") == "1" else False  # 读取环境变量USE_GC，如果有值则开启，否则关闭
    )

    # 开始训练
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=encoded_dataset,
        data_collator=DataCollatorForSeq2Seq(tokenizer=tokenizer)
    )

    print(">>> 开始训练...请观察显存变化！")
    trainer.train()

if __name__ == "__main__":
    main()



