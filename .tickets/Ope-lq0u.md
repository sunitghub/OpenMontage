---
id: Ope-lq0u
status: closed
deps: []
links: []
created: 2026-04-22T20:22:39Z
type: task
priority: 2
assignee: Sunit Joshi
tags: [shorts, voiceover, rendering]
---
# Enforce voiceover-first final Shorts renders

Retrospective ticket for the completed fix that prevents final/captioned/publishable Shorts renders without a configured voiceover, adds voiceover-derived timeline tooling, documents the Shorts voiceover flow, and supports caption positioning for the rendered output.


## Notes

**2026-04-22T20:22:43Z**

Completed before ticket creation: render pipeline now blocks final/captioned/publishable renders unless voiceover audio is configured and exists; visual previews may opt out with render_intent=visual_preview. Added apply-voiceover-timeline tooling, screen-script export support, Shorts usage documentation, caption bottom-offset propagation, and tests for the voiceover gate/timeline helper.
