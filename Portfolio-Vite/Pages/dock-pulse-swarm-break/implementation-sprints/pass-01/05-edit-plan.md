# Edit Plan

### game.js

- Reason: Make the runtime mechanically distinct on the first playable pass.
- Exact change: Replace relic collection and exit unlock messaging with relay repair state, route pressure tracking, and a win state based on repaired nodes.
- Invariant: Keep movement, dash, pulse input, and the main animation loop intact.
- Verification command: node --check game.js

### story-structure.json

				- Reason: Provide relay-specific data and objective text that the runtime can surface directly.
				- Exact change: Rewrite objective, control copy, and scene rule labels to describe repairing relays under noise pressure.
				- Invariant: Preserve valid JSON and retain canonical brainstorm metadata.
				- Verification command: python3 - <<'PY'
import json, pathlib
json.load(open(pathlib.Path('story-structure.json')))
print('ok')
PY

### index.html

				- Reason: Make the shell readable and aligned with the actual relay run.
				- Exact change: Update HUD labels, overlay body, and control hint copy so the page explains relay repair, noise risk, and restart flow cleanly.
				- Invariant: Preserve the existing responsive shell and script entrypoint.
				- Verification command: python3 - <<'PY'
from pathlib import Path
text = Path('index.html').read_text()
assert 'game.js' in text
print('ok')
PY
