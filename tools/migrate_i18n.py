import os
import shutil

root = os.path.dirname(os.path.dirname(__file__))
i18n_dir = os.path.join(root, 'qgis_data_catalog_integration', 'i18n')

if not os.path.isdir(i18n_dir):
    print('i18n directory not found:', i18n_dir)
    raise SystemExit(1)

for fname in os.listdir(i18n_dir):
    if fname.startswith('CKANBrowser_') and fname.endswith('.ts'):
        src = os.path.join(i18n_dir, fname)
        dst = os.path.join(i18n_dir, 'geo_import_' + fname.split('_', 1)[1])
        if os.path.exists(dst):
            print('Exists, skipping:', os.path.basename(dst))
            continue
        shutil.copyfile(src, dst)
        print('Copied', os.path.basename(src), '->', os.path.basename(dst))

print('Done')
