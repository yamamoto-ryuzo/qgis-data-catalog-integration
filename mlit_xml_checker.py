# -*- coding: utf-8 -*-
"""
国土交通省XML診断ツール - スタンドアロン版
XMLファイルが国土交通省関連のデータかどうかを判定します
"""

import sys
import os

# QGISプラグインのパスを追加
plugin_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, plugin_path)

try:
    from xml_attribute_loader import diagnose_mlit_xml, print_mlit_xml_diagnosis
except ImportError:
    from qgis_data_catalog_integration.xml_attribute_loader import diagnose_mlit_xml, print_mlit_xml_diagnosis


def test_xml_files():
    """テスト用XMLファイルの診断を実行"""
    
    # テスト用XMLファイルのサンプル
    test_cases = [
        # 国土交通省報告書XML（Shift_JIS）
        {
            'filename': 'mlit_report_sample.xml',
            'content': '''<?xml version="1.0" encoding="Shift_JIS" ?>
<!DOCTYPE reportdata SYSTEM "REP04.DTD">
<?xml-stylesheet type="text/xsl" href="REP04.XSL"?>
<reportdata DTD_version="04">
  <報告書ファイル情報>
    <報告書名>業務概要版</報告書名>
    <報告書ファイル名>REPORT01.PDF</報告書ファイル名>
    <報告書ファイル日本語名>業務概要版.PDF</報告書ファイル日本語名>
  </報告書ファイル情報>
</reportdata>'''
        },
        # JPGIS準拠地理空間情報XML
        {
            'filename': 'jpgis_sample.xml',
            'content': '''<?xml version="1.0" encoding="UTF-8"?>
<Dataset xmlns="http://jpgis.mlit.go.jp/" xmlns:gml="http://www.opengis.net/gml">
  <地物>
    <Feature>
      <空間属性>
        <gml:Point>
          <gml:coordinates>35.681382,139.766084</gml:coordinates>
        </gml:Point>
      </空間属性>
    </Feature>
  </地物>
</Dataset>'''
        },
        # 積算システムXML
        {
            'filename': 'estimation_sample.xml',
            'content': '''<?xml version="1.0" encoding="UTF-8"?>
<積算データ>
  <工種>
    <種別>土工</種別>
    <細別>掘削</細別>
    <規格>土砂</規格>
    <単価>1500</単価>
    <数量>100</数量>
  </工種>
</積算データ>'''
        },
        # 一般的なXML（非国土交通省）
        {
            'filename': 'generic_sample.xml',
            'content': '''<?xml version="1.0" encoding="UTF-8"?>
<data>
  <record>
    <id>1</id>
    <name>Sample Data</name>
    <value>Test Value</value>
  </record>
</data>'''
        }
    ]
    
    print("=== 国土交通省XML診断テスト ===\n")
    
    # テストファイルを作成して診断
    for i, test_case in enumerate(test_cases, 1):
        filename = test_case['filename']
        
        # 一時ファイルを作成
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(test_case['content'])
        
        print(f"テスト {i}: {filename}")
        print("-" * 40)
        
        try:
            # 診断実行
            result = diagnose_mlit_xml(filename)
            
            # 結果表示
            print(f"国土交通省XML: {'はい' if result['is_mlit_xml'] else 'いいえ'}")
            print(f"XMLタイプ: {result['xml_type']}")
            print(f"信頼度: {result['confidence']:.2f} ({result['confidence']*100:.1f}%)")
            print(f"推奨事項: {result['recommendation']}")
            
            # 詳細情報
            details = result['details']
            if details.get('dtd_detected'):
                print(f"DTD: {details['dtd_detected']}")
            if details.get('mlit_keywords'):
                print(f"キーワード: {', '.join(details['mlit_keywords'][:3])}")
            
        except Exception as e:
            print(f"エラー: {e}")
        
        finally:
            # 一時ファイルを削除
            if os.path.exists(filename):
                os.remove(filename)
        
        print()


def main():
    """メイン関数"""
    if len(sys.argv) > 1:
        # コマンドライン引数でファイルが指定された場合
        xml_file_path = sys.argv[1]
        
        if not os.path.exists(xml_file_path):
            print(f"エラー: ファイルが見つかりません: {xml_file_path}")
            return
        
        print_mlit_xml_diagnosis(xml_file_path)
    else:
        # テストモードで実行
        print("XMLファイルが指定されていません。テストモードで実行します。\n")
        test_xml_files()
        print("\n使用方法:")
        print(f"  python {os.path.basename(__file__)} <XMLファイルパス>")
        print("例:")
        print(f"  python {os.path.basename(__file__)} report.xml")


if __name__ == "__main__":
    main()