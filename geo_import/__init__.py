"""Compatibility alias package: `geo_import` -> `qgis_data_catalog_integration`.

This package exposes the existing `qgis_data_catalog_integration` package
under the new name `geo_import` so both import styles work during the
migration. It keeps runtime compatibility and avoids renaming the on-disk
plugin folder.
"""
from importlib import import_module
import importlib
import sys

# Import the original package
_orig_name = 'qgis_data_catalog_integration'
_orig = import_module(_orig_name)

# Make this package use the same __path__ as the original so submodule imports
# (e.g. `import geo_import.ckan_browser`) resolve to the existing files.
try:
    __path__ = list(_orig.__path__)
except AttributeError:
    # If original isn't a package for some reason, leave path alone
    pass

# Re-export public names from the original package
for _name, _obj in list(_orig.__dict__.items()):
    if not _name.startswith('__'):
        globals()[_name] = _obj

__all__ = getattr(_orig, '__all__', [n for n in globals().keys() if not n.startswith('_')])

def __getattr__(name):
    """Lazy attribute access: import submodules from the original package.

    Allows `from geo_import import ckan_browser` and attribute-style access
    to submodules.
    """
    # If attribute already exists, return it
    if name in globals():
        return globals()[name]

    # Try to import `qgis_data_catalog_integration.<name>` and return module
    submod_name = f"{_orig_name}.{name}"
    try:
        submod = importlib.import_module(submod_name)
    except Exception:
        raise AttributeError(f"module 'geo_import' has no attribute '{name}'")
    globals()[name] = submod
    return submod

def __dir__():
    names = set(globals().keys())
    try:
        names.update(name for _, name, _ in import_module(_orig_name).__all__)
    except Exception:
        pass
    return sorted(names)
