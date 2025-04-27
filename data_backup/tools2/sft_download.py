from datasets import load_dataset
import json
import uuid  # 生成唯一ID
from pathlib import Path
from tqdm import tqdm

# 设置保存路径
save_dir = Path("./opus100_data")
save_dir.mkdir(exist_ok=True)
jsonl_path = save_dir / "opus100-en-zh.jsonl"

# 流式加载数据集
dataset = load_dataset(
    "Helsinki-NLP/opus-100",
    "en-zh",
    split="train",
    streaming=True
)

# 分批写入（内存优化）
batch_size = 1000
current_batch = []

with open(jsonl_path, "w", encoding="utf-8") as f:
    # 添加进度条（OPUS-100 en-zh 实际有 1,000,000 条数据）
    progress_bar = tqdm(total=1_000_000, desc="转换进度", unit="行")

    for idx, example in enumerate(dataset):
        try:
            # 生成唯一ID（或使用行号）
            unique_id = str(uuid.uuid4())  # 或者使用 idx

            # 构建JSON记录
            record = {
                "id": unique_id,
                "text_en": example["translation"]["en"],
                "text_zh": example["translation"]["zh"],
                "metadata": {
                    "source": "OPUS-100",
                    "split": "train"
                }
            }

            current_batch.append(json.dumps(record, ensure_ascii=False))

            # 分批写入提高IO效率
            if len(current_batch) >= batch_size:
                f.write("\n".join(current_batch) + "\n")
                current_batch = []
                progress_bar.update(batch_size)

        except KeyError as e:
            print(f"\n跳过损坏数据（索引 {idx}），错误: {str(e)}")
            continue

    # 写入最后一批
    if current_batch:
        f.write("\n".join(current_batch))
        progress_bar.update(len(current_batch))

    progress_bar.close()

print(f"\n转换完成！文件已保存至: {jsonl_path}")