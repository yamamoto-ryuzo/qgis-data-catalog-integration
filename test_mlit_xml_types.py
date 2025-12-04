#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
XMLタイプ別レイヤ名テスト用ファイル生成

各種XMLタイプに対応した絵文字付きレイヤ名のテスト用XMLファイルを作成します。
"""

import os
import sys

def create_mlit_test_xml_files():
    """MLIT XMLの各タイプに対応したテストファイルを作成"""
    
    # テストディレクトリを作成
    test_dir = "test_mlit_xml_types"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    # 1. 電子納品XML (CALS/EC準拠)
    electronic_delivery_xml = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE OFFICE-INDEX SYSTEM "OFFICE-INDEX_01.DTD">
<OFFICE-INDEX>
    <CONSTRUCTION_NAME>○○道路改良工事</CONSTRUCTION_NAME>
    <OFFICE_NAME>○○工事事務所</OFFICE_NAME>
    <WORK_DATA>
        <FOLDER_NAME>SURVEY</FOLDER_NAME>
        <FILE>
            <FILE_NAME>survey_data.pdf</FILE_NAME>
            <FILE_DATE>2023-03-15</FILE_DATE>
        </FILE>
    </WORK_DATA>
</OFFICE-INDEX>"""

    # 2. 測量成果XML (測量成果電子納品要領)
    survey_results_xml = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE SURVEY SYSTEM "SURVEY_03.DTD">
<SURVEY>
    <SURVEY_NAME>基準点測量</SURVEY_NAME>
    <SURVEY_DATE>2023-03-10</SURVEY_DATE>
    <POINT_DATA>
        <POINT_NO>BM-1</POINT_NO>
        <COORDINATE_X>123456.789</COORDINATE_X>
        <COORDINATE_Y>987654.321</COORDINATE_Y>
        <HEIGHT>12.345</HEIGHT>
    </POINT_DATA>
</SURVEY>"""

    # 3. JPGIS準拠地理空間情報XML
    jpgis_xml = """<?xml version="1.0" encoding="UTF-8"?>
<ksj_app_schema xmlns:gml="http://www.opengis.net/gml/3.2">
    <gml:featureMember>
        <ksj:AdministrativeBoundary gml:id="AB001">
            <ksj:administrativeAreaCode>13101</ksj:administrativeAreaCode>
            <ksj:administrativeAreaName>千代田区</ksj:administrativeAreaName>
            <ksj:geometry>
                <gml:Polygon>
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>139.7 35.7 139.8 35.7 139.8 35.8 139.7 35.8 139.7 35.7</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </ksj:geometry>
        </ksj:AdministrativeBoundary>
    </gml:featureMember>
</ksj_app_schema>"""

    # 4. CAD/SXF関連XML
    cad_sxf_xml = """<?xml version="1.0" encoding="UTF-8"?>
<SXF_DATA xmlns="http://www.jacic.or.jp/sxf">
    <HEADER>
        <FORMAT_VERSION>SXF3.0</FORMAT_VERSION>
        <DRAWING_NAME>構造図</DRAWING_NAME>
        <CREATE_DATE>2023-03-20</CREATE_DATE>
    </HEADER>
    <LAYER>
        <LAYER_NAME>構造物</LAYER_NAME>
        <FEATURE>
            <FEATURE_CODE>25110</FEATURE_CODE>
            <GEOMETRY_TYPE>LINE</GEOMETRY_TYPE>
            <COORDINATE_DATA>1000,2000 1500,2000</COORDINATE_DATA>
        </FEATURE>
    </LAYER>
</SXF_DATA>"""

    # 5. 積算システムXML (JACIC準拠)
    estimation_xml = """<?xml version="1.0" encoding="UTF-8"?>
<COST_ESTIMATION xmlns="http://www.jacic.or.jp/cost">
    <PROJECT_INFO>
        <PROJECT_NAME>橋梁工事</PROJECT_NAME>
        <ESTIMATION_DATE>2023-03-25</ESTIMATION_DATE>
    </PROJECT_INFO>
    <COST_ITEM>
        <ITEM_CODE>0101001</ITEM_CODE>
        <ITEM_NAME>掘削工</ITEM_NAME>
        <UNIT>m3</UNIT>
        <QUANTITY>150.00</QUANTITY>
        <UNIT_PRICE>1200</UNIT_PRICE>
        <AMOUNT>180000</AMOUNT>
    </COST_ITEM>
</COST_ESTIMATION>"""

    # 6. 施設管理XML
    facility_mgmt_xml = """<?xml version="1.0" encoding="UTF-8"?>
