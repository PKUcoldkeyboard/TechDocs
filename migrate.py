import os
import sys
import re

def modify_md_files(directory):
    # 获取目录下的所有md文件
    md_files = [
        "SUMMARY.md",
        "README.md",
        "preface.md",
        "introduction.md",
        "ex0.md",
        "ex1.md",
        "ex2.md",
        "ex3.md",
        "ex4.md",
        "ex5.md",
        "ex6.md",
        "ex7.md",
        "ex8.md",
        "ex9.md",
        "ex10.md",
        "ex11.md",
        "ex12.md",
        "ex13.md",
        "ex14.md",
        "ex15.md",
        "ex16.md",
        "ex17.md",
        "ex18.md",
        "ex19.md",
        "ex20.md",
        "ex21.md",
        "ex22.md",
        "ex23.md",
        "ex24.md",
        "ex25.md",
        "ex26.md",
        "ex27.md",
        "ex28.md",
        "ex29.md",
        "ex30.md",
        "ex31.md",
        "ex32.md",
        "ex33.md",
        "ex34.md",
        "ex35.md",
        "ex36.md",
        "ex37.md",
        "ex38.md",
        "ex39.md",
        "ex40.md",
        "ex41.md",
        "ex42.md",
        "ex43.md",
        "ex44.md",
        "ex45.md",
        "ex46.md",
        "ex47.md",
        "postscript.md",
        "donors.md"
    ]

    # 遍历处理每个md文件
    for index, md_file in enumerate(md_files):
        file_path = os.path.join(directory, md_file)

        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 获取title
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
        else:
            title = ""

        # 计算weight
        weight = 10 + index

        # 添加描述语言
        description = "---\nweight: {}\ndate: \"2023-09-15T02:21:15+00:00\"\ndraft: false\nauthor: \"cuterwrite\"\ntitle: \"{}\"\nicon: \"circle\"\ntoc: true\ndescription: \"\"\npublishdate: \"2023-09-15T02:21:15+00:00\"\n---\n\n".format(weight, title)
        modified_content = description + content

        # 删除大标题
        modified_content = re.sub(r'^# .+$', '', modified_content, flags=re.MULTILINE)

        # 写入修改后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("执行命令格式为：python migrate.py [目录文件地址]")
        sys.exit(1)

    directory = sys.argv[1]
    modify_md_files(directory)