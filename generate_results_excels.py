import glob
import os
import json
import pandas as pd
import csv
def collect_json_txt_data(json_folder, txt_folder, output_excel):
    rows = []

    for filename in os.listdir(json_folder):
        if filename.endswith(".json"):
            name_only = os.path.splitext(filename)[0]
            json_path = os.path.join(json_folder, filename)
            txt_path = os.path.join(txt_folder, f"{name_only}_response.txt")

            # 读取 JSON 中的 locn_geometry 字段
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                locn_geometry = data.get("locn_geometry", "")
            except Exception as e:
                print(f"Error reading JSON {filename}: {e}")
                locn_geometry = ""

            # 读取对应 TXT 内容
            if os.path.exists(txt_path):
                with open(txt_path, 'r', encoding='utf-8') as f:
                    txt_content = f.read().strip()
            else:
                txt_content = ""

            rows.append({
                "file": name_only,
                "locn_geometry": locn_geometry,
                "predictions": txt_content
            })

    # 保存为 Excel
    df = pd.DataFrame(rows)
    df.to_csv(output_excel, index=False, encoding='utf-8-sig')
    print(f"已保存到 {output_excel}")
if __name__ == "__main__":
    json_folder = "/data/zeping_data/map2loc/Img2Loc_Test_Data/Georeference/"
    txt_folder = "/data/zeping_data/map2loc/predictions/"
    output_excel = "/data/zeping_data/results.csv"

    collect_json_txt_data(json_folder, txt_folder, output_excel)
