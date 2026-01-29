#!/usr/bin/env python3
"""
Build script for TMLE explanation video

Usage:
    python scripts/build.py [--render] [--audio] [--combine] [--all]

Options:
    --render    Render Manim scenes only
    --audio     Generate TTS audio only
    --combine   Combine video and audio only
    --all       Run all steps (default)
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Project root
ROOT = Path(__file__).parent.parent
SCENES_FILE = ROOT / "src" / "tmle_explain" / "scenes.py"
AUDIO_DIR = ROOT / "audio"
OUTPUT_DIR = ROOT / "output"
VIDEO_DIR = ROOT / "media" / "videos" / "scenes" / "1080p60"

SCENES = [
    "Scene01_Intro",
    "Scene02_DataTable",
    "Scene03_PS",
    "Scene04_IPTW",
    "Scene05_IPTWExample",
    "Scene06_IPTWProblem",
    "Scene07_TMLEIntro",
    "Scene08_TMLEStep1",
    "Scene09_TMLEStep2",
    "Scene10_TMLEStep3",
    "Scene11_TMLEStep4",
    "Scene12_Comparison",
    "Scene13_Summary",
]


def render_scenes() -> None:
    """Render all Manim scenes at 1080p60"""
    print("=" * 50)
    print("Rendering Manim scenes (1080p60)...")
    print("=" * 50)

    for scene in SCENES:
        print(f"\nRendering {scene}...")
        cmd = ["uv", "run", "manim", "render", "-qh", str(SCENES_FILE), scene]
        result = subprocess.run(cmd, cwd=ROOT)
        if result.returncode != 0:
            print(f"Error rendering {scene}")
            sys.exit(1)
        print(f"  Done: {scene}")


def generate_audio() -> None:
    """Generate TTS audio for all scenes"""
    print("\n" + "=" * 50)
    print("Generating TTS audio...")
    print("=" * 50)

    narration_script = ROOT / "src" / "tmle_explain" / "narration.py"
    subprocess.run(["uv", "run", "python", str(narration_script)], cwd=ROOT, check=True)


def get_duration(file_path: Path) -> float:
    """Get duration of media file using ffprobe"""
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(file_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())


def combine_scene(scene: str) -> Path | None:
    """Combine video and audio for a single scene"""
    video_file = VIDEO_DIR / f"{scene}.mp4"
    audio_file = AUDIO_DIR / f"{scene}.mp3"
    output_file = OUTPUT_DIR / f"{scene}_combined.mp4"

    if not video_file.exists():
        print(f"Warning: Video not found: {video_file}")
        return None
    if not audio_file.exists():
        print(f"Warning: Audio not found: {audio_file}")
        return None

    video_duration = get_duration(video_file)
    audio_duration = get_duration(audio_file)

    print(f"  {scene}: video={video_duration:.1f}s, audio={audio_duration:.1f}s")

    if audio_duration > video_duration:
        padding = audio_duration - video_duration + 0.5
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(video_file),
            "-i",
            str(audio_file),
            "-filter_complex",
            f"[0:v]tpad=stop_mode=clone:stop_duration={padding}[v]",
            "-map",
            "[v]",
            "-map",
            "1:a",
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-shortest",
            str(output_file),
        ]
    else:
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(video_file),
            "-i",
            str(audio_file),
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-shortest",
            str(output_file),
        ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error combining {scene}: {result.stderr}")
        return None

    return output_file


def combine_all() -> None:
    """Combine video and audio, then concatenate all scenes"""
    print("\n" + "=" * 50)
    print("Combining video and audio...")
    print("=" * 50)

    OUTPUT_DIR.mkdir(exist_ok=True)

    combined_files = []
    for scene in SCENES:
        output_file = combine_scene(scene)
        if output_file:
            combined_files.append(output_file)

    if not combined_files:
        print("Error: No combined files generated!")
        sys.exit(1)

    # Create concat list
    concat_file = OUTPUT_DIR / "concat_list.txt"
    with open(concat_file, "w") as f:
        for file_path in combined_files:
            f.write(f"file '{file_path.name}'\n")

    print("\n" + "=" * 50)
    print("Concatenating all scenes...")
    print("=" * 50)

    final_output = ROOT / "final.mp4"
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-c",
        "copy",
        str(final_output),
    ]

    result = subprocess.run(cmd, cwd=OUTPUT_DIR)
    if result.returncode != 0:
        print("Error concatenating, trying with re-encoding...")
        cmd = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            str(final_output),
        ]
        result = subprocess.run(cmd, cwd=OUTPUT_DIR)
        if result.returncode != 0:
            print("Error re-encoding")
            sys.exit(1)

    print("\n" + "=" * 50)
    print(f"SUCCESS! Generated: {final_output}")
    print("=" * 50)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build TMLE explanation video")
    parser.add_argument("--render", action="store_true", help="Render scenes only")
    parser.add_argument("--audio", action="store_true", help="Generate audio only")
    parser.add_argument("--combine", action="store_true", help="Combine only")
    parser.add_argument("--all", action="store_true", help="Run all steps")
    args = parser.parse_args()

    # Default to all if no flags
    run_all = args.all or not (args.render or args.audio or args.combine)

    if run_all or args.render:
        render_scenes()

    if run_all or args.audio:
        generate_audio()

    if run_all or args.combine:
        combine_all()


if __name__ == "__main__":
    main()
