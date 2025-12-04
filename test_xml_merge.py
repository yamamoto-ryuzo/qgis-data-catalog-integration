#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
XML file merging functionality test script

This script tests the XML file merging capabilities for MLIT XML files.
"""

import os
import sys
from xml.etree import ElementTree as ET

def create_test_xml_files():
    """テスト用のMLIT XMLファイルを作成"""
    
    # 河川水位データのサンプル
    river_xml = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ksj_app_schema SYSTEM "KS-META-13-v1_0.dtd">
<ksj_app_schema>
    <gml:featureMember>
        <ksj:W09 gml:id="W09_001">
            <ksj:POS>139.123456 35.654321</ksj:POS>
            <ksj:W09_001>01</ksj:W09_001>
            <ksj:W09_002>東京</ksj:W09_002>
            <ksj:W09_003>河川水位観測所A</ksj:W09_003>
            <ksj:W09_004>2.50</ksj:W09_004>
        </ksj:W09>
    </gml:featureMember>
    <gml:featureMember>
        <ksj:W09 gml:id="W09_002">
            <ksj:POS>139.234567 35.765432</ksj:POS>
            <ksj:W09_001>01</ksj:W09_001>
            <ksj:W09_002>東京</ksj:W09_002>
            <ksj:W09_003>河川水位観測所B</ksj:W09_003>
            <ksj:W09_004>1.80</ksj:W09_004>
        </ksj:W09>
    </gml:featureMember>
</ksj_app_schema>"""

    # 同じタイプの別の河川水位データ
    river_xml2 = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ksj_app_schema SYSTEM "KS-META-13-v1_0.dtd">
<ksj_app_schema>
    <gml:featureMember>
        <ksj:W09 gml:id="W09_003">
            <ksj:POS>139.345678 35.876543</ksj:POS>
            <ksj:W09_001>01</ksj:W09_001>
            <ksj:W09_002>東京</ksj:W09_002>
            <ksj:W09_003>河川水位観測所C</ksj:W09_003>
            <ksj:W09_004>3.20</ksj:W09_004>
        </ksj:W09>
    </gml:featureMember>
</ksj_app_schema>"""

    # 土地利用データのサンプル（異なるタイプ）
    landuse_xml = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ksj_app_schema SYSTEM "KS-META-09-v2_1.dtd">
<ksj_app_schema>
    <gml:featureMember>
        <ksj:L03-a gml:id="L03_001">
            <ksj:POS>139.123456 35.654321</ksj:POS>
            <ksj:L03_001>2020</ksj:L03_001>
            <ksj:L03_002>1101</ksj:L03_002>
            <ksj:L03_003>田</ksj:L03_003>
        </ksj:L03-a>
    </gml:featureMember>
</ksj_app_schema>"""

    # テストディレクトリを作成
    test_dir = "test_xml_merge"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    # XMLファイルを作成
    with open(os.path.join(test_dir, "river_data_1.xml"), "w", encoding="utf-8") as f:
        f.write(river_xml)
    
    with open(os.path.join(test_dir, "river_data_2.xml"), "w", encoding="utf-8") as f:
        f.write(river_xml2)
    
    with open(os.path.join(test_dir, "landuse_data.xml"), "w", encoding="utf-8") as f:
        f.write(landuse_xml)
    
    print(f"テスト用XMLファイルを作成しました: {test_dir}")
    print("- river_data_1.xml (河川水位データ)")
    print("- river_data_2.xml (河川水位データ)")
    print("- landuse_data.xml (土地利用データ)")
    
    return test_dir

if __name__ == "__main__":
    create_test_xml_files()
    print("\n🔄 XMLマージ機能のテスト:")
    print("1. QGISでGeo Importプラグインを開いてください")
    print("2. 'test_xml_merge'フォルダを選択してください")  
    print("3. データをロードしてください")
    print("4. ✅ 結果の確認:")
    print("   - 同じタイプのXMLファイル（river_data_1.xml、river_data_2.xml）が")
    print("     → '河川水位データ_統合_2ファイル' として自動マージされる")
    print("   - 異なるタイプのXMLファイル（landuse_data.xml）が")
    print("     → '土地利用データ' として個別処理される")
    print("   - 各レコードに 'source_file' フィールドが追加され、元ファイル名が記録される")
    print("5. ✅ マージ機能が自動実行されます（手動操作不要）")