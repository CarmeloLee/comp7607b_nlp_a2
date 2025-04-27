import json
from tqdm import tqdm


def convert_translation_dataset(input_path, output_path):
    """
    将OPUS-100格式转换为对话式SFT训练格式

    参数：
        input_path: 输入文件路径
        output_path: 输出文件路径
    """
    # 统计信息
    total = 0
    success = 0
    errors = 0

    with open(input_path, 'r', encoding='utf-8') as fin, \
            open(output_path, 'w', encoding='utf-8') as fout:

        # 添加进度条（假设每行约100字节估算总行数）
        total_lines = sum(1 for _ in fin)
        fin.seek(0)  # 重置文件指针

        for line in tqdm(fin, total=total_lines, desc="处理进度"):
            total += 1

            try:
                # 解析原始数据
                data = json.loads(line.strip())

                # 构建对话格式
                new_data = {
                    "conversations": [
                        {
                            "role": "user",
                            "content": data["text_en"]
                        },
                        {
                            "role": "assistant",
                            "content": data["text_zh"]
                        }
                    ]
                }

                # 写入新格式
                fout.write(json.dumps(new_data, ensure_ascii=False) + '\n')
                success += 1

            except (KeyError, json.JSONDecodeError) as e:
                errors += 1
                # 打印错误信息（可选）
                # print(f"行 {total} 错误: {str(e)}")
                continue

    # 打印统计报告
    print(f"\n转换完成！")
    print(f"总处理行数: {total}")
    print(f"成功转换: {success} ({success / total:.1%})")
    print(f"错误行数: {errors} ({errors / total:.1%})")


# 使用示例
convert_translation_dataset(
    input_path="opus100-en-zh.jsonl",
    output_path="translation_sft.jsonl"
)