# Edit Plan

### game.js

- Reason: Make the enemy slice mechanically distinct without broad rewrites.
- Exact change: Add a commander enemy that claims route space, responds to pulse, and creates short repair windows when interrupted.
- Invariant: Keep the current animation loop and base swarm behavior intact.
- Verification command: node --check game.js

### story-structure.json

				- Reason: Expose commander-role data and route-pressure language to the runtime and documentation.
				- Exact change: Update enemy and objective fields to name commander lane-control behavior and pulse counterplay.
				- Invariant: Preserve valid JSON and canonical brainstorm metadata.
				- Verification command: python3 - <<'PY'
import json, pathlib
json.load(open(pathlib.Path('story-structure.json')))
print('ok')
PY

### index.html

				- Reason: Keep shell messaging aligned with the commander pressure loop.
				- Exact change: Use the status line and telemetry labels to surface commander pressure without changing layout structure.
				- Invariant: Preserve the current page shell and script entrypoint.
				- Verification command: python3 - <<'PY'
from pathlib import Path
text = Path('index.html').read_text()
assert 'game.js' in text
print('ok')
PY
