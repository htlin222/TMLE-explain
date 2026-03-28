# TMLE Explanation Video Generator

[![GitHub stars](https://img.shields.io/github/stars/htlin222/TMLE-explain)](https://github.com/htlin222/TMLE-explain/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/htlin222/TMLE-explain)](https://github.com/htlin222/TMLE-explain/commits/main)
[![Python](https://img.shields.io/badge/python-3.x-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Manim-based video generator for explaining **Targeted Maximum Likelihood Estimation (TMLE)** with Chinese TTS narration.

## Quick Start

```bash
# Install dependencies
make install

# Build the video
make

# Preview
make preview
```

## Project Structure

```
TMLE-explain/
├── src/tmle_explain/
│   ├── scenes.py      # Manim scene definitions
│   └── narration.py   # TTS narration scripts
├── scripts/
│   └── build.py       # Build orchestration
├── audio/             # Generated TTS audio files
├── media/             # Rendered Manim videos
├── output/            # Combined video+audio clips
├── final.mp4          # Final output video
├── Makefile
└── pyproject.toml
```

## Configuration

### Video Quality

Edit Makefile or use manim flags:

- `-ql` (480p15) - Fast preview
- `-qm` (720p30) - Medium quality
- `-qh` (1080p60) - High quality (default)
- `-qk` (4K60) - 4K quality

### TTS Voice

In `src/tmle_explain/narration.py`:

```python
voice = "zh-TW-HsiaoChenNeural"  # Taiwan Mandarin female
# Other options:
# "zh-CN-XiaoxiaoNeural"  # Mainland Mandarin female
# "zh-CN-YunxiNeural"     # Mainland Mandarin male
# "zh-TW-YunJheNeural"    # Taiwan Mandarin male
```

---

## Creating Educational Videos with Manim + TTS

### Suggested Prompt for AI Assistants

```
Create a visual explanation video for [TOPIC] using Manim with Chinese TTS narration.

Requirements:
1. Use Manim for visualization (scenes.py)
2. Use edge-tts for Chinese narration (narration.py)
3. Animation should pause to let narration finish
4. Output 1080p video
5. Use ffmpeg to combine video and audio

Scene structure:
- Scene01: Introduction
- Scene02-N: Main content (one concept per scene)
- SceneN: Summary

For each scene, provide:
- Manim animations
- Corresponding Chinese narration text
```

---

## Layout Tips & Tricks

### 1. Screen Layout Rules

The Manim frame is **14.2 x 8 units** (aspect ratio 16:9). Always leave margins:

```python
# Safe area: keep content within 80% of frame
# Title: top edge with buff=0.5
title.to_edge(UP)

# Content: below title with buff=0.4-0.6
content.next_to(title, DOWN, buff=0.5)
```

### 2. Font Size Guidelines

| Element        | Font Size | Use Case                         |
| -------------- | --------- | -------------------------------- |
| Title          | 44-56     | Scene titles                     |
| Section Header | 28-36     | Section titles                   |
| Body Text      | 22-28     | Main content                     |
| Small Text     | 18-22     | Labels, notes                    |
| Minimum        | 18        | Anything smaller is hard to read |

### 3. Vertical Space Management

**Problem**: Content overflows bottom of screen.

**Solution**: Calculate total height before placing elements.

```python
# Bad: content goes off-screen
problems = VGroup(...).arrange(DOWN, buff=0.4)
solution = VGroup(...)
solution.next_to(problems, DOWN, buff=0.6)  # May overflow!

# Good: use smaller buffs and font sizes
problems = VGroup(...).arrange(DOWN, buff=0.25)
solution = VGroup(...)
solution.next_to(problems, DOWN, buff=0.35)
```

**Rule of thumb for vertical content**:

- Title: ~1 unit
- Each text line: ~0.5-0.8 units (depending on font size)
- Buffs: 0.2-0.4 between items
- Total available: ~6 units (leaving margins)

### 4. Avoid FadeOut at Scene End

**Problem**: FadeOut causes black frame when extending video for audio.

**Bad**:

```python
self.wait(5)
self.play(FadeOut(all_content))  # Ends with black frame!
```

**Good**:

```python
# Keep content visible, just wait
self.wait(10)  # Content stays on screen
```

### 5. Text Wrapping

Manim doesn't auto-wrap. Keep text short or split manually:

```python
# Bad: long line may overflow
Text("這是一段很長的文字可能會超出畫面邊界", font_size=28)

# Good: split into multiple lines
VGroup(
    Text("這是一段很長的文字", font_size=28),
    Text("可能會超出畫面邊界", font_size=28),
).arrange(DOWN, buff=0.2)
```

### 6. Table Sizing

Tables need careful scaling:

```python
table = Table(data).scale(0.5)  # Start at 0.5, adjust as needed

# For 5+ rows, use scale 0.4-0.5
# For 3-4 rows, use scale 0.5-0.6
# For 2 rows, use scale 0.6-0.7
```

### 7. Chinese Font

Always specify Chinese font:

```python
Text("中文內容", font="PingFang TC", font_size=28)
# Other options: "Noto Sans TC", "Microsoft YaHei"
```

---

## Audio-Video Sync Strategy

### Method 1: Extend Video (Recommended)

Use ffmpeg to freeze last frame when audio is longer:

```python
if audio_duration > video_duration:
    padding = audio_duration - video_duration + 0.5
    # Use tpad filter to clone last frame
    f"[0:v]tpad=stop_mode=clone:stop_duration={padding}[v]"
```

### Method 2: Pre-calculate Wait Times

Get audio duration first, then adjust scene timing:

```python
# In scenes.py, add wait time based on audio duration
# Scene01_Intro: audio=30.2s
# Calculate: total_animation_time + wait_time >= audio_duration
self.wait(10)  # Adjust to match audio
```

---

## Troubleshooting

### LaTeX Not Found

If you see `dvisvgm` errors, either:

1. Install LaTeX: `brew install --cask mactex`
2. Use `Text()` instead of `MathTex()` for formulas

### Black Frame at End

Remove `FadeOut()` at scene end. Keep content visible.

### Content Overflow

1. Reduce font sizes (minimum 18-20)
2. Reduce buffs (0.2-0.3)
3. Shorten text
4. Split into multiple scenes

### Audio Out of Sync

Ensure video duration >= audio duration. The build script auto-extends video using `tpad` filter.

---

## License

MIT
