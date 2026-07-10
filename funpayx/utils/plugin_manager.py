import importlib.util
import sys
import json
from pathlib import Path


plugins_dir = Path('plugins')

def load_plugins(fp):
    plugins_dir.mkdir(parents=True, exist_ok=True)
    if plugins_dir.exists():
        for p_fol in plugins_dir.iterdir():
            if p_fol.is_dir():
                config_file = p_fol / 'plugin.json'
                if not config_file.exists():
                    continue
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                routers_paths = config.get('routers', [])
                if isinstance(routers_paths, str):
                    routers_paths = [routers_paths]
                for r_path in routers_paths:
                    *file_parts, router_var_name = r_path.split('.')
                    file_rel_path = Path(*file_parts).with_suffix('.py')
                    router_file = p_fol / file_rel_path
                    if router_file.exists():
                        sub_module_name = '.'.join(file_parts)
                        module_name = f'plugins.{p_fol.name}.{sub_module_name}'
                        spec = importlib.util.spec_from_file_location(module_name, router_file)
                        module = importlib.util.module_from_spec(spec)
                        sys.modules[module_name] = module
                        spec.loader.exec_module(module)
                        plugin_router = getattr(module, router_var_name)
                        fp.router.include_router(plugin_router)