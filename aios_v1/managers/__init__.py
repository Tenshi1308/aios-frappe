from aios_v1.plugin_manager.registry import get_branches
from aios_v1.managers.base_manager import BaseManager

_managers = {}

def get_manager(branch_key: str) -> BaseManager:
    if branch_key not in _managers:
        matched = None
        for b in get_branches():
            if b["key"] == branch_key:
                matched = b
                break
        if not matched:
            matched = {
                "key": branch_key,
                "name": branch_key.capitalize(),
                "description": f"AI Manager {branch_key}"
            }
        _managers[branch_key] = BaseManager(matched)
    return _managers[branch_key]
