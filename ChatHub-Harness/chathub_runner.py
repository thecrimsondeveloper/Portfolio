#!/usr/bin/env python3
"""Run one ChatHub-Harness workflow from committed direction files.

Dependency-free on purpose: GitHub Actions can run this with plain Python.
The runner always emits reviewable outbox files, even when the model call is
blocked or unavailable.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import textwrap
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
DEFAULT_WORKFLOW = ROOT / "workflows" / "game-build.workflow.json"
DEFAULT_DIRECTION = ROOT / "directions" / "current-direction.md"
DEFAULT_OUT = ROOT / "outbox" / "latest-result.md"
DEFAULT_LESSONS = ROOT / "lessons" / "harness-lessons.md"
DEFAULT_BASE_URL = "https://integrate.api.nvidia.com/v1"
DEFAULT_MODEL = "mistralai/mixtral-8x7b-instruct-v0.1"
DEFAULT_FREE_MODEL_ALLOWLIST = {
    DEFAULT_MODEL,
    "nvidia/nemotron-3-ultra-550b-a55b",
    "moonshotai/kimi-k2.6",
    "deepseek-ai/deepseek-v4-pro",
    "zai/glm-5.1",
}


def now_stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def env_or_default(name: str, default: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        return default
    return value.strip()


def read_text(path: Path, fallback: str = "") -> str:
    return path.read_text(encoding="utf-8") if path.exists() else fallback


def load_workflow(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"workflow missing: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SystemExit(f"workflow JSON invalid: {path}: {error}") from error
    if not isinstance(data, dict):
        raise SystemExit(f"workflow root must be an object: {path}")
    return data


def endpoint_config(workflow: dict[str, Any]) -> dict[str, Any]:
    endpoint = workflow.get("endpoint") or {}
    base_url_env = endpoint.get("baseUrlEnv", "NVIDIA_API_BASE_URL")
    model_env = endpoint.get("modelEnv", "NVIDIA_MODEL")
    api_key_env = endpoint.get("apiKeyEnv", "NVIDIA_API_KEY")
    return {
        "base_url": env_or_default(base_url_env, endpoint.get("defaultBaseUrl", DEFAULT_BASE_URL)).rstrip("/"),
        "model": env_or_default(model_env, endpoint.get("defaultModel", DEFAULT_MODEL)),
        "api_key_env": api_key_env,
        "api_key": os.getenv(api_key_env, "").strip(),
        "free_only": env_or_default("NVIDIA_FREE_ENDPOINTS_ONLY", "true").lower() not in {"0", "false", "no"},
    }


def configured_free_model_allowlist() -> set[str]:
    raw = os.getenv("NVIDIA_FREE_MODEL_ALLOWLIST", "")
    configured = {item.strip() for item in raw.split(",") if item.strip()}
    return configured or set(DEFAULT_FREE_MODEL_ALLOWLIST)


def free_endpoint_blocker(config: dict[str, Any]) -> str | None:
    if not config.get("free_only"):
        return None
    allowlist = configured_free_model_allowlist()
    if config.get("model") not in allowlist:
        return (
            f"Free-endpoint guard blocked model `{config.get('model')}`. "
            f"Allowed free endpoint models: {', '.join(sorted(allowlist))}."
        )
    return None


def list_steps(workflow: dict[str, Any]) -> str:
    steps = workflow.get("linearSteps") or []
    return "\n".join(f"- {s.get('id', 'step')}: {s.get('goal', '').strip()}" for s in steps) or "- no steps declared"


def list_items(workflow: dict[str, Any], key: str, fallback: str) -> str:
    items = workflow.get(key) or []
    return "\n".join(f"- {item}" for item in items) or f"- {fallback}"


def build_prompt(workflow: dict[str, Any], direction: str, lessons: str) -> list[dict[str, str]]:
    system = textwrap.dedent(
        """
        You are ChatHub-Harness, a linear workflow runner for a portfolio and game-building repository.
        Follow the workflow steps in order. Produce a reviewable artifact. Do not claim files were edited.
        Extract durable lessons separately from temporary observations. Keep output concise and operational.
        Focus game outputs on small playable browser games, shared Arcade patterns, and validation steps.
        """
    ).strip()
    user = f"""Workflow: {workflow.get('title', workflow.get('id', 'unnamed workflow'))}
