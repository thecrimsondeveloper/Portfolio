# PagesBrainstorm-CLI

A sibling CLI to `PagesInteractive-CLI` for brainstorming variant arcade game ideas using the NVIDIA chat completion endpoint.

## Usage

1. Set `NVIDIA_API_KEY` in your environment.
2. Run:

```bash
cd Portfolio-Vite
python3 PagesBrainstorm-CLI/brainstorm_cli.py --theme "aurora harbor" --count 5
```

## Options

- `--theme`, `-t`: starting theme or concept for ideas
- `--count`, `-c`: number of variant ideas to generate
- `--prompt`, `-p`: custom NVIDIA prompt text
- `--raw`: show raw NVIDIA response without CLI formatting

## Notes

This CLI uses the same NVIDIA endpoint pattern as the existing interactive builder CLI, but is focused on generating compact variant game ideas for brainstorming.
