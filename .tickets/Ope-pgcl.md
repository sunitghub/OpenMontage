---
id: Ope-pgcl
status: closed
deps: []
links: []
created: 2026-04-21T20:14:53Z
type: task
priority: 2
assignee: Sunit Joshi
tags: [voiceover, script, shorts]
---
# Generate per-screen script markdown for voiceover

Add feature to always create a script file, <filaname.md> with each line having a Screen <no> followed by the script for that screen. This should be created after the render and will make it easier to create voiceover for those screens.


## Notes

**2026-04-21T20:16:32Z**

Implemented post-render screen script export: added tools/video/export_screen_script.py and Makefile target export-screen-script. Generated Design-Docs/ToPublish/Shorts/Maa-Kali-5-Unknown-Facts/Maa-Kali-5-Yantra-Facts-Screen-Script.md with Screen <no>: <script> lines.
