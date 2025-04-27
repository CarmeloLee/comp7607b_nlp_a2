import json
from opencc import OpenCC
import re
import sys
import gc


def convert_text_with_tags(text, converter):
    """智能处理<s>标签的转换函数"""
    # 切分保留标签结构
    parts = re.split(r'(<s>.*?</s>)', text)
    converted = []

    for part in parts:
        if part.startswith('<s>'):
            # 仅转换标签内的内容
            content = part[3:-4]
            converted_content = converter.convert(content)
            converted.append(f'<s>{converted_content}</s>')
        else:
            # 转换非标签部分
            converted.append(converter.convert(part))

    return ''.join(converted)


def process_large_jsonl(input_path, output_path):
    cc = OpenCC('s2t')
    converted = 0

    with open(input_path, 'r', encoding='utf-8') as fin, \
            open(output_path, 'w', encoding='utf-8') as fout:

        for line in fin:
            try:
                data = json.loads(line)

                # 专注处理text字段
                if 'text' in data and isinstance(data['text'], str):
                    original_text = data['text']
                    # 带标签转换
                    data['text'] = convert_text_with_tags(original_text, cc)

                    # 转换验证
                    if data['text'] == original_text:
                        print(f"行{converted + 1} 未发生转换", file=sys.stderr)

                # 写入处理后的行
                fout.write(json.dumps(data, ensure_ascii=False) + '\n')
                converted += 1

                if converted % 1000 == 0:
                    gc.collect()
                    print(f"已处理 {converted} 行")

            except Exception as e:
                print(f"行{converted} 错误: {str(e)}", file=sys.stderr)

    print(f"转换完成，共处理 {converted} 行")


# 使用示例
process_large_jsonl('pretrain_hp_1gb.jsonl', 'pretrain_hp_1gb_traditional.jsonl')