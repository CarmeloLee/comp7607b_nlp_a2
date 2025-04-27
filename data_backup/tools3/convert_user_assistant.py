import json
from tqdm import tqdm


def convert_even_rows(input_path, output_path):
    """
    将偶数行的用户/助理角色对调（中->英）

    参数：
        input_path: 输入文件路径（已转换的SFT格式）
        output_path: 输出文件路径
    """
    success = 0
    errors = 0

    with open(input_path, 'r', encoding='utf-8') as fin, \
            open(output_path, 'w', encoding='utf-8') as fout:

        # 获取总行数用于进度条
        total_lines = sum(1 for _ in fin)
        fin.seek(0)

        # 带行号的迭代
        for line_num, line in tqdm(enumerate(fin, 1), total=total_lines, desc="处理进度"):
            try:
                data = json.loads(line.strip())

                # 检查必要字段
                if len(data["conversations"]) != 2:
                    raise ValueError("对话轮次不等于2")

                user_content = data["conversations"][0]["content"]
                assistant_content = data["conversations"][1]["content"]

                # 处理偶数行（行号从1开始）
                if line_num % 2 == 0:
                    new_data = {
                        "conversations": [
                            {"role": "user", "content": assistant_content},
                            {"role": "assistant", "content": user_content}
                        ]
                    }
                else:
                    new_data = data  # 奇数行保持原样

                fout.write(json.dumps(new_data, ensure_ascii=False) + '\n')
                success += 1

            except (KeyError, json.JSONDecodeError, ValueError) as e:
                errors += 1
                # print(f"行 {line_num} 错误: {str(e)}")  # 调试用
                continue

    # 输出统计
    print(f"\n处理完成：")
    print(f"总行数：{total_lines}")
    print(f"成功处理：{success} ({success / total_lines:.1%})")
    print(f"错误行数：{errors} ({errors / total_lines:.1%})")


# 使用示例
convert_even_rows(
    input_path="FT-en-zh.jsonl",
    output_path="lora_mixed_translation.jsonl"
)