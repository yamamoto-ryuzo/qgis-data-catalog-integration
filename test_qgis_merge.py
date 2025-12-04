#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
マージ機能とQGIS追加の動作確認テスト

統合されたXMLファイルがQGISプロジェクトに正しく追加されるかテストします。
"""

import os
import sys

def create_simple_merge_test():
    """シンプルなマージテスト用XMLファイルを作成"""
    
    test_dir = "test_qgis_merge"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    # 同じタイプの2つのファイル（建設工事関連XML）
    construction_xml1 = """<?xml version="1.0" encoding="UTF-8"?>
<CONSTRUCTION_PROJECT>
    <PROJECT_INFO>
        <PROJECT_NAME>道路舗装工事A</PROJECT_NAME>
        <CONTRACTOR>○○建設株式会社</CONTRACTOR>
        <START_DATE>2023-04-01</START_DATE>
    </PROJECT_INFO>
    <WORK_RECORD>
        <WORK_DATE>2023-04-15</WORK_DATE>
        <WORK_TYPE>路盤工</WORK_TYPE>
        <PROGRESS_RATE>25.5</PROGRESS_RATE>
    </WORK_RECORD>
    <WORK_RECORD>
        <WORK_DATE>2023-04-20</WORK_DATE>
        <WORK_TYPE>舗装工</WORK_TYPE>
        <PROGRESS_RATE>45.0</PROGRESS_RATE>
    </WORK_RECORD>
</CONSTRUCTION_PROJECT>"""

    construction_xml2 = """<?xml version="1.0" encoding="UTF-8"?>
<CONSTRUCTION_PROJECT>
    <PROJECT_INFO>
        <PROJECT_NAME>道路舗装工事B</PROJECT_NAME>
        <CONTRACTOR>△△建設株式会社</CONTRACTOR>
        <START_DATE>2023-05-01</START_DATE>
    </PROJECT_INFO>
    <WORK_RECORD>
        <WORK_DATE>2023-05-10</WORK_DATE>
        <WORK_TYPE>掘削工</WORK_TYPE>
        <PROGRESS_RATE>30.0</PROGRESS_RATE>
    </WORK_RECORD>
    <WORK_RECORD>
        <WORK_DATE>2023-05-15</WORK_DATE>
        <WORK_TYPE>路盤工</WORK_TYPE>
        <PROGRESS_RATE>55.0</PROGRESS_RATE>
    </WORK_RECORD>
</CONSTRUCTION_PROJECT>"""

    # 異なるタイプのファイル（施設管理XML）
    facility_xml = """<?xml version="1.0" encoding="UTF-8"?>
<FACILITY_MANAGEMENT>
    <FACILITY_INFO>
        <FACILITY_ID>BR-002</FACILITY_ID>
        <FACILITY_NAME>○○大橋</FACILITY_NAME>
        <FACILITY_TYPE>橋梁</FACILITY_TYPE>
        <CONSTRUCTION_YEAR>1990</CONSTRUCTION_YEAR>
    </FACILITY_INFO>
    <INSPECTION_RECORD>
        <INSPECTION_DATE>2023-06-01</INSPECTION_DATE>
        <CONDITION_RATING>1</CONDITION_RATING>
        <REMARKS>良好</REMARKS>
    </INSPECTION_RECORD>
</FACILITY_MANAGEMENT>"""

    # ファイルを作成
    with open(os.path.join(test_dir, "construction_A.xml"), "w", encoding="utf-8") as f:
        f.write(construction_xml1)
    
    with open(os.path.join(test_dir, "construction_B.xml"), "w", encoding="utf-8") as f:
        f.write(construction_xml2)
    
    with open(os.path.join(test_dir, "facility_mgmt.xml"), "w", encoding="utf-8") as f:
        f.write(facility_xml)
    
    print(f"QGISマージテスト用XMLファイルを作成しました: {test_dir}")
    print("作成されたファイル:")
    print("  - construction_A.xml (建設工事関連XML)")
    print("  - construction_B.xml (建設工事関連XML)")
    print("  - facility_mgmt.xml (施設管理XML)")
    
    return test_dir

if __name__ == "__main__":
    create_simple_merge_test()
    print("\n🎯 QGISマージ機能テスト:")
    print("1. QGISでGeo Importプラグインを開いてください")
    print("2. 'test_qgis_merge'フォルダを選択してください")
    print("3. データをロードしてください")
    print("4. ✅ 期待される結果:")
    print("   - '🏗️ 建設工事関連XML (統合 2ファイル)' レイヤがQGISに追加される")
    print("   - レイヤには4つのレコード（2ファイル×2レコード）が含まれる")
    print("   - 各レコードに'source_file'フィールドで元ファイル名が記録される")
    print("   - 'XML_Attributes_facility_mgmt' レイヤが個別に追加される（元のファイル名ベース）")
    print("5. 🔍 QGISのレイヤパネルで統合レイヤが表示されることを確認してください")
    print("6. 🔍 属性テーブルを開いて'source_file'フィールドを確認してください")