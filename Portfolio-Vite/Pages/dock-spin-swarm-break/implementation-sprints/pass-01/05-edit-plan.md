# Edit Plan

### game.js

- Reason: Implement the spin mechanic.
- Exact change: Add `this.player.mesh.rotation.y += delta * 20` inside the dash block.
- Invariant: The dash speed must remain 28.0.
- Verification command: grep 'rotation.y' game.js
