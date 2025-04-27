def extract_lines(source_path, target_path, start=1000, end=1100):
    """
    高效提取JSONL文件指定行范围

    :param source_path: 源文件路径
    :param target_path: 目标文件路径
    :param start: 起始行号（包含，从1开始计数）
    :param end: 结束行号（包含）
    """
    extracted = 0
    current_line = 0

    with open(source_path, 'r', encoding='utf-8') as src, \
            open(target_path, 'w', encoding='utf-8') as tgt:

        # 逐行流式处理
        for line in src:
            current_line += 1

            # 行号在目标区间时写入
            if start <= current_line <= end:
                tgt.write(line)
                extracted += 1

                # 每处理100行打印进度（可选）
                if extracted % 10 == 0:
                    print(f"\r已提取 {extracted} 行", end='')

            # 超过结束行时终止读取
            if current_line > end:
                break

    print(f"\n完成！共提取 {extracted} 行到 {target_path}")
    print(f"实际提取行号范围：{max(1, start)}-{min(current_line, end)}")


# 使用示例（提取1000-1100行）
extract_lines(
    source_path='sft1.jsonl',
    target_path='output_1000-1100.jsonl',
    start=1000,
    end=1100
)