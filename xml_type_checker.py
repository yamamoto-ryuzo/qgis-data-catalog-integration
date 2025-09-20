#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
XMLタイプ識別診断ツール（スタンドアロン版）

PyQt5に依存せずに、XMLファイルのタイプを識別し、絵文字付きレイヤ名を表示
"""

import os
import sys
from xml.etree import ElementTree as ET


class SimpleXmlTypeChecker:
    """シンプルなXMLタイプ識別クラス"""
    
    def __init__(self):
        self.mlit_xml_patterns = {
            'electronic_delivery': ['電子納品', '工事完成図書', '土木設計業務', 'CALS/EC', 'OFFICE-INDEX', 'CONSTRUCTION_NAME', 'OFFICE_NAME'],
            'survey_results': ['測量成果', '基準点', '水準点', '多角点', 'SURVEY', 'POINT_DATA', 'COORDINATE_X'],
            'jpgis': ['JPGIS', 'GM_', 'GML', 'gml:', 'xmlns:gml', 'ksj_app_schema', 'AdministrativeBoundary'],
            'cad_sxf': ['SXF', 'CAD', 'P21', 'EXPRESS', 'SXF_DATA', 'LAYER_NAME', 'FEATURE_CODE'],
            'estimation': ['積算', '工種', '種別', '細別', '単価', 'COST', 'COST_ESTIMATION', 'UNIT_PRICE'],
            'facility_mgmt': ['施設', '設備', '機器', '点検', '維持管理', 'FACILITY', 'FACILITY_MANAGEMENT', 'INSPECTION_RECORD'],
            'geography': ['地理空間', '座標', '測地', 'COORDINATE', 'DATUM', 'GEOGRAPHIC_DATA', 'LOCATION_INFO'],
            'construction': ['施工', 'PROJECT_INFO', 'WORK_RECORD']  # より具体的なパターンに変更
        }
    
    def _detect_encoding(self, file_path):
        """ファイルのエンコーディングを検出"""
        encodings = ['utf-8', 'shift_jis', 'cp932', 'euc-jp', 'iso-2022-jp']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    f.read()
                return encoding
            except UnicodeDecodeError:
                continue
        
        return 'utf-8'  # デフォルト
    
    def _parse_xml(self, xml_file_path):
        """XMLファイルを解析"""
        try:
            encoding = self._detect_encoding(xml_file_path)
            with open(xml_file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            # DTD宣言を除去（簡易版）
            lines = content.split('\n')
            filtered_lines = []
            for line in lines:
                if not line.strip().startswith('<!DOCTYPE'):
                    filtered_lines.append(line)
            
            filtered_content = '\n'.join(filtered_lines)
            root = ET.fromstring(filtered_content)
            return root, content.lower(), encoding
            
        except Exception as e:
            print(f"XML解析エラー: {e}")
            return None, None, None
    
    def identify_xml_type(self, xml_file_path):
        """XMLファイルのタイプを識別"""
        root, xml_content_str, encoding = self._parse_xml(xml_file_path)
        
        if root is None:
            return "解析不可", 0.0, {}
        
        # ルート要素の名前とその子要素を確認
        root_tag = root.tag.lower()
        if '}' in root_tag:
            root_tag = root_tag.split('}')[1]
        
        # 子要素の名前リストを作成
        child_tags = []
        for child in root:
            tag_name = child.tag.lower()
            if '}' in tag_name:
                tag_name = tag_name.split('}')[1]
            child_tags.append(tag_name)
        
        # DTD宣言からの識別
        if 'rep04.dtd' in xml_content_str or 'rep' in xml_content_str:
            return "📄 国土交通省報告書データ", 0.9, {'dtd': 'rep04.dtd detected'}
        
        # 各パターンとマッチング
        best_match = None
        best_confidence = 0.0
        match_details = {}
        
        for xml_type, patterns in self.mlit_xml_patterns.items():
            confidence = 0.0
            matched_patterns = []
            
            for pattern in patterns:
                pattern_lower = pattern.lower()
                if (pattern_lower in xml_content_str or 
                    pattern_lower in root_tag or 
                    any(pattern_lower in tag for tag in child_tags)):
                    confidence += 0.3
                    matched_patterns.append(pattern)
            
            if confidence > best_confidence:
                best_confidence = confidence
                best_match = xml_type
                match_details = {
                    'matched_patterns': matched_patterns,
                    'root_tag': root_tag,
                    'child_tags': child_tags[:5],  # 最初の5つ
                    'encoding': encoding
                }
        
        if best_match:
            type_names = {
                'electronic_delivery': "📋 電子納品XML (CALS/EC準拠)",
                'survey_results': "📐 測量成果XML (測量成果電子納品要領)", 
                'jpgis': "🗺️ JPGIS準拠地理空間情報XML",
                'cad_sxf': "📐 CAD/SXF関連XML",
                'estimation': "💰 積算システムXML (JACIC準拠)",
                'facility_mgmt': "🏢 施設管理XML",
                'geography': "🌏 地理空間情報XML",
                'construction': "🏗️ 建設工事関連XML"
            }
            return type_names.get(best_match, f"{best_match}関連XML"), best_confidence, match_details
        
        # 特定の構造からの識別
        if '報告書' in root_tag or '情報' in root_tag:
            return "📝 日本語XML（報告書/情報系）", 0.6, {'reason': 'japanese structure'}
        elif 'feature' in root_tag or 'gml' in xml_content_str:
            return "🗺️ GML/地理情報XML", 0.7, {'reason': 'gml structure'}
        elif root_tag in ['data', 'records', 'items']:
            return "📊 データテーブルXML", 0.5, {'reason': 'table structure'}
        
        return "📄 汎用XML", 0.3, {'reason': 'default'}


def diagnose_xml_type(xml_file_path):
    """XMLファイルのタイプを診断し、絵文字付きレイヤ名を表示"""
    
    print(f"\n🔍 XMLファイル診断: {os.path.basename(xml_file_path)}")
    print("=" * 60)
    
    if not os.path.exists(xml_file_path):
        print("❌ ファイルが存在しません")
        return
    
    checker = SimpleXmlTypeChecker()
    
    try:
        xml_type, confidence, details = checker.identify_xml_type(xml_file_path)
        
        print(f"✅ XMLファイル形式チェック: OK")
        print(f"\n🎨 XMLタイプ識別結果:")
        print(f"   タイプ: {xml_type}")
        print(f"   信頼度: {confidence:.2f}")
        
        if details:
            print(f"\n📊 詳細情報:")
            for key, value in details.items():
                if isinstance(value, list):
                    print(f"   {key}: {', '.join(map(str, value))}")
                else:
                    print(f"   {key}: {value}")
        
        print(f"\n🏷️ 最終レイヤ名: {xml_type}")
        
    except Exception as e:
        print(f"❌ 診断エラー: {str(e)}")
        import traceback
        traceback.print_exc()


def test_all_xml_types():
    """test_mlit_xml_typesディレクトリの全XMLファイルをテスト"""
    
    test_dir = "test_mlit_xml_types"
    if not os.path.exists(test_dir):
        print(f"❌ テストディレクトリが見つかりません: {test_dir}")
        print("先にtest_mlit_xml_types.pyを実行してテストファイルを作成してください")
        return
    
    xml_files = [f for f in os.listdir(test_dir) if f.endswith('.xml')]
    
    if not xml_files:
        print(f"❌ {test_dir}にXMLファイルが見つかりません")
        return
    
    print(f"🎯 {len(xml_files)}個のXMLファイルをテストします")
    print("=" * 80)
    
    # 結果をサマリー表示
    results = []
    
    for xml_file in sorted(xml_files):
        xml_path = os.path.join(test_dir, xml_file)
        checker = SimpleXmlTypeChecker()
        xml_type, confidence, details = checker.identify_xml_type(xml_path)
        results.append((xml_file, xml_type, confidence))
        diagnose_xml_type(xml_path)
        print()
    
    # サマリー表示
    print("📋 テスト結果サマリー:")
    print("=" * 80)
    for filename, xml_type, confidence in results:
        print(f"  {filename:25} → {xml_type} (信頼度: {confidence:.2f})")


def main():
    """メイン関数"""
    if len(sys.argv) > 1:
        # 特定のファイルをテスト
        xml_file_path = sys.argv[1]
        diagnose_xml_type(xml_file_path)
    else:
        # 全テストファイルをテスト
        test_all_xml_types()


if __name__ == "__main__":
    main()