<FACILITY_MANAGEMENT>
    <FACILITY_INFO>
        <FACILITY_ID>BR-001</FACILITY_ID>
        <FACILITY_NAME>○○橋</FACILITY_NAME>
        <FACILITY_TYPE>橋梁</FACILITY_TYPE>
        <CONSTRUCTION_YEAR>1985</CONSTRUCTION_YEAR>
    </FACILITY_INFO>
    <INSPECTION_RECORD>
        <INSPECTION_DATE>2023-03-30</INSPECTION_DATE>
        <CONDITION_RATING>2</CONDITION_RATING>
        <REMARKS>軽微な損傷あり</REMARKS>
    </INSPECTION_RECORD>
</FACILITY_MANAGEMENT>"""

    # 7. 地理空間情報XML
    geography_xml = """<?xml version="1.0" encoding="UTF-8"?>
<GEOGRAPHIC_DATA xmlns:gml="http://www.opengis.net/gml">
    <LOCATION_INFO>
        <PLACE_NAME>東京駅</PLACE_NAME>
        <PREFECTURE>東京都</PREFECTURE>
        <CITY>千代田区</CITY>
        <gml:Point>
            <gml:pos>139.7673068 35.6809591</gml:pos>
        </gml:Point>
    </LOCATION_INFO>
</GEOGRAPHIC_DATA>"""

    # 8. 建設工事関連XML
    construction_xml = """<?xml version="1.0" encoding="UTF-8"?>
<CONSTRUCTION_PROJECT>
    <PROJECT_INFO>
        <PROJECT_NAME>道路舗装工事</PROJECT_NAME>
        <CONTRACTOR>○○建設株式会社</CONTRACTOR>
        <START_DATE>2023-04-01</START_DATE>
        <END_DATE>2023-09-30</END_DATE>
    </PROJECT_INFO>
    <WORK_RECORD>
        <WORK_DATE>2023-04-15</WORK_DATE>
        <WORK_TYPE>路盤工</WORK_TYPE>
        <PROGRESS_RATE>25.5</PROGRESS_RATE>
    </WORK_RECORD>
</CONSTRUCTION_PROJECT>"""

    # 9. 国土交通省報告書データ
    report_xml = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE REPORT SYSTEM "rep04.dtd">
<REPORT>
    <TITLE>道路交通量調査報告書</TITLE>
    <REPORT_DATE>2023-03-31</REPORT_DATE>
    <SURVEY_POINT>
        <POINT_NAME>国道1号線 東京IC付近</POINT_NAME>
        <TRAFFIC_VOLUME>45250</TRAFFIC_VOLUME>
        <SURVEY_TIME>24時間</SURVEY_TIME>
    </SURVEY_POINT>
</REPORT>"""

    # ファイルを作成
    files_data = [
        ("electronic_delivery.xml", electronic_delivery_xml),
        ("survey_results.xml", survey_results_xml),
        ("jpgis_data.xml", jpgis_xml),
        ("cad_sxf_drawing.xml", cad_sxf_xml),
        ("cost_estimation.xml", estimation_xml),
        ("facility_management.xml", facility_mgmt_xml),
        ("geographic_info.xml", geography_xml),
        ("construction_project.xml", construction_xml),
        ("mlit_report.xml", report_xml)
    ]
    
    for filename, content in files_data:
        with open(os.path.join(test_dir, filename), "w", encoding="utf-8") as f:
            f.write(content)
    
    print(f"MLIT XMLタイプ別テストファイルを作成しました: {test_dir}")
    print("作成されたファイル:")
    for filename, _ in files_data:
        print(f"  - {filename}")
    
    return test_dir

if __name__ == "__main__":
    create_mlit_test_xml_files()
    print("\n🎯 XMLタイプ別レイヤ名テスト:")
    print("1. QGISでGeo Importプラグインを開いてください")
    print("2. 'test_mlit_xml_types'フォルダを選択してください")  
    print("3. データをロードしてください")
    print("4. ✅ 期待される結果:")
    print("   📋 電子納品XML (CALS/EC準拠)")
    print("   📐 測量成果XML (測量成果電子納品要領)")
    print("   🗺️ JPGIS準拠地理空間情報XML")
    print("   📐 CAD/SXF関連XML")
    print("   💰 積算システムXML (JACIC準拠)")
    print("   🏢 施設管理XML")
    print("   🌏 地理空間情報XML")
    print("   🏗️ 建設工事関連XML")
    print("   📄 国土交通省報告書データ")
    print("5. 🎨 絵文字付きレイヤ名で表示されることを確認してください")