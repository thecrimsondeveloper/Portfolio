
		# Validation Loop 01 Edit Plan

		### story-structure.json

- Reason: Expose movement, sentry, and hazard tuning needed by the runtime
- Exact change: Add player movement tuning for beatWindow, mirrorWindow, and dodgeCooldown; add sentry tuning for visionRange, alertSeconds, chaseSpeed, and stunSeconds; add one hazard tuning block for rotateInterval or lockDuration
- Invariant: Preserve the current story payload structure and existing level metadata
- Verification command: python3 -m json.tool Pages/pier-spin-swarm-break/story-structure.json

### game.js

- Reason: Implement the missing mechanics that distinguish the factory escape run
- Exact change: Add rhythm-step and mirror-walk movement logic, one sentry patrol-alert-chase state machine, one rotating or locking route hazard, and matching HUD updates for dawn, keys, relay, and alert status
- Invariant: Preserve existing render loop, asset loading, and core objective flow
- Verification command: node --check Pages/pier-spin-swarm-break/game.js

### index.html

- Reason: Keep shell feedback aligned with the actual runtime state
- Exact change: Add or relabel compact HUD elements for Keys, Dawn Timer, Relay progress, and Alert status only if stable ids are needed by game.js
- Invariant: Do not rewrite the shell structure or break current script hooks
- Verification command: open Pages/pier-spin-swarm-break/index.html
