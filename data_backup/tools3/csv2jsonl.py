import csv
import json
import re
from html import unescape


def process_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
            open(output_file, 'w', encoding='utf-8') as outfile:

        reader = csv.reader(infile, delimiter=';', quotechar='"')

        for row in reader:
            if len(row) < 7:
                continue

            # 提取并处理中英文内容
            en_content = unescape(row[5]).strip()
            zh_content = unescape(row[6]).strip()

            # 分割句子并清洗
            en_sentences = [s.strip() for s in re.split(r' @ |\.@|\s@', en_content) if s.strip()]
            zh_sentences = [s.strip() for s in re.split(r' @ |\.@|\s@', zh_content) if s.strip()]

            # 对齐处理
            num_pairs = min(len(en_sentences), len(zh_sentences))

            for i in range(num_pairs):
                # 生成独立对话对象
                conversation = {
                    "conversations": [
                        {"role": "user", "content": en_sentences[i]},
                        {"role": "assistant", "content": zh_sentences[i]}
                    ]
                }
                outfile.write(json.dumps(conversation, ensure_ascii=False) + '\n')


# 使用示例
process_csv('FT-en-zh.csv', 'FT-en-zh.jsonl')