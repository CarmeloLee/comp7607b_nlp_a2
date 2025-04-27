import pandas as pd
import json
import random

# 读取Excel文件
df = pd.read_excel('lora_dataset.xlsx', sheet_name='body', header=None)  # 假设没有表头

# 转换为对话格式
conversations = []
for _, row in df.iterrows():
    english = row[0].strip()  # 第一列英文
    chinese = row[1].strip()  # 第二列中文

    conv = {
        "conversations": [
            {
                "role": "user",
                "content": english
            },
            {
                "role": "assistant",
                "content": chinese
            }
        ]
    }
    conversations.append(conv)

# 随机打乱顺序
random.shuffle(conversations)

# 保存为jsonl文件
with open('lora2_translation.jsonl', 'w', encoding='utf-8') as f:
    for item in conversations:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

print(f"转换完成，共处理{len(conversations)}条数据")