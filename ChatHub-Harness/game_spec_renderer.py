"""Render a normalized game spec into self-contained browser output."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", str(text).lower()).strip("-")
    return slug[:56].strip("-") or "chathub-game"


def clamp_int(value: Any, default: int, lo: int, hi: int) -> int:
    try:
        return max(lo, min(hi, int(value)))
    except (TypeError, ValueError):
        return default


def clean_text(value: Any, default: str, limit: int = 140) -> str:
    if not isinstance(value, str):
        return default
    value = re.sub(r"\s+", " ", value).strip()
    return value[:limit] if value else default


def safe_color(value: Any, default: str) -> str:
    if isinstance(value, str) and re.fullmatch(r"#[0-9a-fA-F]{6}", value.strip()):
        return value.strip()
    return default


def title_from_prompt(prompt: str) -> str:
    body = prompt
    marker = re.search(r"(?im)^##\s+Prompt\s*$", prompt)
    if marker:
        body = prompt[marker.end():]
    called = re.search(r"called\s+([A-Z][A-Za-z0-9 ':\-]{2,60})", body)
    if called:
        return called.group(1).strip(" .'")
    for line in body.splitlines():
        line = line.strip("# -*\t")
        if len(line) > 8 and not line.lower().startswith(("workflow:", "mode:", "output:")):
            return line[:64]
    return "ChatHub Arcade Prototype"


def fallback_spec(prompt: str) -> dict[str, Any]:
    title = title_from_prompt(prompt)
    low = title.lower()
    if any(word in low for word in ["forest", "moss", "seed", "root"]):
        palette = {"background": "#06130d", "player": "#a8ffb0", "collectible": "#ffe58a", "hazard": "#ff6b6b", "accent": "#72f7c7"}
        collectible, hazard = "glow seeds", "thorn pulses"
    elif any(word in low for word in ["star", "sky", "orbit", "moon"]):
        palette = {"background": "#070914", "player": "#fff3a3", "collectible": "#8bd3ff", "hazard": "#ff5577", "accent": "#c9a7ff"}
        collectible, hazard = "star shards", "meteor ghosts"
    else:
        palette = {"background": "#090b10", "player": "#eef2ff", "collectible": "#8bd3ff", "hazard": "#ff5577", "accent": "#b8ff8b"}
        collectible, hazard = "data cores", "corruption fields"
    return {
        "title": title,
        "tagline": "A fresh ChatHub-built browser arcade prototype.",
        "objective": f"Collect {collectible}, avoid {hazard}, and survive the timer.",
        "playerName": "signal core",
        "collectibleName": collectible,
        "hazardName": hazard,
        "timerSeconds": 45,
        "goalScore": 120,
        "collectibleCount": 10,
        "hazardCount": 7,
        "playerSpeed": 900,
        "hazardSpeed": 95,
        "scorePerCollectible": 10,
        "backgroundPattern": "grid",
        "winText": "Signal restored.",
        "loseText": "Signal lost. Try again.",
        "palette": palette,
    }


def normalize_spec(raw: Any, prompt: str) -> dict[str, Any]:
    base = fallback_spec(prompt)
    source = raw if isinstance(raw, dict) else {}
    palette = base["palette"].copy()
    if isinstance(source.get("palette"), dict):
        for key in palette:
            palette[key] = safe_color(source["palette"].get(key), palette[key])
    title = clean_text(source.get("title"), base["title"], 72)
    spec = {
        "title": title,
        "slug": slugify(source.get("slug") or title),
        "tagline": clean_text(source.get("tagline"), base["tagline"], 140),
        "objective": clean_text(source.get("objective"), base["objective"], 220),
        "playerName": clean_text(source.get("playerName"), base["playerName"], 40),
        "collectibleName": clean_text(source.get("collectibleName"), base["collectibleName"], 40),
        "hazardName": clean_text(source.get("hazardName"), base["hazardName"], 40),
        "timerSeconds": clamp_int(source.get("timerSeconds"), base["timerSeconds"], 20, 120),
        "goalScore": clamp_int(source.get("goalScore"), base["goalScore"], 30, 500),
        "collectibleCount": clamp_int(source.get("collectibleCount"), base["collectibleCount"], 3, 25),
        "hazardCount": clamp_int(source.get("hazardCount"), base["hazardCount"], 1, 20),
        "playerSpeed": clamp_int(source.get("playerSpeed"), base["playerSpeed"], 450, 1600),
        "hazardSpeed": clamp_int(source.get("hazardSpeed"), base["hazardSpeed"], 30, 220),
        "scorePerCollectible": clamp_int(source.get("scorePerCollectible"), base["scorePerCollectible"], 1, 50),
        "backgroundPattern": clean_text(source.get("backgroundPattern"), base["backgroundPattern"], 20).lower(),
        "winText": clean_text(source.get("winText"), base["winText"], 90),
        "loseText": clean_text(source.get("loseText"), base["loseText"], 90),
        "palette": palette,
    }
    if spec["backgroundPattern"] not in {"grid", "stars", "rings", "cells"}:
        spec["backgroundPattern"] = "grid"
    return spec


def game_html(spec: dict[str, Any], summary: str) -> str:
    safe_title = html.escape(spec["title"])
    safe_tagline = html.escape(spec["tagline"])
    safe_objective = html.escape(spec["objective"])
    safe_collectible = html.escape(spec["collectibleName"])
    safe_hazard = html.escape(spec["hazardName"])
    safe_summary = html.escape(summary[:700])
    spec_json = json.dumps(spec, ensure_ascii=False)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>{safe_title}</title><style>html,body{{margin:0;height:100%;background:{spec['palette']['background']};color:#eef2ff;font-family:Inter,system-ui,Arial,sans-serif;overflow:hidden}}#wrap{{height:100%;display:grid;grid-template-rows:auto 1fr;background:radial-gradient(circle at 50% 16%,{spec['palette']['accent']}44,transparent 34%)}}header{{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px 18px;border-bottom:1px solid #ffffff1a;background:#05070acc;backdrop-filter:blur(10px)}}h1{{font-size:15px;margin:0;font-weight:900;letter-spacing:.08em;text-transform:uppercase}}.meta{{font-size:12px;color:#c8d2ea;max-width:55vw;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}canvas{{width:100%;height:100%;display:block}}#panel{{position:fixed;left:18px;bottom:18px;max-width:520px;padding:14px 16px;border:1px solid #ffffff22;background:#070a12df;border-radius:18px;box-shadow:0 20px 80px #0008}}#panel b{{color:#fff}}#panel p{{margin:.35rem 0;color:#bac5df;font-size:13px;line-height:1.35}}button{{background:#eef2ff;color:#05070a;border:0;border-radius:999px;padding:9px 14px;font-weight:900;cursor:pointer}}</style></head><body><div id="wrap"><header><h1>{safe_title}</h1><div class="meta">{safe_tagline}</div></header><canvas id="game"></canvas></div><div id="panel"><p><b>{safe_objective}</b></p><p>Move with WASD/arrows. Press Space for a pulse dash. Collect {safe_collectible}; avoid {safe_hazard}.</p><p>{safe_summary}</p><button id="start">Start / Restart</button></div><script>const SPEC={spec_json};const canvas=document.getElementById('game'),ctx=canvas.getContext('2d'),panel=document.getElementById('panel'),startBtn=document.getElementById('start');let w=0,h=0,keys={{}},running=false,last=0,score=0,time=SPEC.timerSeconds,pulse=0,cool=0,player,items,hazards,parts;function resize(){{w=canvas.width=innerWidth;h=canvas.height=innerHeight-48}}addEventListener('resize',resize);resize();addEventListener('keydown',e=>{{keys[e.key.toLowerCase()]=true;if(e.code==='Space'){{e.preventDefault();dash()}}}});addEventListener('keyup',e=>keys[e.key.toLowerCase()]=false);function rand(a,b){{return a+Math.random()*(b-a)}}function d(a,b){{return Math.hypot(a.x-b.x,a.y-b.y)}}function item(){{return{{x:rand(45,w-45),y:rand(45,h-45),r:9+Math.random()*5,spin:rand(0,7)}}}}function hz(i){{return{{x:rand(60,w-60),y:rand(60,h-60),r:14+i%4*3,vx:rand(-SPEC.hazardSpeed,SPEC.hazardSpeed),vy:rand(-SPEC.hazardSpeed,SPEC.hazardSpeed)}}}}function reset(){{running=true;score=0;time=SPEC.timerSeconds;pulse=0;cool=0;panel.style.display='none';player={{x:w*.5,y:h*.55,r:15,vx:0,vy:0}};items=Array.from({{length:SPEC.collectibleCount}},item);hazards=Array.from({{length:SPEC.hazardCount}},(_,i)=>hz(i));parts=[];last=performance.now();requestAnimationFrame(loop)}}startBtn.onclick=reset;function dash(){{if(!running||cool>0)return;pulse=.28;cool=7;burst(player.x,player.y,32,SPEC.palette.accent)}}function burst(x,y,n,c){{for(let i=0;i<n;i++)parts.push({{x,y,vx:rand(-210,210),vy:rand(-210,210),life:rand(.3,.9),c}})}}function bg(){{ctx.fillStyle=SPEC.palette.background;ctx.fillRect(0,0,w,h);ctx.strokeStyle='#ffffff12';ctx.lineWidth=1;if(SPEC.backgroundPattern==='rings'){{for(let r=60;r<Math.max(w,h);r+=70){{ctx.beginPath();ctx.arc(w/2,h/2,r,0,7);ctx.stroke()}}}}else if(SPEC.backgroundPattern==='stars'){{for(let i=0;i<115;i++){{ctx.fillStyle=i%3?'#ffffff18':SPEC.palette.accent+'66';ctx.fillRect((i*97)%w,(i*53)%h,2,2)}}}}else{{for(let x=0;x<w;x+=48){{ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,h);ctx.stroke()}}for(let y=0;y<h;y+=48){{ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(w,y);ctx.stroke()}}}}}}function update(dt){{time-=dt;cool=Math.max(0,cool-dt);pulse=Math.max(0,pulse-dt);let boost=pulse>0?1.9:1,ax=(keys.d||keys.arrowright?1:0)-(keys.a||keys.arrowleft?1:0),ay=(keys.s||keys.arrowdown?1:0)-(keys.w||keys.arrowup?1:0);player.vx=(player.vx+ax*SPEC.playerSpeed*boost*dt)*.86;player.vy=(player.vy+ay*SPEC.playerSpeed*boost*dt)*.86;player.x=Math.max(player.r,Math.min(w-player.r,player.x+player.vx*dt));player.y=Math.max(player.r,Math.min(h-player.r,player.y+player.vy*dt));for(const z of hazards){{z.x+=z.vx*dt;z.y+=z.vy*dt;if(z.x<z.r||z.x>w-z.r)z.vx*=-1;if(z.y<z.r||z.y>h-z.r)z.vy*=-1}}items=items.filter(c=>{{c.spin+=dt*4;if(d(player,c)<player.r+c.r){{score+=SPEC.scorePerCollectible;burst(c.x,c.y,18,SPEC.palette.collectible);return false}}return true}});while(items.length<SPEC.collectibleCount)items.push(item());for(const z of hazards){{if(d(player,z)<player.r+z.r){{score=Math.max(0,score-Math.ceil(SPEC.scorePerCollectible*1.5));burst(player.x,player.y,30,SPEC.palette.hazard);player.x=w*.5;player.y=h*.55;player.vx=0;player.vy=0}}}parts.forEach(p=>{{p.x+=p.vx*dt;p.y+=p.vy*dt;p.life-=dt}});parts=parts.filter(p=>p.life>0)}}function draw(){{bg();for(const c of items){{ctx.save();ctx.translate(c.x,c.y);ctx.rotate(c.spin);ctx.fillStyle=SPEC.palette.collectible;ctx.shadowColor=SPEC.palette.collectible;ctx.shadowBlur=18;ctx.fillRect(-c.r,-c.r,c.r*2,c.r*2);ctx.restore();ctx.shadowBlur=0}}for(const z of hazards){{ctx.beginPath();ctx.strokeStyle=SPEC.palette.hazard;ctx.lineWidth=3;ctx.arc(z.x,z.y,z.r,0,7);ctx.stroke();ctx.fillStyle=SPEC.palette.hazard+'55';ctx.beginPath();ctx.arc(z.x,z.y,z.r*.45,0,7);ctx.fill()}}for(const p of parts){{ctx.globalAlpha=Math.max(0,p.life);ctx.fillStyle=p.c;ctx.fillRect(p.x,p.y,3,3);ctx.globalAlpha=1}}ctx.beginPath();ctx.fillStyle=SPEC.palette.player;ctx.shadowColor=SPEC.palette.player;ctx.shadowBlur=pulse>0?34:20;ctx.arc(player.x,player.y,player.r+(pulse>0?6:0),0,7);ctx.fill();ctx.shadowBlur=0;ctx.fillStyle='#eef2ff';ctx.font='800 16px system-ui';ctx.fillText('Score '+score+' / '+SPEC.goalScore,18,28);ctx.fillText('Time '+Math.max(0,time).toFixed(1),18,52);ctx.fillText('Pulse '+(cool<=0?'READY':cool.toFixed(1)),18,76)}}function loop(t){{if(!running)return;let dt=Math.min(.033,(t-last)/1000||.016);last=t;update(dt);draw();if(score>=SPEC.goalScore)return end(true);if(time<=0)return end(false);requestAnimationFrame(loop)}}function end(win){{running=false;panel.style.display='block';panel.querySelector('p').innerHTML='<b>'+(win?SPEC.winText:SPEC.loseText)+'</b> Final score: '+score+'.'}};</script></body></html>"""


