import json
import re
import sys
import gc


def clean_s_tags(input_path, output_path):
    """仅移除<s>标签的纯净版"""
    s_tag_pattern = re.compile(r'</?s>')

    with open(input_path, 'r', encoding='utf-8') as fin, \
            open(output_path, 'w', encoding='utf-8') as fout:

        for line_num, line in enumerate(fin, 1):
            try:
                data = json.loads(line)
                if 'text' in data:
                    data['text'] = s_tag_pattern.sub('', data['text'])
                fout.write(json.dumps(data, ensure_ascii=False) + '\n')
            except Exception as e:
                print(f"行 {line_num} 错误: {str(e)}", file=sys.stderr)


def test_cleaner():
    """更新后的测试用例"""
    test_cases = [
        ('<s>测试内容</s>', '测试内容'),
        ('混合<s>标签</s>和内容', '混合标签和内容'),
        ('<s>嵌套</s><s>多标签</s>', '嵌套多标签'),
        ('无<s>闭合标签', '无闭合标签'),
        ('</s>闭合在前', '闭合在前'),
        ('正常内容', '正常内容')
    ]

    for original, expected in test_cases:
        cleaned = re.sub(r'</?s>', '', original)
        assert cleaned == expected, f"测试失败: {original} → {cleaned}"
    print("✅ 所有测试通过！")


if __name__ == "__main__":
    test_cleaner()
    clean_s_tags('pretrain_hp_1gb_traditional.jsonl', 'zh_coarse.jsonl')