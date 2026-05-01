# Edit Plan

### story-structure.json

- Reason: Give the sentry archetype explicit tuning fields
- Exact change: Add sentry tuning values for visionRange, alertSeconds, chaseSpeed, and stunSeconds with starter defaults
- Invariant: Preserve current story payload shape
- Verification command: python3 -m json.tool Pages/pier-spin-swarm-break/story-structure.json

### game.js

- Reason: Replace generic pressure with one readable sentry archetype
- Exact change: Add sentry state fields, detection checks, patrol behavior, chase windows, and brief interrupt handling tied to existing pulse or dodge actions
- Invariant: Preserve player controls, render loop, and existing objective flow
- Verification command: node --check Pages/pier-spin-swarm-break/game.js

### index.html

- Reason: Optionally surface stealth state to the player
- Exact change: Add or relabel a compact status element for Hidden or Alert only if it does not conflict with current HUD bindings
- Invariant: Keep the shell stable and additive
- Verification command: open Pages/pier-spin-swarm-break/index.html
