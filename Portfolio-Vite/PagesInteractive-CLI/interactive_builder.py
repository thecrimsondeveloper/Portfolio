#!/usr/bin/env python3
import argparse
import json
import os
import random
import re
import sys
import textwrap
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES_ROOT = ROOT / "Pages"
SEED_FILE = PAGES_ROOT / "arcade-seed.json"
NON_INTERACTIVE_MODE = False


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "new-game"


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def load_seed_data() -> dict:
    with open(SEED_FILE, "r", encoding="utf-8") as handle:
        return json.load(handle)


def sample_combination(seed: dict) -> dict:
    options = seed.get("options", {})
    rules = seed.get("randomGenerator", {}).get("sampleRules", {})
    combination = {}

    for key, count in rules.items():
        items = options.get(key, [])
        if not items:
            continue

        if count == 1:
            combination[key] = random.choice(items)
        else:
            sample_count = min(count, len(items))
            combination[key] = random.sample(items, sample_count)

    return combination


def format_combination(combination: dict) -> str:
    lines = ["Generated game seed combination:"]
    for key, value in combination.items():
        label = key.replace("camel", " ").replace("Motivations", " motivations").replace("Loops", " loops")
        label = re.sub(r"([a-z])([A-Z])", r"\1 \2", label).capitalize()
        if isinstance(value, list):
            value = ", ".join(value)
        lines.append(f"- {label}: {value}")
    return "\n".join(lines)


def build_game_engineer_prompt(content: str) -> str:
    return textwrap.dedent(f"""
    You are a game engineering expert.
    Rewrite the architecture and design patterns in the current file to fit the game idea better.
    Prioritize reusable, data-driven game systems, clear separation of concerns, and a robust playable engine structure.

    {content}
    """)


def call_nvidia_ai(prompt: str) -> str:
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        raise EnvironmentError("NVIDIA_API_KEY is not set in the environment.")

    prompt = build_game_engineer_prompt(prompt)
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    payload = {
        "model": "mistralai/mixtral-8x7b-instruct-v0.1",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "top_p": 1,
        "max_tokens": 512,
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    last_error = None
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                response_data = json.load(response)
            break
        except urllib.error.HTTPError as exc:
            last_error = f"HTTP {exc.code}: {exc.reason}"
        except urllib.error.URLError as exc:
            last_error = str(exc.reason)
        except json.JSONDecodeError as exc:
            last_error = f"Invalid JSON response: {exc}"

        if attempt < 3:
            time.sleep(attempt * 2)
            continue
        print(f"NVIDIA AI request failed after {attempt} attempts: {last_error}")
        return f"(NVIDIA AI unavailable; placeholder generated for prompt: {prompt[:80]})"

    choice = response_data.get("choices", [{}])[0]
    message = choice.get("message", {})
    text = message.get("content") or choice.get("delta", {}).get("content")
    return (text or "").strip() or f"(NVIDIA AI returned no text for prompt: {prompt[:80]})"


def prompt_multiline(prompt: str, sentinel: str = "END", auto_fill: bool = False) -> str:
    if auto_fill and NON_INTERACTIVE_MODE:
        print("Auto-fill non-interactive mode: generating content with NVIDIA AI...")
        return call_nvidia_ai(prompt)

    print("\n" + prompt)
    print(f"Enter text below. Finish by typing '{sentinel}' on its own line.")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            line = sentinel
        if line.strip() == sentinel:
            break
        lines.append(line)
    value = "\n".join(lines).strip()
    if not value and auto_fill:
        print("No input provided; using NVIDIA AI to generate content...")
        return call_nvidia_ai(prompt)
    return value


def prompt_short(prompt: str, default: str = "", auto_fill: bool = False) -> str:
    if default:
        prompt_text = f"{prompt} [{default}]: "
    else:
        prompt_text = f"{prompt}: "
    try:
        value = input(prompt_text).strip()
    except EOFError:
        value = ""
    if value:
        return value
    if default:
        return default
    if auto_fill:
        print("No input provided; using NVIDIA AI to generate content...")
        return call_nvidia_ai(prompt)
    return ""


def prompt_yes_no_ai(prompt: str, default: str = "yes", auto_fill: bool = False, auto_decide: bool = False) -> str:
    normalized_default = "yes" if default.lower() in {"yes", "y", "1"} else "no"
    default_label = "1" if normalized_default == "yes" else "2"
    option_text = f"{prompt} [1=yes, 2=no, 3=ask AI] [{default_label}]: "

    def parse_choice(value: str):
        value = value.strip().lower()
        if not value:
            value = default_label
        if value in {"1", "yes", "y"}:
            return "yes"
        if value in {"2", "no", "n"}:
            return "no"
        if value in {"3", "ask", "ai", "ask ai"}:
            return "ai"
        return None

    if auto_decide or (auto_fill and not sys.stdin.isatty()):
        choice = "3"
        print(f"{option_text} (auto-decide)")
    else:
        try:
            choice = input(option_text).strip().lower()
        except EOFError:
            choice = ""

    normalized = parse_choice(choice)
    if normalized is None:
        print("Invalid choice. Please type 1, 2, or 3.")
        return prompt_yes_no_ai(prompt, default=default, auto_fill=auto_fill, auto_decide=auto_decide)

    if normalized == "ai" or (auto_fill and not choice):
        print("Using NVIDIA AI to decide...")
        ai_prompt = textwrap.dedent(f"""
        Decide yes or no for the following question.
        Answer with only 1 or 2.

        Question: {prompt}

        1: yes
        2: no
        """)
        ai_result = call_nvidia_ai(ai_prompt)
        ai_choice = parse_choice(ai_result)
        if ai_choice in {"yes", "no"}:
            return ai_choice
        # Fallback if AI did not produce a clean answer
        print("NVIDIA AI did not return a clear 1 or 2. Defaulting to yes.")
        return "yes"

    return normalized


def make_safe_filename(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9 \-]+", "", text)
    text = text.strip().replace(" ", "-").lower()
    return text[:80] or "chapter"


def ensure_target_directory(folder_name: str, force: bool = False) -> Path:
    target_dir = PAGES_ROOT / folder_name
    if target_dir.exists() and any(target_dir.iterdir()):
        if not force:
            print(f"Warning: target directory '{target_dir}' already exists and is not empty.")
            confirm = input("Type 'yes' to continue and overwrite files inside, or press Enter to cancel: ").strip().lower()
            if confirm != "yes":
                raise SystemExit("Canceled by user.")
    else:
        target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir


def write_text_file(path: Path, content: str) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)


