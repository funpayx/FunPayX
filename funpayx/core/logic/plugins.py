import json
import sys
import httpx
import io
import zipfile
import shutil
from pathlib import Path


PLUGINS_DIR = Path('plugins')

marketplace_structure = {
  "plugins": [
    {
      "id": "my_test_plugin",
      "repo": "someuser/some-plugin-repo",
      "commit": "a1b2c3d4e5f6",
      "path": "my_test_plugin",
      "title": "Пример плагина",
      "verified_by": "@sanyalca"
    }
  ]
}

CORE_DIR = Path('funpayx/core/logic')

class PluginManager:
    @staticmethod
    def get_marketplace():
        marketplace = CORE_DIR / 'marketplace.json'
        if not marketplace.exists():
            with open(marketplace, 'w', encoding='utf-8') as f:
                json.dump(marketplace_structure, f, ensure_ascii=False, indent=2)
        with open(marketplace, 'r', encoding='utf-8') as f:
            market = json.load(f)
        return market['plugins']

    @staticmethod
    def find_plugin_by_id(id):
        market = PluginManager.get_marketplace()
        for i in market:
            if i['id'] == id:
                return i

    @staticmethod
    def delete_plugin(plugin_id):
        for json_path in PLUGINS_DIR.rglob('plugin.json'):
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if int(data['id']) == int(plugin_id):
                    shutil.rmtree(json_path.parent)
                    return 'Успешно удалено. Используйте /restart для применения изменений.'
        return 'Папка не найдена по неизвестной причине'
    
    @staticmethod
    async def install_from_marketplace(entry: dict):
        url = f"https://codeload.github.com/{entry['repo']}/zip/{entry['commit']}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            if resp.status_code != 200:
                raise RuntimeError(f'Не удалось скачать архив: HTTP {resp.status_code}')
            data = await resp.aread()
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            names = zf.namelist()
            root_prefix = names[0].split('/')[0] + '/'
            source_prefix = root_prefix + (entry.get('path', '').rstrip('/') + '/' if entry.get('path') else '')
            target_dir = PLUGINS_DIR / entry['id']
            target_dir.mkdir(parents=True, exist_ok=True)
            for member in names:
                if not member.startswith(source_prefix) or member == source_prefix:
                    continue
                rel_path = member[len(source_prefix):]
                target = (target_dir / rel_path).resolve()
                if not str(target).startswith(str(target_dir.resolve())):
                    raise RuntimeError('Архив содержит подозрительные пути')
                if member.endswith('/'):
                    target.mkdir(parents=True, exist_ok=True)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(zf.read(member))