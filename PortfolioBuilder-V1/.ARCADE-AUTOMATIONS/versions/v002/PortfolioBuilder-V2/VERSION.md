# PortfolioBuilder V2

This is a runnable copied builder flow derived from `/Users/crimsonwheeler/Documents/GitHub/Portfolio/PortfolioBuilder-V1`.

## Purpose

- Run beside V1 as an additional automation target.
- Keep V1 unchanged while V2 tests stricter QA and deeper prompt rules.
- Promote only after evidence shows V2 produces better technical and gameplay-depth results than V1.
- If promoted, become the source copy for the next challenger, `v003`.

## Active Differences From V1

- `playwright-qa.py` fails when Start/Play/Begin does not produce visible canvas growth.
- `builder-agent.py` routes zero-growth canvas failures into the upgrade loop.
- `builder-orchestrator.py` requires implemented mechanics to stay aligned across story, design, runtime code, and validation.

## Automation Target

The central supervisor in V1 should run this copy through target id `arcade-builder-v002`.

## Promotion Lifecycle

V2 stays a challenger until its latest output beats V1. When it wins, the central automation should disable the V1 target, promote `latest.json` to `v002`, mark V2 as the active baseline, and create V3 from this V2 copy on the following improvement loop.
