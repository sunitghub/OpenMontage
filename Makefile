.PHONY: setup install install-dev install-gpu test test-contracts lint clean preflight demo demo-list hyperframes-doctor hyperframes-warm cleanup-renders sync-scene-beats export-screen-script apply-voiceover-timeline cleanup-remotion-staging shorts-scenes shorts-artifacts shorts-generate-clips shorts-render

UV ?= $(shell command -v uv 2>/dev/null)
PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python)
PIP ?= $(if $(UV),uv pip,$(PYTHON) -m pip)

# ---- One-command setup ----

setup:
	@echo "==> Installing Python dependencies..."
	$(PIP) install -r requirements.txt
	@echo ""
	@echo "==> Installing Remotion composer..."
	cd remotion-composer && npm install
	@echo ""
	@echo "==> Installing free offline TTS (Piper)..."
	$(PIP) install piper-tts || echo "  [skip] piper-tts install failed — TTS will use cloud providers instead"
	@echo ""
	@echo "==> Installing HyperFrames runtime (cache-warm via npx)..."
	@echo "    Pulls the 'hyperframes' npm package into the local npx cache so the"
	@echo "    first render doesn't pay a 30-60s cold-fetch penalty. ~20MB of disk."
	@npx --yes hyperframes --version >/dev/null 2>&1 && echo "    HyperFrames CLI cached (npx)" || echo "  [skip] HyperFrames cache-warm failed — offline or npm unavailable; first render will fetch on demand"
	@$(PYTHON) -c "from tools.video.hyperframes_compose import HyperFramesCompose; HyperFramesCompose._npm_resolve_cache=None; c=HyperFramesCompose()._runtime_check(); print(f'    HyperFrames runtime_available={c[\"runtime_available\"]}, npm={c.get(\"npm_package_version\") or c.get(\"npm_resolve_error\")}'); [print(f'    note: {r}') for r in c['reasons']]" || echo "  [skip] HyperFrames check failed — runtime can be set up later"
	@echo ""
	$(PYTHON) -c "import shutil, os; e=os.path.exists('.env'); shutil.copy('.env.example','.env') if not e else None; print('==> Created .env from .env.example — add your API keys there.' if not e else '==> .env already exists — skipping.')"
	@echo ""
	@echo "Done! Open this project in your AI coding assistant and start creating."
	@echo "  Optional: add API keys to .env to unlock cloud providers."
	@echo "  Optional: run 'make install-gpu' if you have an NVIDIA GPU."
	@echo "  Optional: run 'make hyperframes-doctor' to fully validate the HyperFrames runtime."
	@echo "  Optional: run 'make hyperframes-warm' anytime to refresh the npx cache to the latest hyperframes version."

# ---- Individual installs ----

install:
	$(PIP) install -r requirements.txt

install-dev:
	$(PIP) install -r requirements-dev.txt

install-gpu:
	$(PIP) install -r requirements-gpu.txt
	$(PIP) install diffusers transformers accelerate

# ---- Testing ----

test:
	$(PYTHON) -m pytest tests/ -v

test-contracts:
	$(PYTHON) -m pytest tests/contracts/ -v

# ---- Utilities ----

preflight:
	$(PYTHON) -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu(), indent=2))"

hyperframes-doctor:
	@echo "==> Probing HyperFrames runtime (node/ffmpeg/npx + hyperframes doctor)..."
	python -c "from tools.video.hyperframes_compose import HyperFramesCompose; r=HyperFramesCompose().execute({'operation':'doctor'}); import json; print(json.dumps(r.data, indent=2)); print('OK' if r.success else f'FAIL: {r.error}')"

hyperframes-warm:
	@echo "==> Refreshing the HyperFrames npx cache to latest..."
	@echo "    Uses --prefer-online so npx picks up new releases since your last run."
	npx --yes --prefer-online hyperframes --version
	@echo "==> Cache warm complete."

demo:
	@echo "==> Rendering zero-key demo videos (no API keys needed)..."
	@echo "    These use only Remotion components — animated charts, text, data viz."
	@echo ""
	python render_demo.py

demo-list:
	@python render_demo.py --list

