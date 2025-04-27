import json
import random
from tqdm import tqdm
import jieba
import re


def detect_translation_direction(user_content):
    """智能检测翻译方向（英->中 或 中->英）"""
    # 通过字符类型判断
    en_char_ratio = sum(1 for c in user_content if ord(c) < 256) / len(user_content)
    return 'en2zh' if en_char_ratio > 0.7 else 'zh2en'


def truncate_translation(text, direction, min_ratio=0.3, max_ratio=0.7):
    """根据翻译方向智能截断"""
    # 中英不同的截断策略
    if direction == 'en2zh':
        # 中文截断逻辑（同之前）
        sentences = re.split(r'[。！？，；]', text)
        sentences = [s for s in sentences if s.strip()]
        if len(sentences) > 1:
            split_pos = random.randint(1, len(sentences) - 1)
            return ''.join(sentences[:split_pos]), text

        # 保底分词截断
        words = list(jieba.cut(text))
        split_pos = random.randint(int(len(words) * min_ratio), int(len(words) * max_ratio))
        return ''.join(words[:split_pos]), text

    else:  # zh2en
        # 英文截断逻辑
        sentences = re.split(r'[.!?,;]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        if len(sentences) > 1:
            split_pos = random.randint(1, len(sentences) - 1)
            return ' '.join(sentences[:split_pos]), text

        # 按单词截断
        words = text.split()
        split_pos = random.randint(int(len(words) * min_ratio), int(len(words) * max_ratio))
        return ' '.join(words[:split_pos]), text


def convert_lora_to_dpo_enhanced(input_path, output_path):
    """
    支持双向翻译的转换函数
    """
    stats = {'en2zh': 0, 'zh2en': 0, 'error': 0}

    with open(input_path, 'r', encoding='utf-8') as fin, \
            open(output_path, 'w', encoding='utf-8') as fout:

        for line in tqdm(fin, desc='Processing'):
            try:
                data = json.loads(line)
                conv = data["conversations"]

                # 验证对话结构
                if len(conv) != 2 or conv[0]["role"] != "user" or conv[1]["role"] != "assistant":
                    stats['error'] += 1
                    continue

                # 检测翻译方向
                user_text = conv[0]["content"]
                direction = detect_translation_direction(user_text)

                # 生成错误翻译
                good_translation = conv[1]["content"]
                bad_translation, _ = truncate_translation(good_translation, direction)

                # 构建用户指令
                if direction == 'en2zh':
                    instruction = f"Please translate the following sentence from English to Chinese: {user_text}"
                else:
                    instruction = f"请将以下中文句子翻译成英文：{user_text}"

                # 构建DPO数据
                dpo_item = {
                    "chosen": [
                        {"role": "user", "content": instruction},
                        {"role": "assistant", "content": good_translation}
                    ],
                    "rejected": [
                        {"role": "user", "content": instruction},
                        {"role": "assistant", "content": bad_translation}
                    ]
                }

                fout.write(json.dumps(dpo_item, ensure_ascii=False) + '\n')
                stats[direction] += 1

            except Exception as e:
                stats['error'] += 1

    print(f"转换完成！统计信息：")
    print(f"英译中样本: {stats['en2zh']}")
    print(f"中译英样本: {stats['zh2en']}")
    print(f"错误/无效样本: {stats['error']}")


# 使用示例
convert_lora_to_dpo_enhanced("lora2.jsonl", "dpo3.jsonl")