def write_json_file(path: Path, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def create_design_file(target_dir: Path, design_text: str) -> None:
    design_path = target_dir / "DESIGN.md"
    content = textwrap.dedent(f"""
    # DESIGN

    {design_text}
    """)
    write_text_file(design_path, content)
    print(f"Saved design spec to {design_path}")


def create_seed_choice_file(target_dir: Path, combination: dict) -> None:
    seed_path = target_dir / "seed-choice.json"
    write_json_file(seed_path, combination)
    print(f"Saved chosen seed payload to {seed_path}")


def create_ideation_file(target_dir: Path, title: str, combination: dict, expansion_text: str) -> None:
    ideation_path = target_dir / "IDEATION.md"
    content = textwrap.dedent(f"""
    # IDEATION

    ## {title}

    ### Seed Summary
    {format_combination(combination)}

    ### Expansion Ideas
    {expansion_text}

    Use these expansion ideas as the basis for a fully comprehensive game idea that will be captured in DESIGN.md.
    """)
    write_text_file(ideation_path, content)
    print(f"Saved ideation notes to {ideation_path}")


def create_implementation_chapters(target_dir: Path, chapters_text: str) -> None:
    implementation_dir = target_dir / "implementation"
    implementation_dir.mkdir(parents=True, exist_ok=True)
    chapter_lines = [line.strip() for line in chapters_text.splitlines() if line.strip()]

    if not chapter_lines:
        chapter_lines = [
            "Game setup and core loop",
            "Movement and player controls",
            "Progression systems",
            "Completion and reward flow",
            "Story / narrative integration"
        ]
        print("No chapters were entered, so default implementation chapters were created.")

    for index, chapter in enumerate(chapter_lines, start=1):
        filename = f"{index:02d}-{make_safe_filename(chapter)}.md"
        chapter_path = implementation_dir / filename
        write_text_file(chapter_path, f"# {chapter}\n\nWrite the implementation plan for this chapter here.\n")
        print(f"Created implementation chapter {chapter_path}")

    index_path = implementation_dir / "README.md"
    index_content = "# Implementation Chapters\n\n" + "\n".join(
        f"- [{chapter}](./{index:02d}-{make_safe_filename(chapter)}.md)" for index, chapter in enumerate(chapter_lines, start=1)
    )
    write_text_file(index_path, index_content)
    print(f"Created implementation index at {index_path}")


def scan_existing_pages() -> list[dict]:
    pages = []
    for child in PAGES_ROOT.iterdir():
        if not child.is_dir():
            continue
        existing = {"folder": child.name, "title": None, "description": None}
        story_file = child / "story-structure.json"
        if story_file.exists():
            try:
                with open(story_file, "r", encoding="utf-8") as handle:
                    data = json.load(handle)
                existing["title"] = data.get("title")
                existing["description"] = data.get("description")
            except Exception:
                pass
        if not existing["title"]:
            design_file = child / "DESIGN.md"
            if design_file.exists():
                try:
                    lines = design_file.read_text(encoding="utf-8").splitlines()
                    if lines:
                        existing["title"] = lines[0].lstrip("# ").strip()
                        if len(lines) > 1:
                            existing["description"] = lines[1].strip()
                except Exception:
                    pass
        if existing["title"] or existing["description"]:
            pages.append(existing)
    return pages


def similarity_score(text_a: str, text_b: str) -> float:
    a_words = set(re.findall(r"[a-z]{4,}", text_a.lower()))
    b_words = set(re.findall(r"[a-z]{4,}", text_b.lower()))
    if not a_words or not b_words:
        return 0.0
    common = a_words & b_words
    return len(common) / max(len(a_words), len(b_words))


def find_similar_pages(title: str, description: str, pages: list[dict]) -> list[dict]:
    candidates = []
    source_text = f"{title} {description}".lower()
    for page in pages:
        existing_text = "".join(filter(None, [page.get("title", ""), page.get("description", "")]))
        score = similarity_score(source_text, existing_text)
        if score >= 0.15:
            candidates.append({"folder": page["folder"], "title": page.get("title"), "description": page.get("description"), "score": score})
    return sorted(candidates, key=lambda item: item["score"], reverse=True)


def confirm_unique_idea(title: str, description: str, pages: list[dict], auto_confirm: bool = False, auto_fill: bool = False, auto_decide: bool = False) -> bool:
    similar = find_similar_pages(title, description, pages)
    if not similar:
        return True
    print("\nExisting Pages with potentially similar ideas:")
    for item in similar[:5]:
        print(f"- {item['folder']}: {item['title']} — {item['description']} (similarity {item['score']:.2f})")
    if auto_confirm:
        print("Auto-confirming idea uniqueness in non-interactive mode.")
        return True
    decision = prompt_yes_no_ai(
        "Does this idea look unique enough?",
        default="yes",
        auto_fill=auto_fill,
        auto_decide=auto_decide,
    )
    return decision == "yes"


def format_fun_needs_for_markdown(fun_needs: str) -> str:
    if not fun_needs.strip():
        return "- (No fun checklist items provided yet.)"
    lines = [line.strip() for line in fun_needs.splitlines() if line.strip()]
    return "\n" + "\n".join(f"- {line.lstrip('- ').strip()}" for line in lines)


def append_fun_section_to_design(design_text: str, assessment: str, fun_needs: str) -> str:
    fun_section = textwrap.dedent(f"""
    ## Fun game assessment

    - Assessment: {assessment}

    ### Things needed to make this game fun
    {format_fun_needs_for_markdown(fun_needs)}
    """)
    return design_text.rstrip() + "\n\n" + fun_section.strip() + "\n"


def create_fun_check_file(target_dir: Path, assessment: str, fun_needs: str) -> None:
    fun_path = target_dir / "FUN-CHECK.md"
    content = textwrap.dedent(f"""
    # FUN CHECK

    **Is this a fun game?**
    {assessment}

    **Things needed to make this game fun:**
    {format_fun_needs_for_markdown(fun_needs)}
    """)
    write_text_file(fun_path, content)
    print(f"Saved fun checklist to {fun_path}")


def create_story_json(target_dir: Path, folder_name: str, title: str, description: str, combination: dict, design_text: str, chapters_text: str, fun_assessment: str, fun_needs: str) -> None:
    story_path = target_dir / "story-structure.json"
    scene_data = {
        "ground": {
            "width": 60,
            "depth": 60,
            "color": "#121a2a"
        },
        "player": {
            "start": {"x": 0, "y": 0.5, "z": 10},
            "size": {"x": 1, "y": 1, "z": 1},
            "color": "#8bd8ff",
            "speed": 4.0
        },
        "goal": {
            "position": {"x": 0, "y": 0.1, "z": -12},
            "size": {"x": 3, "y": 0.2, "z": 3},
            "color": "#6cff8a"
        },
        "obstacles": [
            {"position": {"x": -6, "y": 1, "z": -2}, "size": {"x": 3, "y": 2, "z": 3}, "color": "#ff8a5c"},
            {"position": {"x": 6, "y": 1, "z": -6}, "size": {"x": 3, "y": 2, "z": 3}, "color": "#ff8a5c"},
            {"position": {"x": 0, "y": 1, "z": -8}, "size": {"x": 3, "y": 2, "z": 3}, "color": "#ff8a5c"}
        ],
        "camera": {
            "offset": {"x": 0, "y": 8, "z": 16}
        },
        "rules": {
            "goalRadius": 1.5,
            "statusMessage": "Reach the green goal area."
        }
    }
    story_template = {
        "id": folder_name,
        "title": title,
        "description": description,
        "seed": combination,
        "fun": {
            "assessment": fun_assessment,
            "needs": [line.lstrip("- ").strip() for line in fun_needs.splitlines() if line.strip()]
        },
        "design": {
            "summary": design_text.splitlines()[0] if design_text else "",
            "details": design_text,
            "chapters": [line.strip() for line in chapters_text.splitlines() if line.strip()]
        },
        "scene": scene_data,
        "story": {
            "start": "intro",
            "nodes": [
                {
                    "id": "intro",
                    "title": "Introduction",
                    "text": "Describe the opening scene here.",
                    "choices": []
                }
            ]
        },
        "delivery": {
            "format": "story-driven JSON nodes",
            "note": "Add fields for choices, transitions, and implementation mapping as needed."
        }
    }
    write_json_file(story_path, story_template)
    print(f"Created story structure JSON at {story_path}")


def create_html_file(target_dir: Path, title: str, description: str) -> None:
    html_path = target_dir / "index.html"
    content = textwrap.dedent(f"""
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>{title}</title>
        <style>
          body {{ margin: 0; font-family: system-ui, sans-serif; background: #080b12; color: #fff; }}
          .page-shell {{ display: flex; flex-direction: column; min-height: 100vh; }}
          header {{ padding: 1rem 1.5rem; background: #0f1728; border-bottom: 1px solid #223051; }}
          h1 {{ margin: 0; font-size: 1.75rem; }}
          .meta {{ margin-top: 0.5rem; color: #8ca6d9; }}
          #game-container {{ position: relative; flex: 1; min-height: 60vh; background: #090d1a; }}
          #game-canvas {{ width: 100%; height: 100%; display: block; }}
          #game-ui {{ position: absolute; top: 1rem; left: 1rem; padding: 0.75rem 1rem; background: rgba(0,0,0,0.55); border-radius: 14px; color: #d5e0ff; max-width: 320px; }}
          #story-summary {{ margin: 1rem auto; max-width: 960px; padding: 1rem; background: #10172d; border: 1px solid #1f3158; border-radius: 16px; }}
        </style>
      </head>
      <body>
        <div class="page-shell">
          <header>
            <h1>{title}</h1>
            <p class="meta">{description}</p>
          </header>
          <section id="story-summary">
            <strong>Game summary:</strong>
            <pre id="story-text">Loading story structure...</pre>
          </section>
          <div id="game-container">
            <canvas id="game-canvas"></canvas>
            <div id="game-ui">
              <div><strong>Controls:</strong> WASD / Arrow keys</div>
              <div id="game-status">Loading game...</div>
            </div>
          </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/three@0.184.0/build/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@dimforge/rapier3d-compat@0.15.0/rapier3d.umd.js"></script>
        <script type="module" src="./game.js"></script>
      </body>
    </html>
    """)
    write_text_file(html_path, content)
    print(f"Created HTML page at {html_path}")


def create_game_script(target_dir: Path, title: str) -> None:
    game_js_path = target_dir / "game.js"
    content = textwrap.dedent("""
    import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.184.0/build/three.module.js';

    class InputManager {
      constructor() {
        this.keys = { forward: false, backward: false, left: false, right: false };
        window.addEventListener('keydown', (event) => this.onKeyDown(event));
        window.addEventListener('keyup', (event) => this.onKeyUp(event));
      }

      onKeyDown(event) {
        if (['w', 'ArrowUp'].includes(event.key)) this.keys.forward = true;
        if (['s', 'ArrowDown'].includes(event.key)) this.keys.backward = true;
        if (['a', 'ArrowLeft'].includes(event.key)) this.keys.left = true;
        if (['d', 'ArrowRight'].includes(event.key)) this.keys.right = true;
      }

      onKeyUp(event) {
        if (['w', 'ArrowUp'].includes(event.key)) this.keys.forward = false;
        if (['s', 'ArrowDown'].includes(event.key)) this.keys.backward = false;
        if (['a', 'ArrowLeft'].includes(event.key)) this.keys.left = false;
        if (['d', 'ArrowRight'].includes(event.key)) this.keys.right = false;
      }
    }

    class GameObject {
      constructor(mesh, body = null) {
        this.mesh = mesh;
        this.body = body;
      }

      syncFromPhysics() {
        if (this.body) {
          const translation = this.body.translation();
          this.mesh.position.set(translation.x, translation.y, translation.z);
        }
      }
    }

    class Game {
      constructor() {
        this.canvas = document.getElementById('game-canvas');
        this.status = document.getElementById('game-status');
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 200);
        this.renderer = new THREE.WebGLRenderer({ canvas: this.canvas, antialias: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.input = new InputManager();
        this.objects = [];
        this.physics = null;
        this.player = null;
        this.goal = null;
        this.story = null;
      }

      async init() {
        this.setupLighting();
        this.setupCamera();
        await this.loadStory();
        await this.initPhysics();
        this.buildScene();
        this.onResize();
        window.addEventListener('resize', () => this.onResize());
        this.animate();
      }

      setupLighting() {
        const ambient = new THREE.HemisphereLight(0x99bbff, 0x222233, 1.2);
        this.scene.add(ambient);
        const dirLight = new THREE.DirectionalLight(0xd3e9ff, 1.1);
        dirLight.position.set(5, 10, 5);
        this.scene.add(dirLight);
      }

      setupCamera() {
        this.camera.position.set(0, 8, 18);
        this.camera.lookAt(0, 0, 0);
      }

      async loadStory() {
        try {
          const response = await fetch('./story-structure.json');
          if (!response.ok) throw new Error('Could not load story-structure.json');
          this.story = await response.json();
          document.getElementById('story-text').textContent = JSON.stringify(this.story, null, 2);
        } catch (error) {
          document.getElementById('story-text').textContent = error.message;
        }
      }

      async initPhysics() {
        await Rapier.init();
        const gravity = new Rapier.Vector3(0.0, -9.81, 0.0);
        const world = new Rapier.World(gravity);
        this.physics = world;

        const groundDesc = Rapier.RigidBodyDesc.fixed();
        const groundBody = world.createRigidBody(groundDesc);
        groundBody.createCollider(Rapier.ColliderDesc.cuboid(30, 0.1, 30));
      }

      buildScene() {
        this.createGround();
        this.createPlayer();
        this.createGoal();
        this.createObstacles();
      }

      createGround() {
        const material = new THREE.MeshStandardMaterial({ color: 0x121a2a });
        const mesh = new THREE.Mesh(new THREE.PlaneGeometry(60, 60), material);
        mesh.rotation.x = -Math.PI / 2;
        this.scene.add(mesh);
      }

      createPlayer() {
        const material = new THREE.MeshStandardMaterial({ color: 0x8bd8ff });
        const mesh = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), material);
        mesh.position.set(0, 0.5, 10);
        this.scene.add(mesh);

        const bodyDesc = Rapier.RigidBodyDesc.dynamic().setTranslation(0, 0.5, 10);
        const body = this.physics.createRigidBody(bodyDesc);
        body.createCollider(Rapier.ColliderDesc.cuboid(0.5, 0.5, 0.5));

        this.player = new GameObject(mesh, body);
        this.objects.push(this.player);
      }

      createGoal() {
        const material = new THREE.MeshStandardMaterial({ color: 0x6cff8a });
        const mesh = new THREE.Mesh(new THREE.BoxGeometry(3, 0.2, 3), material);
        mesh.position.set(0, 0.1, -12);
        this.scene.add(mesh);
        this.goal = new GameObject(mesh, null);
      }

      createObstacles() {
        const obstacles = [
          { x: -6, z: -2 },
          { x: 6, z: -6 },
          { x: 0, z: -8 },
        ];

        obstacles.forEach((pos) => {
          const material = new THREE.MeshStandardMaterial({ color: 0xff8a5c });
          const mesh = new THREE.Mesh(new THREE.BoxGeometry(3, 2, 3), material);
          mesh.position.set(pos.x, 1, pos.z);
          this.scene.add(mesh);

          const bodyDesc = Rapier.RigidBodyDesc.fixed().setTranslation(pos.x, 1, pos.z);
          const body = this.physics.createRigidBody(bodyDesc);
          body.createCollider(Rapier.ColliderDesc.cuboid(1.5, 1, 1.5));
          this.objects.push(new GameObject(mesh, body));
        });
      }

      updatePhysics() {
        this.physics.step();
        this.objects.forEach((object) => object.syncFromPhysics());
      }

      updatePlayer() {
        if (!this.player || !this.player.body) return;
        const direction = new Rapier.Vector3(0, 0, 0);
        const speed = 4.0;
        if (this.input.keys.forward) direction.z -= speed;
        if (this.input.keys.backward) direction.z += speed;
        if (this.input.keys.left) direction.x -= speed;
        if (this.input.keys.right) direction.x += speed;
        this.player.body.setLinvel(direction, true);
      }

      updateUI() {
        this.status.textContent = `Use WASD / arrows to move. Position: ${this.player.mesh.position.x.toFixed(1)}, ${this.player.mesh.position.z.toFixed(1)}`;
      }

      animate() {
        requestAnimationFrame(() => this.animate());
        this.updatePlayer();
        this.updatePhysics();
        this.updateUI();
        this.camera.position.x = this.player.mesh.position.x;
        this.camera.position.z = this.player.mesh.position.z + 16;
        this.camera.lookAt(this.player.mesh.position);
        this.renderer.render(this.scene, this.camera);
      }

      onResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
      }
    }

    const game = new Game();
    game.init();
    """)
    write_text_file(game_js_path, content)
    print(f"Created game script at {game_js_path}")


def review_html_loop(target_dir: Path, title: str, description: str, auto_accept: bool = False, auto_fill: bool = False, auto_decide: bool = False) -> None:
    create_html_file(target_dir, title, description)
    if auto_accept:
        return
    while True:
        decision = prompt_yes_no_ai(
            "Review the generated HTML page? Type 1 to edit, 2 to accept, or 3 to ask AI.",
            default="no",
            auto_fill=auto_fill,
            auto_decide=auto_decide,
        )
        if decision != 'yes':
            break
        html_body = prompt_multiline(
            "Rewrite the full HTML file content below. The page should load story-structure.json from the same folder.",
            auto_fill=auto_fill,
        )
        write_text_file(target_dir / 'index.html', html_body)
        print(f"Updated HTML page at {target_dir / 'index.html'}")


def create_validation_file(target_dir: Path, loop_index: int, kind: str, content: str) -> None:
    filename = f"validation-loop-{loop_index:02d}-{kind}.md"
    path = target_dir / filename
    text = textwrap.dedent(f"""
    # Validation loop {loop_index:02d} {kind.replace('-', ' ').title()}

    {content}
    """)
    write_text_file(path, text)
    print(f"Created validation file at {path}")


def create_continue_gate_file(target_dir: Path, loop_index: int, status: str, next_steps: str) -> None:
    filename = f"continue-gate-{loop_index:02d}.md"
    path = target_dir / filename
    content = textwrap.dedent(f"""
    # Continue Gate {loop_index:02d}

    **Status:** {status}

    **Next steps:**
    {next_steps}
    """)
    write_text_file(path, content)
    print(f"Created continue gate file at {path}")


def run_validation_loops(target_dir: Path, default_loops: int = 3, auto_fill: bool = False, auto_decide: bool = False) -> None:
    print("\nSTAGE 5: Run Plan -> Action -> Review -> Continue Gate loops.")
    print("Each loop should identify issues, create a concrete action plan, apply improvements, and then gate the decision to continue.")

    completed_loops = 0
    for loop_index in range(1, default_loops + 1):
        completed_loops = loop_index
        print(f"\nLoop {loop_index} of {default_loops}: PLAN")
        issues = prompt_multiline(
            "List everything that is wrong, broken, or incomplete in the generated folder. Use a short, itemized list.",
            auto_fill=auto_fill,
        )
        if not issues.strip():
            issues = "(No issues listed.)"
        create_validation_file(target_dir, loop_index, "issues", issues)

        plan = prompt_multiline(
            "Based on the issues above, write the action plan for this loop. Include the three most important fixes to apply.",
            auto_fill=auto_fill,
        )
        if not plan.strip():
            plan = "(No action plan provided.)"
        create_validation_file(target_dir, loop_index, "plan", plan)

        print(f"\nLoop {loop_index}: ACTION — BREAKDOWN")
        breakdown = prompt_multiline(
            "Break the action plan above into a concrete implementation breakdown. Use numbered steps and keep them directly actionable.",
            auto_fill=auto_fill,
        )
        if not breakdown.strip():
            breakdown = "(No breakdown provided.)"
        create_validation_file(target_dir, loop_index, "breakdown", breakdown)

        print(f"\nLoop {loop_index}: ACTION — GOAL-BASED SPEC")
        goal_spec = prompt_multiline(
            "Rewrite the action plan as a goal-based specification. Each goal should be measurable and tied to an outcome.",
            auto_fill=auto_fill,
        )
        if not goal_spec.strip():
            goal_spec = "(No goal-based spec provided.)"
        create_validation_file(target_dir, loop_index, "goal-spec", goal_spec)

        print(f"\nLoop {loop_index}: ACTION — REBUILD")
        edit_choice = prompt_yes_no_ai(
            "Would you like to apply a rebuild now using the goal-based spec?",
            default="no",
            auto_fill=auto_fill,
            auto_decide=auto_decide,
        )
        if edit_choice == 'yes':
            html_body = prompt_multiline(
                "Rewrite the full HTML file content below using the goal-based spec and breakdown to improve the page.",
                auto_fill=auto_fill,
            )
            write_text_file(target_dir / 'index.html', html_body)
            print(f"Updated HTML page at {target_dir / 'index.html'}")

        json_choice = prompt_yes_no_ai(
            "Would you like to revise story-structure.json now using the goal-based spec?",
            default="no",
            auto_fill=auto_fill,
            auto_decide=auto_decide,
        )
        if json_choice == 'yes':
            json_body = prompt_multiline(
                "Rewrite the full story-structure.json content below. It should remain valid JSON and reflect the goal-based spec and latest design changes.",
                auto_fill=auto_fill,
            )
            try:
                parsed = json.loads(json_body)
                write_json_file(target_dir / 'story-structure.json', parsed)
                print(f"Updated JSON file at {target_dir / 'story-structure.json'}")
            except json.JSONDecodeError as exc:
                print(f"JSON was invalid: {exc}. The file was not updated.")

        print(f"\nLoop {loop_index}: REVIEW")
        review_assessment = prompt_short(
            "After applying the action plan, is the current build better? Answer yes/no and briefly explain", "yes", auto_fill=auto_fill)
        review_notes = prompt_multiline(
            "Capture any remaining issues, observations, or improvements after the action step. If nothing remains, type END immediately.",
            auto_fill=auto_fill,
        )
        review_content = textwrap.dedent(f"""
        # Review feedback

        **Review assessment:**
        {review_assessment}

        **Remaining issues or observations:**
        {review_notes}
        """)
        create_validation_file(target_dir, loop_index, "review", review_content)

        print(f"\nLoop {loop_index}: CONTINUE GATE")
        continue_choice = prompt_yes_no_ai(
            "Continue to the next loop?",
            default="yes",
            auto_fill=auto_fill,
            auto_decide=auto_decide,
        )
        next_steps = review_notes if review_notes.strip() else "No remaining issues recorded."
        gate_status = "Continue" if continue_choice == 'yes' else "Stop"
        create_continue_gate_file(target_dir, loop_index, gate_status, next_steps)

        if continue_choice != 'yes':
            print("Stopping early based on the continue gate.")
            break

    completion_content = textwrap.dedent(f"""
    # Validation completion

    Completed {completed_loops} Plan -> Action -> Review -> Continue Gate loop(s).

    Each loop contains an issues list, action plan, review notes, and a continue gate decision.
    Review the generated files and confirm that the build is now ready for gated completion.
    """)
    write_text_file(target_dir / 'completion-gate.md', completion_content)
    print(f"Created completion gate file at {target_dir / 'completion-gate.md'}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Interactive arcade page builder")
    parser.add_argument("--auto-fill", action="store_true", help="Use NVIDIA AI to fill empty prompts automatically.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing target directories without prompting.")
    parser.add_argument("--auto-accept", action="store_true", help="Auto-accept generated HTML and skip manual review.")
    parser.add_argument("--non-interactive", action="store_true", help="Run fully non-interactively using defaults and AI auto-fill.")
    parser.add_argument("--title", type=str, help="Use this game title instead of the seed-generated default.")
    parser.add_argument("--description", type=str, help="Use this game description instead of the seed-generated default.")
    parser.add_argument("--objective", type=str, help="Use this player objective instead of the seed-generated default.")
    parser.add_argument("--validation-loops", type=int, default=3, help="Number of validation loops to run.")
    parser.add_argument("--auto-decide", action="store_true", help="Use NVIDIA AI to decide yes/no prompts when possible.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    global NON_INTERACTIVE_MODE
    if args.non_interactive:
        args.auto_fill = True
        args.auto_accept = True
        args.force = True
        args.auto_decide = True
        NON_INTERACTIVE_MODE = True
        if args.validation_loops < 0:
            args.validation_loops = 0
    print("Interactive arcade game builder")
    print("This script creates a new Page folder, saves DESIGN.md, builds implementation chapters, and scaffolds a story JSON shape.\n")

    load_env_file(ROOT / ".env")
    seed = load_seed_data()
    combination = sample_combination(seed)
    print(format_combination(combination))

    def get_seed_value(singular: str, plural: str, default: str):
        value = combination.get(singular)
        if not value:
            value = combination.get(plural)
        if isinstance(value, list):
            return ", ".join(value)
        return str(value) if value else default

    default_title = get_seed_value("theme", "themes", "New Arcade Game").title()
    default_description = (
        f"A {get_seed_value('theme', 'themes', 'new game')} set in {get_seed_value('environment', 'environments', 'a vivid location')} at "
        f"{get_seed_value('setting', 'settings', 'a dramatic time')}, where the player must {get_seed_value('characterMotivations', 'characterMotivations', 'complete a mission')} "
        f"while using {get_seed_value('movementMechanics', 'movementMechanics', [])}."
    )
    default_objective = (
        f"{get_seed_value('characterMotivations', 'characterMotivations', 'Complete the mission').capitalize()} by "
        f"{get_seed_value('coreLoops', 'coreLoops', 'solving the main loop')} and then {get_seed_value('completionLoops', 'completionLoops', 'finishing the finale')}.")

    while True:
        game_title = args.title or prompt_short("Enter the game title", default_title, auto_fill=args.auto_fill)
        game_description = args.description or prompt_short("Enter a short game description", default_description, auto_fill=args.auto_fill)
        game_objective = args.objective or prompt_short("Enter the main player objective", default_objective, auto_fill=args.auto_fill)

        existing_pages = scan_existing_pages()
        if confirm_unique_idea(game_title, game_description, existing_pages, auto_confirm=args.non_interactive, auto_fill=args.auto_fill, auto_decide=args.auto_decide):
            break
        if args.non_interactive:
            print("Non-interactive mode auto-confirmed uniqueness; continuing.")
            break
        print("\nOkay, revise the title and description to make the game idea more unique.")

    folder_name = slugify(game_title)
    target_dir = ensure_target_directory(folder_name, force=args.force)

    seed_data = {
        "title": game_title,
        "description": game_description,
        "objective": game_objective,
        "seed": combination
    }
    create_seed_choice_file(target_dir, seed_data)

    print("\nSTAGE 1: Ideate expansion ideas from the seed.")
    expansion_text = prompt_multiline(
        "List the top expansion ideas, features, or twists that should make this game more comprehensive. Use the seed details as context.",
        auto_fill=args.auto_fill,
    )
    if not expansion_text.strip():
        expansion_text = "- (No expansion ideas provided yet.)"
    create_ideation_file(target_dir, game_title, combination, expansion_text)

    print("\nSTAGE 2A: Extract core actions, detail chunks, and collapsed gameplay tasks.")
    action_extraction_prompt = textwrap.dedent(f"""
    Take the game idea below and produce:
    1. A concise action map with 6 numbered game activities.
    2. A list of 6 extracted detail items that must be captured in the prototype.
    3. A collapsed task summary useful for building the playable version.

    Game title: {game_title}
    Seed summary:
    {format_combination(combination)}
    Expansion ideas:
    {expansion_text}
    """)
    action_text = call_nvidia_ai(action_extraction_prompt) if args.auto_fill else "- (Manual action extraction required.)"
    action_path = target_dir / "ACTION-EXTRACTION.md"
    write_text_file(action_path, textwrap.dedent(f"""
    # ACTION EXTRACTION

    {action_text}
    """))
    print(f"Saved action extraction to {action_path}")

    print("\nSTAGE 2: Expand the seed and ideation into a full game design specification.")
    print("Design this as a data-driven game built with three.js and Rapier physics.")
    design_intro = textwrap.dedent(f"""
    # {game_title}

    **Description:** {game_description}

    **Objective:** {game_objective}

    **Seed summary:**
    {format_combination(combination)}

    **Expansion ideas:**
    {expansion_text}

    """)
    design_body = prompt_multiline(
        "Use the seed summary and expansion ideas above to write a fully comprehensive DESIGN.md. Include objectives, loop structure, visual style, and game delivery notes. Explicitly frame the game as a data-driven three.js + Rapier experience.",
        auto_fill=args.auto_fill,
    )
    design_text = design_intro + "\n" + (design_body or "(Add the design details here.)")
    create_design_file(target_dir, design_text)

    print("\nSTAGE 3A: Review the concept for fun and build a fun-game checklist into the design.")
    fun_assessment = prompt_short(
        "Is this a fun game? Answer yes/no and briefly explain", "yes", auto_fill=args.auto_fill)
    fun_needs = prompt_multiline(
        "List the elements needed to make this game fun. Use an itemized list.",
        auto_fill=args.auto_fill,
    )
    create_fun_check_file(target_dir, fun_assessment, fun_needs)
    design_text = append_fun_section_to_design(design_text, fun_assessment, fun_needs)
    create_design_file(target_dir, design_text)

    print("\nSTAGE 4: Break the design into implementation chapters.")
    chapters_text = prompt_multiline(
        "List the implementation chapter headings, one per line. Each chapter should cover a distinct part of the design.",
        auto_fill=args.auto_fill,
    )
    create_implementation_chapters(target_dir, chapters_text)

    print("\nSTAGE 5: Define the JSON data shape and story delivery structure.")
    create_story_json(
        target_dir,
        folder_name,
        game_title,
        game_description,
        combination,
        design_text,
        chapters_text,
        fun_assessment,
        fun_needs,
    )

    print("\nSTAGE 6: Build the HTML page in the same folder as the JSON file.")
    print("The HTML page will load story-structure.json from the same location and can treat it as a local file.")
    create_game_script(target_dir, game_title)
    review_html_loop(target_dir, game_title, game_description, auto_accept=args.auto_accept, auto_fill=args.auto_fill, auto_decide=args.auto_decide)

    run_validation_loops(target_dir, default_loops=args.validation_loops, auto_fill=args.auto_fill, auto_decide=args.auto_decide)

    print("\nDone. The new page folder is ready at:")
    print(target_dir)
    print("\nOpen DESIGN.md to refine the spec, review implementation chapters under implementation/, and open index.html to test the story payload loading from story-structure.json.")


if __name__ == "__main__":
    main()
