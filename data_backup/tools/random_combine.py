import random
import os


def shuffle_merge(zh_path, en_path, output_path, buffer_size=50000):
    """
    中英文JSONL随机混排合并

    参数：
        zh_path: 中文文件路径
        en_path: 英文文件路径
        output_path: 输出路径
        buffer_size: 内存缓冲区行数（默认5万行≈50MB）
    """
    # 初始化文件指针
    zh_file = open(zh_path, 'r', encoding='utf-8')
    en_file = open(en_path, 'r', encoding='utf-8')
    output_file = open(output_path, 'w', encoding='utf-8')

    # 初始化缓冲区
    buffer = []

    def fill_buffer():
        """填充缓冲区至指定大小"""
        while len(buffer) < buffer_size:
            # 随机选择读取哪个文件
            if random.random() < 0.5:
                line = zh_file.readline()
                if not line: continue  # 中文文件读完
            else:
                line = en_file.readline()
                if not line: continue  # 英文文件读完

            buffer.append(line)

            # 任一文件结束时提前返回
            if not line and (zh_file.closed or en_file.closed):
                return

    try:
        while True:
            # 填充缓冲区
            fill_buffer()

            if not buffer:
                break  # 全部数据读取完成

            # 打乱当前缓冲区
            random.shuffle(buffer)

            # 写入输出文件
            output_file.writelines(buffer)
            buffer.clear()

            # 检查文件状态
            if zh_file.closed and en_file.closed:
                break

            # 处理已读完的文件
            if zh_file.closed:
                buffer.extend(en_file.readlines())
                random.shuffle(buffer)
                output_file.writelines(buffer)
                break

            if en_file.closed:
                buffer.extend(zh_file.readlines())
                random.shuffle(buffer)
                output_file.writelines(buffer)
                break

    finally:
        zh_file.close()
        en_file.close()
        output_file.close()


if __name__ == "__main__":
    # 使用示例
    shuffle_merge(
        zh_path='zh.jsonl',
        en_path='en.jsonl',
        output_path='../pretrain.jsonl',
        buffer_size=10000  # 内存允许可增大至10万行
    )