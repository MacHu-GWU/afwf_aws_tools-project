import yaml
from pathlib_mate import Path

p = Path(__file__).change(new_basename="console-urls.yml")

data = yaml.load(p.read_text(encoding="utf-8"), Loader=yaml.SafeLoader)
print(data[0])