import json
from opencc import OpenCC
from tqdm import tqdm


def convert_simplified_to_traditional(input_path, output_path):
    """
    将JSONL中的简体中文内容转换为繁体中文

    参数：
        input_path: 输入文件路径
        output_path: 输出文件路径
    """
    # 初始化转换器（简体->繁体）
    cc = OpenCC('s2t')

    # 统计信息
    total = 0
    converted = 0
    errors = 0

    with open(input_path, 'r', encoding='utf-8') as fin, \
            open(output_path, 'w', encoding='utf-8') as fout:

        # 获取总行数用于进度条
        total_lines = sum(1 for _ in fin)
        fin.seek(0)  # 重置文件指针

        for line in tqdm(fin, total=total_lines, desc="转换进度"):
            total += 1
            try:
                data = json.loads(line.strip())

                # 处理每条对话内容
                for conv in data["conversations"]:
                    original = conv["content"]

                    # 智能判断是否需要转换（混合内容处理）
                    if any('\u4e00' <= c <= '\u9fff' for c in original):
                        converted_text = cc.convert(original)

                        # 记录转换变化（仅当实际发生转换时更新）
                        if converted_text != original:
                            conv["content"] = converted_text
                            converted += 1

                # 写入处理后的数据
                fout.write(json.dumps(data, ensure_ascii=False) + '\n')

            except (KeyError, json.JSONDecodeError) as e:
                errors += 1
                # 可选：记录错误行到日志文件
                # with open("error.log", "a") as log:
                #     log.write(f"行 {total} 错误: {str(e)}\n")
                continue

    # 打印统计报告
    print(f"\n转换完成！")
    print(f"总处理行数: {total}")
    print(f"发生转换的内容块: {converted}")
    print(f"错误行数: {errors} ({errors / total:.2%})")


# 使用示例
convert_simplified_to_traditional(
    # input_path="test.jsonl",
    input_path="mixed_translation.jsonl",
    output_path="sft1.jsonl"
)