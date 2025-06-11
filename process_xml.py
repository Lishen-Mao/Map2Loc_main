import xml.etree.ElementTree as ET
import os

from torch.fx.experimental.unification.dispatch import namespace


def extract_bounding_box(xml_file_path):
    """
    从单个 XML 文件中提取 minLon, maxLon, maxLat, minLat。
    """
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # 查找边界框信息
        # XPath: metadata/idinfo/spdom/bounding
        bounding_element = root.find('.//spdom/bounding')

        if bounding_element is not None:
            min_lon_elem = bounding_element.find('westbc')
            max_lon_elem = bounding_element.find('eastbc')
            max_lat_elem = bounding_element.find('northbc')
            min_lat_elem = bounding_element.find('southbc')

            min_lon = min_lon_elem.text if min_lon_elem is not None else "N/A"
            max_lon = max_lon_elem.text if max_lon_elem is not None else "N/A"
            max_lat = max_lat_elem.text if max_lat_elem is not None else "N/A"
            min_lat = min_lat_elem.text if min_lat_elem is not None else "N/A"

            return (min_lon, max_lon, max_lat, min_lat)
        else:
            print(f"警告: 文件 '{os.path.basename(xml_file_path)}' 中未找到 <bounding> 元素。跳过此文件。")
            return None

    except ET.ParseError as e:
        print(f"错误: 解析文件 '{os.path.basename(xml_file_path)}' 时出错: {e}。跳过此文件。")
        return None
    except Exception as e:
        print(f"处理文件 '{os.path.basename(xml_file_path)}' 时发生未知错误: {e}。跳过此文件。")
        return None

def batch_extract_and_save_per_file(xml_directory, output_directory='.'):
    """
    批量处理指定目录下的所有 XML 文件，为每个文件提取边界框信息
    并保存到同名的 TXT 文件中。
    """

    if not os.path.isdir(xml_directory):
        print(f"错误: 目录 '{xml_directory}' 不存在或不是一个有效的目录。")
        return

    # 确保输出目录存在
    os.makedirs(output_directory, exist_ok=True)

    processed_count = 0
    print(f"正在扫描目录: {xml_directory}")

    # 遍历指定目录中的所有文件
    for filename in os.listdir(xml_directory):
        if filename.endswith('.xml'):
            full_xml_path = os.path.join(xml_directory, filename)
            print(f"正在处理文件: {filename}")

            coords = extract_bounding_box(full_xml_path)

            if coords:
                # 构建输出 TXT 文件的名称 (例如: Burlington_1951.xml -> Burlington_1951.txt)
                txt_filename = os.path.splitext(filename)[0] + '.txt'
                full_txt_path = os.path.join(output_directory, txt_filename)

                # 将提取的数据写入到对应的 TXT 文件
                with open(full_txt_path, 'w', encoding='utf-8') as f:
                    f.write(f"({coords[0]}, {coords[1]}, {coords[2]}, {coords[3]})")
                print(f"  -> 坐标已保存到: {txt_filename}")
                processed_count += 1
            else:
                print(f"  -> 未能从文件 '{filename}' 提取坐标。")

    if processed_count > 0:
        print(f"\n成功处理 {processed_count} 个 XML 文件，并生成了对应的 TXT 文件。")
        print(f"输出文件保存在目录: '{os.path.abspath(output_directory)}'")
    else:
        print("\n未找到任何 XML 文件或未能提取到任何有效的坐标信息。")

if __name__ == '__main__':

    # --- 配置部分 ---
    # 将这里的路径替换为你的 XML 文件所在的目录
    # 例如: 'C:/Users/YourUser/Documents/MyXMLs' 或 '/home/user/data/xml_files'
    xml_directory = '/data/mls_data/USGS_Map_Gallery/USGS_Histo_Maps_24000_Metadata'

    # 输出 TXT 文件的目录。
    # '.' 表示在运行脚本的当前目录下创建 TXT 文件。
    # 你也可以指定一个不同的目录，例如 'output_txts/'
    output_directory = '/data/zeping_data/map2loc/xml2txt/'

    # --- 运行脚本 ---
    batch_extract_and_save_per_file(xml_directory, output_directory)