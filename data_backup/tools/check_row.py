import json
import sys


def inspect_jsonl(file_path, start_line=1, end_line=5):
    """查看指定行范围的内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if i < start_line:
                continue
            if i > end_line:
                break

            try:
                data = json.loads(line)
                print(f"\n行号：{i}")
                print(json.dumps(data, indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                print(f"\n行号：{i} [无效JSON结构]")
                print(line.strip())


if __name__ == "__main__":
    inspect_jsonl("pretrain_hp_1gb.jsonl", start_line=55539, end_line=55540)