

import os


import os
import re
import zipfile
import shutil
from configparser import ConfigParser

# Windowsのごみ箱へ移動（pip不要）
import sys
def move_to_trash(filepath):
    if sys.platform.startswith('win'):
        import ctypes
        from ctypes import wintypes
        class SHFILEOPSTRUCTW(ctypes.Structure):
            _fields_ = [
                ('hwnd', wintypes.HWND),
                ('wFunc', wintypes.UINT),
                ('pFrom', wintypes.LPCWSTR),
                ('pTo', wintypes.LPCWSTR),
                ('fFlags', ctypes.c_ushort),  # 修正: FILEOP_FLAGS → c_ushort
                ('fAnyOperationsAborted', wintypes.BOOL),
                ('hNameMappings', wintypes.LPVOID),
                ('lpszProgressTitle', wintypes.LPCWSTR),
            ]
        FO_DELETE = 3
        FOF_ALLOWUNDO = 0x40
        FOF_NOCONFIRMATION = 0x10
        op = SHFILEOPSTRUCTW()
        op.hwnd = 0
        op.wFunc = FO_DELETE
        op.pFrom = filepath + '\0\0'
        op.pTo = None
        op.fFlags = FOF_ALLOWUNDO | FOF_NOCONFIRMATION
        op.fAnyOperationsAborted = False
        op.hNameMappings = None
        op.lpszProgressTitle = None
        res = ctypes.windll.shell32.SHFileOperationW(ctypes.byref(op))
        return res == 0
    else:
        # 非Windowsは完全削除
        os.remove(filepath)
        return True


PLUGIN_DIR = 'qgis_data_catalog_integration'  # フォルダ名もPEP 8準拠に変更
META_FILE = os.path.join(PLUGIN_DIR, 'metadata.txt')
ZIP_PREFIX = 'QGISDataCatalogIntegration_'

# 配布に含めるファイル・ディレクトリ（必要に応じて追加）
INCLUDE_FILES = [
    PLUGIN_DIR,
    # 'readme.md',  # ルートのreadmeも含めたい場合はコメント解除
]

def parse_version(verstr):
    m = re.match(r'V?(\d+)\.(\d+)\.(\d+)', verstr)
    if not m:
        raise ValueError('Invalid version string: ' + verstr)
    return tuple(map(int, m.groups()))

def bump_patch(ver):
    a, b, c = ver
    return (a, b, c+1)

def version_to_str(ver):
    return f'V{ver[0]}.{ver[1]}.{ver[2]}'

def main():


    # metadata.txtからversion=行を直接パース
    with open(META_FILE, encoding='utf-8') as f:
        lines = f.readlines()
    verstr = None
    for line in lines:
        if line.strip().startswith('version='):
            verstr = line.strip().split('=', 1)[1]
            break
    if not verstr:
        raise ValueError('version entry not found in metadata.txt')
    ver = parse_version(verstr)
    new_ver = bump_patch(ver)
    new_verstr = version_to_str(new_ver)

    # metadata.txtのバージョン書き換え
    with open(META_FILE, 'w', encoding='utf-8') as f:
        for line in lines:
            if line.strip().startswith('version='):
                f.write(f'version={new_verstr}\n')
            else:
                f.write(line)

    # 旧ZIP削除（ひとつ前のバージョンのみ削除、他は残す）
    prev_zipname = f'{ZIP_PREFIX}{ver[0]}.{ver[1]}.{ver[2]}.zip'
    if os.path.exists(prev_zipname):
        move_to_trash(prev_zipname)

    # 一時作業ディレクトリ作成

    tmp_dir = f'{PLUGIN_DIR}_tmp_pack'
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir)

    # 必要なファイル・ディレクトリを一時ディレクトリにコピー
    for item in INCLUDE_FILES:
        if os.path.isdir(item):
            target_dir = os.path.join(tmp_dir, os.path.basename(item))
            shutil.copytree(item, target_dir)
        elif os.path.isfile(item):
            shutil.copy2(item, os.path.join(tmp_dir, os.path.basename(item)))

    # ZIP作成

    zipname = f'{ZIP_PREFIX}{new_ver[0]}.{new_ver[1]}.{new_ver[2]}.zip'
    with zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(tmp_dir):
            # __pycache__ディレクトリをスキップ
            if '__pycache__' in dirs:
                dirs.remove('__pycache__')
            for file in files:
                # .pycファイルをスキップ
                if file.endswith('.pyc'):
                    continue
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, tmp_dir)
                zf.write(abs_path, rel_path)

    # 作業ディレクトリ削除
    shutil.rmtree(tmp_dir)
    print(f'Created: {zipname}')
    print(f'Updated {META_FILE} to version {new_verstr}')

if __name__ == '__main__':
    main()