Workflow intent:
{workflow.get('intent', '(none)')}

Linear steps:
{list_steps(workflow)}

Output contract:
{list_items(workflow, 'outputContract', 'markdown result')}

Constraints:
{list_items(workflow, 'constraints', 'stay bounded')}

Committed direction:
{direction.strip() or '(empty direction file)'}

Existing lessons:
{lessons[-6000:].strip() or '(no lessons yet)'}

Return the requested markdown artifact only.
"""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def call_nvidia_chat(config: dict[str, Any], messages: list[dict[str, str]], timeout: int) -> str:
    request = urllib.request.Request(
        f"{config['base_url']}/chat/completions",
        data=json.dumps(
            {
                "model": config["model"],
                "messages": messages,
                "temperature": 0.3,
                "top_p": 1,
                "max_tokens": 2048,
                "stream": False,
            }
        ).encode("utf-8"),
        headers={"Authorization": f"Bearer {config['api_key']}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"endpoint HTTP {error.code}: {body[:1200]}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"endpoint connection failed: {error}") from error
    try:
        data = json.loads(raw)
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"endpoint returned unexpected response: {raw[:1200]}") from error
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError(f"endpoint returned empty assistant content: {raw[:1200]}")
    return content.strip()


def slugify(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")[:44] or "chathub-playtest"


def direction_title(direction: str, workflow: dict[str, Any]) -> str:
    for line in direction.splitlines():
        clean = line.strip("# -\t ")
        if clean:
            return clean[:80]
    return str(workflow.get("title") or "ChatHub Playtest")


def blocked_result(workflow: dict[str, Any], config: dict[str, Any], reason: str) -> str:
    return f"""# ChatHub Result

status: blocked
time: {now_stamp()}
workflow: {workflow.get('id', 'unknown')}
model: {config.get('model', '')}
base_url: {config.get('base_url', '')}
free_only: {config.get('free_only')}

## Blocker

{reason}

## Playable Output

A deterministic fallback playable HTML file was still emitted for review:

```text
ChatHub-Harness/outbox/latest-game.html
```

## Next Fix

