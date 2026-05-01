
		# Validation Loop 02 Breakdown


- 1) Add ember fields to story-structure.json (player.emberMax, player.emberRechargeRate, player.pulseCost).
- 2) Edit game.js: add player.ember, show ember in HUD, require ember >= pulseCost to trigger pulse and subtract cost.
- 3) Edit game.js: on triggerPulse set hazard.stun timer and ensure updateHazards skips damage while hazard.stun>0.
- 4) Ensure enemy stun behavior remains compatible and is still triggered by pulse.
- 5) Update index.html overlay hint and HUD copy to include Ember Charge and Companion Status.
- 6) Run syntax checks (`node --check`) and boot the page for a smoke test; adjust tuning values as needed.