def write_outputs(out_dir: Path, spec: dict[str, Any], result_md: str, model: str, status: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    page = game_html(spec, result_md)
    slug = spec["slug"]
    (out_dir / "latest-game.html").write_text(page, encoding="utf-8")
    game_dir = out_dir / "games" / slug
    game_dir.mkdir(parents=True, exist_ok=True)
    (game_dir / "index.html").write_text(page, encoding="utf-8")
    (out_dir / "generated-game-spec.json").write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
    repo_latest = "ChatHub-Harness/outbox/latest-game.html"
    repo_archived = f"ChatHub-Harness/outbox/games/{slug}/index.html"
    links = f"""# ChatHub Play Links

status: {status}
model: {model}
game: {spec['title']}
slug: {slug}

## Public Pages

- Public root: https://thecrimsondeveloper.github.io/Portfolio/
- Latest game: https://thecrimsondeveloper.github.io/Portfolio/{repo_latest}
- Archived game: https://thecrimsondeveloper.github.io/Portfolio/{repo_archived}

## GitHub Review

- Latest game source: https://github.com/thecrimsondeveloper/Portfolio/blob/ChatHub-Output/{repo_latest}
- Archived game source: https://github.com/thecrimsondeveloper/Portfolio/blob/ChatHub-Output/{repo_archived}
- Game spec: https://github.com/thecrimsondeveloper/Portfolio/blob/ChatHub-Output/ChatHub-Harness/outbox/generated-game-spec.json
"""
    (out_dir / "latest-links.md").write_text(links, encoding="utf-8")