Check `NVIDIA_API_KEY`, `NVIDIA_MODEL`, `NVIDIA_API_BASE_URL`, and `NVIDIA_FREE_MODEL_ALLOWLIST`, then rerun the workflow.
"""


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>__TITLE__ | ChatHub Playtest</title>
<style>
html,body{margin:0;height:100%;background:#090b10;color:#eef2ff;font-family:Inter,system-ui,Arial,sans-serif;overflow:hidden}
#wrap{height:100%;display:grid;grid-template-rows:auto 1fr;background:radial-gradient(circle at 50% 20%,#26314d,#090b10 62%)}
header{display:flex;gap:16px;align-items:center;justify-content:space-between;padding:14px 18px;border-bottom:1px solid #ffffff1a;background:#05070acc;backdrop-filter:blur(10px)}
h1{font-size:15px;margin:0;font-weight:700;letter-spacing:.08em;text-transform:uppercase}.meta{font-size:12px;color:#aab6d3;max-width:55vw;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
canvas{width:100%;height:100%;display:block}#panel{position:fixed;left:18px;bottom:18px;max-width:440px;padding:14px 16px;border:1px solid #ffffff22;background:#070a12d9;border-radius:18px;box-shadow:0 20px 80px #0008}
#panel b{color:#fff}#panel p{margin:.35rem 0;color:#bac5df;font-size:13px;line-height:1.35}button{background:#eef2ff;color:#05070a;border:0;border-radius:999px;padding:9px 14px;font-weight:800;cursor:pointer}
</style>
</head>
<body>
<div id="wrap"><header><h1>__TITLE__</h1><div class="meta">ChatHub status: __STATUS__ · model: __MODEL__</div></header><canvas id="game"></canvas></div>
<div id="panel"><p><b>Signal Salvage.</b> Move with WASD/arrow keys. Collect blue data cores, avoid red corruption fields, survive the timer.</p><p>__SUMMARY__</p><button id="start">Start / Restart</button></div>
<script>
const canvas=document.getElementById('game'),ctx=canvas.getContext('2d'),panel=document.getElementById('panel'),startBtn=document.getElementById('start');
let w=0,h=0,keys={},running=false,last=0,score=0,time=45,player,cores,hazards,particles;
function resize(){w=canvas.width=innerWidth;h=canvas.height=innerHeight-48} addEventListener('resize',resize);resize();
addEventListener('keydown',e=>keys[e.key.toLowerCase()]=true); addEventListener('keyup',e=>keys[e.key.toLowerCase()]=false);
function rand(a,b){return a+Math.random()*(b-a)}
function reset(){running=true;score=0;time=45;panel.style.display='none';player={x:w*.5,y:h*.55,r:15,vx:0,vy:0};cores=Array.from({length:9},()=>({x:rand(40,w-40),y:rand(40,h-40),r:9}));hazards=Array.from({length:7},(_,i)=>({x:rand(50,w-50),y:rand(50,h-50),r:16+i%3*4,vx:rand(-90,90),vy:rand(-80,80)}));particles=[];last=performance.now();requestAnimationFrame(loop)}
startBtn.onclick=reset; function burst(x,y,n){for(let i=0;i<n;i++)particles.push({x,y,vx:rand(-180,180),vy:rand(-180,180),life:rand(.35,.8)})}
function loop(t){if(!running)return;let dt=Math.min(.033,(t-last)/1000||.016);last=t;time-=dt;let ax=(keys.d||keys.arrowright?1:0)-(keys.a||keys.arrowleft?1:0),ay=(keys.s||keys.arrowdown?1:0)-(keys.w||keys.arrowup?1:0);player.vx=(player.vx+ax*900*dt)*.86;player.vy=(player.vy+ay*900*dt)*.86;player.x=Math.max(player.r,Math.min(w-player.r,player.x+player.vx*dt));player.y=Math.max(player.r,Math.min(h-player.r,player.y+player.vy*dt));for(const hz of hazards){hz.x+=hz.vx*dt;hz.y+=hz.vy*dt;if(hz.x<hz.r||hz.x>w-hz.r)hz.vx*=-1;if(hz.y<hz.r||hz.y>h-hz.r)hz.vy*=-1}cores=cores.filter(c=>{let d=Math.hypot(c.x-player.x,c.y-player.y);if(d<c.r+player.r){score+=10;burst(c.x,c.y,16);return false}return true});while(cores.length<9)cores.push({x:rand(40,w-40),y:rand(40,h-40),r:9});for(const hz of hazards){if(Math.hypot(hz.x-player.x,hz.y-player.y)<hz.r+player.r){score=Math.max(0,score-15);burst(player.x,player.y,28);player.x=w*.5;player.y=h*.55}}particles.forEach(p=>{p.x+=p.vx*dt;p.y+=p.vy*dt;p.life-=dt});particles=particles.filter(p=>p.life>0);draw();if(time<=0)end();else requestAnimationFrame(loop)}
function draw(){ctx.clearRect(0,0,w,h);ctx.fillStyle='#090b10';ctx.fillRect(0,0,w,h);ctx.strokeStyle='#ffffff12';ctx.lineWidth=1;for(let x=0;x<w;x+=48){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,h);ctx.stroke()}for(let y=0;y<h;y+=48){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(w,y);ctx.stroke()}for(const c of cores){ctx.beginPath();ctx.fillStyle='#8bd3ff';ctx.shadowColor='#8bd3ff';ctx.shadowBlur=18;ctx.arc(c.x,c.y,c.r,0,7);ctx.fill();ctx.shadowBlur=0}for(const hz of hazards){ctx.beginPath();ctx.strokeStyle='#ff5577';ctx.lineWidth=3;ctx.arc(hz.x,hz.y,hz.r,0,7);ctx.stroke()}for(const p of particles){ctx.globalAlpha=Math.max(0,p.life);ctx.fillStyle='#eef2ff';ctx.fillRect(p.x,p.y,3,3);ctx.globalAlpha=1}ctx.beginPath();ctx.fillStyle='#eef2ff';ctx.shadowColor='#eef2ff';ctx.shadowBlur=20;ctx.arc(player.x,player.y,player.r,0,7);ctx.fill();ctx.shadowBlur=0;ctx.fillStyle='#eef2ff';ctx.font='700 16px system-ui';ctx.fillText('Score '+score,18,28);ctx.fillText('Time '+Math.max(0,time).toFixed(1),18,52)}
function end(){running=false;panel.style.display='block';panel.querySelector('p').innerHTML='<b>Run complete.</b> Final score: '+score+'. Start again or review the harness output.'}
</script>
</body>
</html>
"""


