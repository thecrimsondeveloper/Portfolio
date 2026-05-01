# PagesBrainstorm-CLI

This folder contains small brainstorming CLIs for arcade idea iteration.

## brainstorm_cli.py

Ingests `summary_brainstorming.json` and compiles `final_brainstorming.json` using the same LM Studio endpoint/model pattern as `chainstorm_cli.py`, while still assembling and validating the final JSON locally.

Example:

```bash
cd Portfolio-Vite
python3 PagesBrainstorm-CLI/brainstorm_cli.py --raw
```

Brainstorm finalizer behavior:

- reads `PagesInteractive-CLI/summary_brainstorming.json`
- sends compact structured prompts to the LM Studio-compatible endpoint at `http://10.0.0.137:1234/v1/chat/completions`
- walks through explicit design steps for gameplay time, enemy types, player actions, progression goals, and world anchors
- adds random injections and random exploration loops to widen the concept space
- keeps final JSON assembly local so the output stays build-ready even if individual LM replies need fallback handling
- writes `PagesInteractive-CLI/final_brainstorming.json` with a build-ready final game spec

Useful options:

- `--file`: choose a different summary JSON file
- `--output`: choose a different final brainstorming output path
- `--model`: LM Studio model id for finalization
- `--endpoint`: LM Studio chat completions endpoint
- `--temperature`: sampling temperature for finalization prompts
- `--random-seed`: seed for random injections and exploration loops
- `--exploration-loops`: number of exploration loops to run before finalizing the spec
- `--raw`: print only the output file path

## chainstorm_cli.py

Runs one-word chain brainstorming against the LM Studio-compatible endpoint at `http://10.0.0.137:1234/v1/chat/completions`.

Example single-word rewrite:

```bash
cd Portfolio-Vite
python3 PagesBrainstorm-CLI/chainstorm_cli.py --model qwen3.5-0.8b --seed harbor --raw
```

Example full dataset smoothing pass:

```bash
cd Portfolio-Vite
python3 PagesBrainstorm-CLI/chainstorm_cli.py --model qwen3.5-0.8b
```

Dataset-pass behavior:

- walks every row in `PagesInteractive-CLI/seed_brainstorming.json`
- smooths each row from left to right so adjacent words fit better together
- avoids repeating words already present in the row
- appends 5 new words to each row on every run by default

Useful options:

- `--model`: LM Studio model id
- `--seed`: rewrite one standalone seed word
- `--file`: choose a different brainstorming JSON file
- `--extend-count`: number of new words to append per row during a dataset pass
- `--raw`: print only the raw result

## seed_fetcher_cli.py

Builds a robust summary-ready seed dataset from very simple injected category parameters while preserving the `[category, rows]` 2D shape expected by the summary tools.

Example:

```bash
cd Portfolio-Vite
python3 PagesBrainstorm-CLI/seed_fetcher_cli.py \
	--environment harbor,reef,forest \
	--mechanic dash,pulse,drift \
	--enemy sentry,raider,drone \
	--progression unlock,recover,converge \
	--output PagesInteractive-CLI/seed_brainstorming.generated.json \
	--raw
```

Seed fetcher behavior:

- accepts simple comma-separated seed words per category
- injects those words into category-specific expansion maps
- pulls fallback vocabulary from the current seed dataset
- preserves the existing 2D brainstorming rows and appends one new row per category when augmentation is enabled
- when LM Studio is available, appends one extra brainstorm row per category using `qwen3.5-2b@q8_0`
- if LM Studio is unavailable, falls back to deterministic row growth instead of failing

Useful options:

- `--source`: source brainstorming dataset for fallback vocabulary
- `--output`: output brainstorming dataset path
- `--environment`: comma-separated environment seed words
- `--mechanic`: comma-separated mechanic seed words
- `--enemy`: comma-separated enemy seed words
- `--progression`: comma-separated progression seed words
- `--inject`: extra category injection like `environment=reef,lagoon`
- `--brainstorm-mode`: `auto`, `required`, or `skip` for model-driven row augmentation
- `--endpoint`: LM Studio chat completions endpoint used for augmentation
- `--model`: LM Studio model id used for augmentation
- `--augment-rows`: how many model rows to append per category on each run
- `--raw`: print only the output file path

## chainsummary_cli.py

Builds `PagesInteractive-CLI/summary_brainstorming.json` from `seed_brainstorming.json` using chained inference aggregation, ranked passing, and sampled game-concept synthesis.

Example:

```bash
cd Portfolio-Vite
python3 PagesBrainstorm-CLI/chainsummary_cli.py --raw
```

Summary behavior:

- reads the current 2D seed chain dataset from `PagesInteractive-CLI/seed_brainstorming.json`
- runs deterministic ranked aggregation passes per category
- samples category words from multiple piecemeal slices including ranked words, row heads, middles, tails, and focus pools
- smooths those sampled parts into a merged category sample set before synthesizing the game design document
- writes `explorationLevel`, sampled category words, `smoothedWords`, a synthesized `gameDesignDoc`, per-category top words, per-pass rankings, and per-row chain summaries
- writes the final summary artifact to `PagesInteractive-CLI/summary_brainstorming.json`

Useful options:

- `--file`: choose a different source brainstorming JSON file
- `--output`: choose a different summary output path
- `--passes`: number of ranked aggregation passes per category
- `--top-k`: number of top ranked words to keep per category
- `--row-top-k`: number of focus words to keep per row summary
- `--sample-size`: number of random words to sample per category
- `--smooth-sample-size`: number of merged words to keep after piecemeal smoothing
- `--random-seed`: seed for category sampling
- `--exploration-level`: label to embed in the generated summary and game design doc
- `--raw`: print only the output file path