lint:
	$(PYTHON) -m py_compile tools/base_tool.py
	$(PYTHON) -m py_compile tools/tool_registry.py
	$(PYTHON) -m py_compile tools/cost_tracker.py
	$(PYTHON) -m py_compile tools/analysis/composition_validator.py

cleanup-renders:
	@if [ -z "$(DIR)" ]; then echo "Usage: make cleanup-renders DIR=projects/foo/renders [KEEP=1] [DRY_RUN=1]"; exit 1; fi
	$(PYTHON) tools/video/render_cleanup.py $(DIR) $(if $(KEEP),--keep $(KEEP),) $(if $(DRY_RUN),--dry-run,)

sync-scene-beats:
	@if [ -z "$(MD)" ] || [ -z "$(EDIT)" ]; then echo "Usage: make sync-scene-beats MD=path/to/package.md EDIT=path/to/edit_decisions.json [DRY_RUN=1]"; exit 1; fi
	$(PYTHON) tools/video/sync_scene_beats.py $(MD) $(EDIT) $(if $(DRY_RUN),--dry-run,)

export-screen-script:
	@if [ -z "$(MD)" ]; then echo "Usage: make export-screen-script MD=path/to/package.md [OUT=path/to/script.md] [DRY_RUN=1]"; exit 1; fi
	$(PYTHON) tools/video/export_screen_script.py $(MD) $(if $(OUT),--output $(OUT),) $(if $(DRY_RUN),--dry-run,)

apply-voiceover-timeline:
	@if [ -z "$(EDIT)" ] || [ -z "$(TRANSCRIPT)" ] || [ -z "$(VOICEOVER)" ] || [ -z "$(SCENE_END_SEGMENTS)" ]; then echo "Usage: make apply-voiceover-timeline EDIT=path/to/edit.json TRANSCRIPT=path/to/transcript.json VOICEOVER=path/to/voiceover.mp3 SCENE_END_SEGMENTS=4,6,9 [OUT=path/to/output.json] [DRY_RUN=1]"; exit 1; fi
	$(PYTHON) tools/video/apply_voiceover_timeline.py $(EDIT) $(TRANSCRIPT) $(VOICEOVER) --scene-end-segments $(SCENE_END_SEGMENTS) $(if $(OUT),--output $(OUT),) $(if $(DRY_RUN),--dry-run,)

cleanup-remotion-staging:
	@if [ -z "$(PROJECT)" ]; then echo "Usage: make cleanup-remotion-staging PROJECT=<project-slug>"; exit 1; fi
	@rm -f remotion-composer/public/test-props.json
	@rm -f remotion-composer/public/$(PROJECT)/props-v*.json
	@if [ -d "remotion-composer/public/$(PROJECT)/assets" ] && [ ! -L "remotion-composer/public/$(PROJECT)/assets" ]; then rm -rf remotion-composer/public/$(PROJECT)/assets; fi
	@if [ ! -e "remotion-composer/public/$(PROJECT)/assets" ]; then ln -s "$(CURDIR)/projects/$(PROJECT)/assets" remotion-composer/public/$(PROJECT)/assets; fi

shorts-scenes:
	@if [ -z "$(NAME)" ]; then echo "Usage: make shorts-scenes NAME=<folder>"; exit 1; fi
	@./youtube-shorts.sh $(NAME) --scenes

shorts-artifacts:
	@if [ -z "$(NAME)" ]; then echo "Usage: make shorts-artifacts NAME=<folder>"; exit 1; fi
	@./youtube-shorts.sh $(NAME) --artifacts

shorts-generate-clips:
	@if [ -z "$(NAME)" ]; then echo "Usage: make shorts-generate-clips NAME=<folder>"; exit 1; fi
	@./youtube-shorts.sh $(NAME) --generate-clips

shorts-render:
	@if [ -z "$(NAME)" ]; then echo "Usage: make shorts-render NAME=<folder>"; exit 1; fi
	@./youtube-shorts.sh $(NAME) --rendershorts

clean:
	$(PYTHON) -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]; [p.unlink() for p in pathlib.Path('.').rglob('*.pyc')]"