def write_playable_outputs(out_path: Path, workflow: dict[str, Any], direction: str, model_result: str, config: dict[str, Any], status: str) -> None:
    out_dir = out_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    title = direction_title(direction, workflow)
    slug = slugify(title)
    safe = {
        "__TITLE__": html.escape(title),
        "__MODEL__": html.escape(config.get("model", "unknown")),
        "__STATUS__": html.escape(status),
        "__SUMMARY__": html.escape((model_result or direction or "ChatHub generated playtest")[:900]),
    }
    page = HTML_TEMPLATE
    for key, value in safe.items():
        page = page.replace(key, value)
    (out_dir / "latest-game.html").write_text(page, encoding="utf-8")
    repo_path = "ChatHub-Harness/outbox/latest-game.html"
    (out_dir / "latest-links.md").write_text(
        f"""# ChatHub Play Links

status: {status}
time: {now_stamp()}
slug: {slug}

## Play / Review

- GitHub file: https://github.com/thecrimsondeveloper/Portfolio/blob/ChatHub-Output/{repo_path}
- HTML preview: https://htmlpreview.github.io/?https://github.com/thecrimsondeveloper/Portfolio/blob/ChatHub-Output/{repo_path}

## Output Files

```text
ChatHub-Harness/outbox/latest-result.md
ChatHub-Harness/outbox/latest-game.html
ChatHub-Harness/outbox/latest-links.md
```
""",
        encoding="utf-8",
    )


def write_result(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one ChatHub-Harness workflow")
    parser.add_argument("--workflow", type=Path, default=DEFAULT_WORKFLOW)
    parser.add_argument("--direction", type=Path, default=DEFAULT_DIRECTION)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--lessons", type=Path, default=DEFAULT_LESSONS)
    parser.add_argument("--require-key", action="store_true")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()

    workflow = load_workflow(args.workflow)
    direction = read_text(args.direction)
    lessons = read_text(args.lessons)
    config = endpoint_config(workflow)

    blocker = free_endpoint_blocker(config)
    if blocker:
        result = blocked_result(workflow, config, blocker)
        write_result(args.out, result)
        write_playable_outputs(args.out, workflow, direction, result, config, "blocked-free-endpoint-guard")
        print(f"ChatHub-Harness blocked: {blocker}")
        return 1 if args.require_key else 0

    if not config["api_key"]:
        result = blocked_result(workflow, config, f"Missing `{config['api_key_env']}`.")
        write_result(args.out, result)
        write_playable_outputs(args.out, workflow, direction, result, config, "blocked-missing-key")
        print(f"ChatHub-Harness blocked: missing {config['api_key_env']}")
        return 1 if args.require_key else 0

    try:
        content = call_nvidia_chat(config, build_prompt(workflow, direction, lessons), args.timeout)
        result = f"""<!-- generated by ChatHub-Harness at {now_stamp()} -->
<!-- workflow: {workflow.get('id', 'unknown')} -->
<!-- model: {config.get('model', '')} -->
<!-- free_only: {config.get('free_only')} -->

{content}
"""
        status = "completed"
    except RuntimeError as error:
        result = blocked_result(workflow, config, str(error))
        status = "blocked-endpoint-error"
        print(f"ChatHub-Harness blocked: {error}")

    write_result(args.out, result)
    write_playable_outputs(args.out, workflow, direction, result, config, status)
    print(f"ChatHub-Harness wrote outbox: {args.out.parent}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
