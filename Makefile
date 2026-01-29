.PHONY: all render audio combine clean preview help install lint format

# Default target
all: final.mp4

# Install dependencies
install:
	uv sync

# Render all Manim scenes (1080p60)
render:
	@echo "Rendering Manim scenes..."
	@for scene in Scene01_Intro Scene02_DataTable Scene03_PS Scene04_IPTW \
		Scene05_IPTWExample Scene06_IPTWProblem Scene07_TMLEIntro \
		Scene08_TMLEStep1 Scene09_TMLEStep2 Scene10_TMLEStep3 \
		Scene11_TMLEStep4 Scene12_Comparison Scene13_Summary; do \
		echo "  Rendering $$scene..."; \
		uv run manim render -qh src/tmle_explain/scenes.py $$scene; \
	done

# Generate TTS audio
audio:
	@echo "Generating TTS audio..."
	uv run python src/tmle_explain/narration.py

# Combine video and audio
combine:
	@echo "Combining video and audio..."
	uv run python scripts/build.py --combine

# Build final video
final.mp4: render audio combine
	@echo "Build complete: final.mp4"

# Preview final video
preview: final.mp4
	open final.mp4

# Render single scene (usage: make scene SCENE=Scene01_Intro)
scene:
	uv run manim render -qh src/tmle_explain/scenes.py $(SCENE)

# Render single scene in preview quality (faster)
scene-preview:
	uv run manim render -ql src/tmle_explain/scenes.py $(SCENE)

# Lint and format
lint:
	uv run ruff check src/ scripts/

format:
	uv run ruff format src/ scripts/
	uv run ruff check --fix src/ scripts/

# Clean generated files
clean:
	rm -rf media/
	rm -rf audio/
	rm -rf output/
	rm -f final.mp4

# Clean only output (keep rendered scenes)
clean-output:
	rm -rf output/
	rm -f final.mp4

# Help
help:
	@echo "TMLE Explanation Video Builder"
	@echo ""
	@echo "Usage:"
	@echo "  make              Build final.mp4 (all steps)"
	@echo "  make install      Install dependencies"
	@echo "  make render       Render all Manim scenes"
	@echo "  make audio        Generate TTS audio"
	@echo "  make combine      Combine video and audio"
	@echo "  make preview      Open final.mp4"
	@echo "  make scene SCENE=SceneName  Render single scene"
	@echo "  make scene-preview SCENE=SceneName  Render single scene (fast)"
	@echo "  make lint         Run linter"
	@echo "  make format       Format code"
	@echo "  make clean        Remove all generated files"
	@echo "  make clean-output Remove only output files"
