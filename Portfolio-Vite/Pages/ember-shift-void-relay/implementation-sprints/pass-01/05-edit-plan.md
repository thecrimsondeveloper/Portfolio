# Edit Plan

### game.js

- Reason: Implement shift toggle.
- Exact change: Inside updatePlayer, toggle this.player.isShifted and update mesh color.
- Invariant: Rotation and velocity should not be reset.
- Verification command: grep 'isShifted' game.js
