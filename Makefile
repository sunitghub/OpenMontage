.PHONY: setup install install-dev install-gpu test test-contracts lint clean preflight demo cleanup-renders sync-scene-beats

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
	$(PYTHON) -c "import shutil, os; e=os.path.exists('.env'); shutil.copy('.env.example','.env') if not e else None; print('==> Created .env from .env.example — add your API keys there.' if not e else '==> .env already exists — skipping.')"
	@echo ""
	@echo "Done! Open this project in your AI coding assistant and start creating."
	@echo "  Optional: add API keys to .env to unlock cloud providers."
	@echo "  Optional: run 'make install-gpu' if you have an NVIDIA GPU."

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

demo:
	@echo "==> Rendering zero-key demo videos (no API keys needed)..."
	@echo "    These use only Remotion components — animated charts, text, data viz."
	@echo ""
	./render-demo.sh

demo-list:
	@./render-demo.sh --list

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

clean:
	$(PYTHON) -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]; [p.unlink() for p in pathlib.Path('.').rglob('*.pyc')]"
