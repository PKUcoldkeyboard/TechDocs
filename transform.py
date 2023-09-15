import toml
import yaml

def toml_to_yaml(toml_file, yaml_file):
    # 读取TOML文件
    with open(toml_file, 'r', encoding='utf-8') as f:
        toml_data = f.read()

    # 解析TOML数据
    parsed_data = toml.loads(toml_data)

    # 将解析后的数据转换为YAML格式
    yaml_data = yaml.dump(parsed_data)

    # 将YAML数据写入文件
    with open(yaml_file, 'w') as f:
        f.write(yaml_data)

    print(f"转换完成，结果保存在{yaml_file}中。")

toml_file = 'hugo.toml'
yaml_file = 'output.yaml'
toml_to_yaml(toml_file, yaml_file)