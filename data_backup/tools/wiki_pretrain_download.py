import os
import json
import math
from datasets import load_dataset
from tqdm import tqdm


def chunk_wiki_data(language='en', chunk_size_mb=100, output_dir="wiki_chunks"):
    """
    分块下载维基百科数据到指定大小的JSONL文件

    参数：
        language: 语言代码（如'en','zh'）
        chunk_size_mb: 每个文件的目标大小（MB）
        output_dir: 输出目录
    """
    # 初始化配置
    os.makedirs(output_dir, exist_ok=True)
    target_bytes = chunk_size_mb * 1024 ** 2
    file_counter = 1
    current_size = 0
    current_file = None

    # 加载数据集并获取分片信息
    dataset = load_dataset(
        "wikipedia",
        f"20220301.{language}",
        split="train",
        streaming=True,
        trust_remote_code=True
    )

    # 创建进度条
    pbar = tqdm(desc=f"Processing {language} data", unit='MB')

    def write_chunk(text):
        """写入数据并管理文件切换"""
        nonlocal current_size, file_counter, current_file
        text_size = len(text.encode('utf-8'))

        # 需要切换新文件的情况
        if current_file is None or (current_size + text_size) > target_bytes:
            if current_file:
                current_file.close()
                pbar.update(current_size // 1024 ** 2)
            current_file = open(
                os.path.join(output_dir, f"{language}_chunk_{file_counter:03d}.jsonl"),
                'w', encoding='utf-8'
            )
            current_size = 0
            file_counter += 1

        # 写入数据
        current_file.write(json.dumps({"text": text}, ensure_ascii=False) + '\n')
        current_size += text_size

    # 处理数据流
    try:
        for example in dataset:
            text = example["text"].strip()
            if not text:
                continue

            # 拆分长文本为段落
            paragraphs = [p for p in text.split('\n') if p]
            for para in paragraphs:
                write_chunk(para)

    finally:
        if current_file:
            current_file.close()
            pbar.update(current_size // 1024 ** 2)
    pbar.close()

    print(f"\n✅ {language} 数据已分割为 {file_counter - 1} 个文件，每个约 {chunk_size_mb}MB")


if __name__ == "__main__":
    # 示例：下载英文数据到10个100MB文件
    chunk_wiki_data(language='en', chunk_size_mb=100)