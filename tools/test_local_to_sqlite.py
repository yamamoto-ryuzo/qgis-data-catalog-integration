import os, json, sqlite3, sys

# Usage: python test_local_to_sqlite.py <local_folder>
local = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'CKAN-Browser')
local = os.path.abspath(local)
print('Local folder:', local)

# 除外ファイル・フォルダのリスト（メタデータファイルや一般的なシステムファイル）
exclude_names = {
    'packages.json', 'groups.json', 'thumbs.db', 'desktop.ini', '.ds_store',
    '__pycache__', '.git', '.svn', 'node_modules', '.tmp', 'temp'
}
exclude_extensions = {
    '.tmp', '.temp', '.bak', '.log', '.cache', '.lock', '.swp', '.swo',
    '.exe', '.dll', '.so', '.dylib', '.app', '.deb', '.rpm', '.msi'
}

def should_include_file(filename, filepath):
    """
    ファイルをデータベースに含めるかどうかを判定
    除外対象以外のすべてのファイルを含める（拡張子制限なし）
    """
    fname_lower = filename.lower()
    ext_lower = os.path.splitext(filename)[1].lower()
    
    # 除外ファイル名（完全一致）
    if fname_lower in exclude_names:
        return False
    
    # 除外拡張子
    if ext_lower in exclude_extensions:
        return False
    
    # 隠しファイル（Unix系）
    if filename.startswith('.') and len(filename) > 1:
        return False
    
    # 一時ファイル
    if filename.startswith('~') or filename.endswith('~'):
        return False
    
    # 空ファイルは除外（0バイト）
    try:
        if os.path.getsize(filepath) == 0:
            return False
    except:
        pass
    
    return True
generated_pkgs = []
generated_groups = []
exclude_names = {'packages.json', 'groups.json'}

# immediate subdirectories -> groups and packages
for name in os.listdir(local):
    p = os.path.join(local, name)
    if os.path.isdir(p):
        grp = {'id': name, 'name': name, 'title': name, 'description': ''}
        generated_groups.append(grp)
        i = 1
        resources = []
        for root, dirs, files in os.walk(p):
            for fname in files:
                filepath = os.path.join(root, fname)
                if should_include_file(fname, filepath):
                    ext = os.path.splitext(fname)[1].lower().lstrip('.') or 'file'
                    file_url = 'file:///' + os.path.abspath(filepath).replace('\\', '/')
                    resources.append({'id': f'{name}-res-{i}', 'name': fname, 'format': ext, 'url': file_url})
                    i += 1
        if resources:
            pkg = {'id': f'local-package-{name}', 'title': name, 'resources': resources, 'groups': [{'name': name}]}
            generated_pkgs.append(pkg)

# root-level files -> a package
root_resources = []
j = 1
for fname in os.listdir(local):
    filepath = os.path.join(local, fname)
    if os.path.isfile(filepath):
        if should_include_file(fname, filepath):
            ext = os.path.splitext(fname)[1].lower().lstrip('.') or 'file'
            file_url = 'file:///' + os.path.abspath(filepath).replace('\\', '/')
            root_resources.append({'id': f'root-res-{j}', 'name': fname, 'format': ext, 'url': file_url})
            j += 1
if root_resources:
    pkg_root = {'id': 'local-package-root', 'title': os.path.basename(local) or 'local-package', 'resources': root_resources}
    generated_pkgs.insert(0, pkg_root)

all_results = generated_pkgs

# write packages.json and groups.json
pkg_json_path = os.path.join(local, 'packages.json')
with open(pkg_json_path, 'w', encoding='utf-8') as pf:
    json.dump(all_results, pf, ensure_ascii=False, indent=2)
print('Wrote', pkg_json_path)

groups_path = os.path.join(local, 'groups.json')
with open(groups_path, 'w', encoding='utf-8') as gf:
    json.dump(generated_groups, gf, ensure_ascii=False, indent=2)
print('Wrote', groups_path)

# save to sqlite using local ckan_cache.db
db_path = os.path.join(local, 'ckan_cache.db')
print('DB path:', db_path)
# create tables
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS packages (id TEXT PRIMARY KEY, title TEXT, notes TEXT, author TEXT, author_email TEXT, license_id TEXT, raw_json TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS resources (id TEXT PRIMARY KEY, package_id TEXT, format TEXT, url TEXT, name TEXT, raw_json TEXT, FOREIGN KEY(package_id) REFERENCES packages(id))''')
c.execute('''CREATE TABLE IF NOT EXISTS groups (raw_json TEXT)''')

# insert
for pkg in all_results:
    c.execute('INSERT OR REPLACE INTO packages (id, title, notes, author, author_email, license_id, raw_json) VALUES (?, ?, ?, ?, ?, ?, ?)', (
        pkg.get('id'), pkg.get('title'), pkg.get('notes'), pkg.get('author'), pkg.get('author_email'), pkg.get('license_id'), json.dumps(pkg, ensure_ascii=False)
    ))
    for res in pkg.get('resources', []):
        c.execute('INSERT OR REPLACE INTO resources (id, package_id, format, url, name, raw_json) VALUES (?, ?, ?, ?, ?, ?)', (
            res.get('id'), pkg.get('id'), res.get('format'), res.get('url'), res.get('name'), json.dumps(res, ensure_ascii=False)
        ))

c.execute('DELETE FROM groups')
for group in generated_groups:
    c.execute('INSERT INTO groups (raw_json) VALUES (?)', (json.dumps(group),))

conn.commit()

# report
c.execute('SELECT count(*) FROM packages')
print('packages count:', c.fetchone()[0])
c.execute('SELECT count(*) FROM resources')
print('resources count:', c.fetchone()[0])
c.execute('SELECT count(*) FROM groups')
print('groups count:', c.fetchone()[0])

print('\nSample package raw_json:')
c.execute('SELECT raw_json FROM packages LIMIT 1')
row = c.fetchone()
if row:
    print(row[0][:500])
else:
    print('none')

conn.close()
