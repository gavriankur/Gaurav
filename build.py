import json, os, shutil
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
root=Path(__file__).parent
now=datetime.now(ZoneInfo('Asia/Kolkata')).date()
if os.getenv('BUILD_DATE'): now=date.fromisoformat(os.environ['BUILD_DATE'])
posts=json.loads((root/'posts.json').read_text())
for p in posts:
 p['release']=p.get('publish_on') or (date.fromisoformat(p['date'])-timedelta(days=5)).isoformat()
 p['available']=p['release']<=now.isoformat()
out=root/'public'; out.mkdir(exist_ok=True)
shutil.copyfile(root/'diwali.png',out/'diwali.png')
html=(root/'template.html').read_text().replace('__DATA__',json.dumps(posts).replace('<','\\u003c')).replace('__UPDATED__',now.strftime('%d %b %Y'))
(out/'index.html').write_text(html)
print(f'Built {len(posts)} posts; {sum(p["available"] for p in posts)} available on {now}')
