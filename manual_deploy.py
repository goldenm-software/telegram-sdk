"""Manual deploy"""

import os
import shutil

from dotenv import load_dotenv

load_dotenv()

# Remove previous build
if os.path.exists('dist'):
  shutil.rmtree('dist')

if os.path.exists('telegram_sdk.egg-info'):
  shutil.rmtree('telegram_sdk.egg-info')

os.system('python -m build')
os.system(f'python -m twine upload -u __token__ -p {os.getenv("PYPI_TOKEN")} dist/*')
