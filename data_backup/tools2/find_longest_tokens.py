import json
import sys
from tqdm import tqdm


def find_longest_lines(file_path, length_mode='char'):
    """
    终极健壮版长行定位方案
    """
    max_length = 0
    max_line_num = 0
    max_content = ""
    error_lines = []

    # 第一阶段：二进制模式快速统计行数
    print("[阶段1] 正在快速扫描文件结构...")
    with open(file_path, 'rb') as f:
        total_lines = sum(1 for _ in f)

    # 第二阶段：带异常处理的详细扫描
    print("[阶段2] 正在分析内容...")
    with open(file_path, 'rb') as f:
        line_iterator = enumerate(f, 1)
        if total_lines > 1000:
            line_iterator = tqdm(line_iterator, total=total_lines, desc="处理进度")

        for line_num, line_bytes in line_iterator:
            try:
                # 动态编码检测和解码
                try:
                    line_str = line_bytes.decode('utf-8')
                except UnicodeDecodeError:
                    line_str = line_bytes.decode('utf-8', errors='replace')

                # JSON解析
                data = json.loads(line_str)

                # 长度计算
                current_length = 0
                for msg in data.get("conversations", []):
                    text = msg.get("content", "")
                    if length_mode == 'char':
                        current_length += len(text)
                    elif length_mode == 'word':
                        current_length += len(text.split())

                # 更新最大值
                if current_length > max_length:
                    max_length = current_length
                    max_line_num = line_num
                    max_content = line_str[:100] + "..."

            except Exception as e:
                error_lines.append((line_num, str(e)))
                continue

    # 输出报告
    print("\n" + "=" * 50)
    print(f"文件总行数: {total_lines}")
    print(f"成功处理行数: {total_lines - len(error_lines)}")
    print(f"错误行数: {len(error_lines)}")
    if error_lines:
        print("\n前10个错误行信息：")
        for err in error_lines[:10]:
            print(f"行号 {err[0]} → 错误类型：{err[1]}")
    print("\n最大长度统计：")
    print(f"所在行号: {max_line_num}")
    print(f"长度值({length_mode}): {max_length}")
    print(f"内容预览: {max_content}")


if __name__ == "__main__":
    find_longest_lines("../sft.jsonl", length_mode='char')