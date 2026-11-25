# Lab 4: Skyscraper Stack

Based on the faculty repository SETAPESU26/54_skyscrapper_stack and the student's existing implementation at vishnurohit-6300/54_skyscrapper_stack. The source has been consolidated into a runnable project, retaining the existing game design.

## Setup (Windows PowerShell)

```powershell
python -m venv lab4_env
.\lab4_env\Scripts\python.exe -m pip install -r requirements.txt
.\lab4_env\Scripts\python.exe main.py
```

Space or left click drops a block. Space, R or left click restarts after collapse.

## Implemented features

- Correct positive-overlap condition and exact trimming.
- Perfect placement within 3 pixels, 3 points, golden popup, and width restoration after three consecutive perfect drops.
- Rotating falling debris with gravity and camera offset.
- Height-driven atmospheric gradient and stars; actual height and bonus score are shown separately.
- Restart support and minimum one-pixel drawing dimensions for very narrow blocks.

## Verification

Run `python test_game.py` inside the environment. Source syntax was checked; Pygame runtime tests were not run in the packaging environment because Pygame was unavailable.

## Submission scope

Code-only package requested. No gameplay videos or chat history PDF are included. The original handout separately requires these items. No remote repository was modified.
