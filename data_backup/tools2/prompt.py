import json
from tqdm import tqdm


def add_translation_prompts(input_path, output_path):
    """
    为翻译数据集添加指令前缀

    参数：
        input_path: 输入文件路径
        output_path: 输出文件路径
    """
    # 统计信息
    total = 0
    modified = 0
    errors = 0

    with open(input_path, 'r', encoding='utf-8') as fin, \
            open(output_path, 'w', encoding='utf-8') as fout:

        # 先获取总行数用于进度条
        total_lines = sum(1 for _ in fin)
        fin.seek(0)  # 重置文件指针

        # 带行号的迭代处理
        for line_num, line in tqdm(enumerate(fin, 1), total=total_lines, desc="处理进度"):
            total += 1

            try:
                data = json.loads(line.strip())

                # 验证数据结构
                if len(data["conversations"]) != 2:
                    raise ValueError("无效的对话结构")

                user_content = data["conversations"][0]["content"]
                assistant_content = data["conversations"][1]["content"]

                # 根据行号添加提示词
                # if line_num % 2 == 1:  # 奇数行（英->中）
                #     new_user = f"Please translate the following sentence from English to Chinese: {user_content}"
                # else:  # 偶数行（中->英）
                #     new_user = f"请把以下句子从中文翻译成英文：{user_content}"
                if line_num % 10 == 1:  # 奇数行（英->中）
                    new_user = f"Please translate the following sentence from English to Chinese: {user_content}"
                elif line_num % 10 == 0:  # 偶数行（中->英）
                    new_user = f"请把以下句子从中文翻译成英文：{user_content}"
                else:  # 其他行（不添加提示词）
                    new_user = user_content

                # 更新对话内容
                data["conversations"][0]["content"] = new_user
                data["conversations"][1]["content"] = assistant_content  # 保持助理内容不变

                # 写入新数据
                fout.write(json.dumps(data, ensure_ascii=False) + '\n')
                modified += 1

            except (KeyError, json.JSONDecodeError, ValueError) as e:
                errors += 1
                # 打印错误信息（可选）
                # print(f"行 {line_num} 错误: {str(e)}")
                continue

    # 输出统计报告
    print(f"\n处理完成！")
    print(f"总处理行数: {total}")
    print(f"成功修改: {modified} ({modified / total:.1%})")
    print(f"错误行数: {errors} ({errors / total:.1%})")


# 使用示例
add_translation_prompts(
    input_path="test.jsonl",
    output_path="sft_prompt.jsonl"
)