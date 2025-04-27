import json
import re
import os
from tqdm import tqdm


def filter_short_text(input_path, output_path, min_words=15):
    """
    过滤JSONL文件中文本长度不足的条目

    参数：
        input_path: 输入文件路径
        output_path: 输出文件路径
        min_words: 最小单词数阈值（英文按空格分词，中文按字计数）
    """
    # 初始化统计器
    total = 0
    removed = 0
    kept = 0

    # 获取文件总行数（用于进度条）
    with open(input_path, 'r', encoding='utf-8') as f:
        total_lines = sum(1 for _ in f)

    with open(input_path, 'r', encoding='utf-8') as fin, \
            open(output_path, 'w', encoding='utf-8') as fout:

        # 创建进度条
        pbar = tqdm(total=total_lines, desc='处理进度', unit='行')

        for line in fin:
            total += 1
            data = json.loads(line)
            text = data.get('text', '')

            # 中英文兼容分词逻辑
            if re.search(r'[\u4e00-\u9fff]', text):  # 检测中文字符
                word_count = len(text.strip())
            else:
                word_count = len(text.strip().split())

            # 过滤条件
            if word_count >= min_words:
                fout.write(line)
                kept += 1
            else:
                removed += 1

            # 更新进度条
            pbar.update(1)
            pbar.set_postfix({'保留': kept, '移除': removed})

        pbar.close()

    # 打印统计信息
    print(f"\n处理完成：")
    print(f"总行数：{total}")
    print(f"保留行数：{kept} ({kept / total:.1%})")
    print(f"移除行数：{removed} ({removed / total:.1%})")


# 使用示例（过滤英文数据）
filter_short_text(
    input_path='en_all.jsonl',
    output_path='en_filtered.jsonl',
    min_words=35
)

# 可选：备份原始文件
# import shutil
#
# shutil.move('en.jsonl', 'en_backup.jsonl')
# shutil.move('en_filtered.jsonl', 'en.jsonl')