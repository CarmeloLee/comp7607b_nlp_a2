def delete_lines(source, target, lines_to_delete):
    """
    安全删除指定行（处理编码问题）
    """
    deleted = 0
    with open(source, 'rb') as fin, open(target, 'wb') as fout:
        for line_num, line in enumerate(fin, 1):
            try:
                # 尝试UTF-8解码
                decoded_line = line.decode('utf-8')

                # 验证是否为有效JSON（可选）
                # json.loads(decoded_line)  # 如果需严格验证可取消注释

                # 检查是否需要删除
                if line_num not in lines_to_delete:
                    fout.write(line)
                else:
                    print(f"已删除行 {line_num}")
                    deleted += 1
            except UnicodeDecodeError:
                # 处理编码异常行：保留原始字节
                if line_num not in lines_to_delete:
                    fout.write(line)
                else:
                    print(f"删除异常编码行 {line_num}")
                    deleted += 1
            except Exception as e:
                print(f"行 {line_num} 未知错误已保留: {str(e)}")
                fout.write(line)

    print(f"总删除行数: {deleted} (预期 {len(lines_to_delete)})")


# 使用示例
delete_lines(
    source="sft.jsonl",
    target="sft_cleaned.jsonl",
    lines_to_delete={136621, 136622}  # 使用集合提升查询效率
)