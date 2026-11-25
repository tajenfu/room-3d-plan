"""Build room-offline.html and room-3d-plan.zip, which work without internet.

Usage: python build_offline.py <three_dir>

<three_dir> is an unpacked copy of the three.js 0.170.0 npm package.
"""
import base64
import json
import pathlib
import re
import sys
import zipfile

if len(sys.argv) != 2:
    sys.exit(__doc__)
here = pathlib.Path(__file__).parent
three = pathlib.Path(sys.argv[1])
html = (here / 'room.html').read_text(encoding='utf-8')

modules = {'three': 'build/three.module.js'}
for path in ['controls/OrbitControls.js', 'renderers/CSS2DRenderer.js',
             'geometries/RoundedBoxGeometry.js', 'exporters/GLTFExporter.js']:
    modules['three/addons/' + path] = 'examples/jsm/' + path

# Each library file becomes a data: URL that the import map points to.
imports = {name: 'data:text/javascript;base64,' + base64.b64encode((three / file).read_bytes()).decode()
           for name, file in modules.items()}
importmap = '<script type="importmap">\n' + json.dumps({'imports': imports}) + '\n</script>'
html, n = re.subn(r'<script type="importmap">.*?</script>', lambda _: importmap, html, count=1, flags=re.S)
assert n == 1 and 'cdn.jsdelivr.net' not in html

licence = (three / 'LICENSE').read_text(encoding='utf-8')
assert '--' not in licence
html = html.replace('<!doctype html>', f'<!doctype html>\n<!-- Includes three.js 0.170.0\n{licence}-->', 1)
(here / 'room-offline.html').write_text(html, encoding='utf-8', newline='\n')

with zipfile.ZipFile(here / 'room-3d-plan.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('room.html', html)
    for name in ['README.txt', 'room-versions.json']:
        z.write(here / name, name)
print('Built room-offline.html and room-3d-plan.zip')
