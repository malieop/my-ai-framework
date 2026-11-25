---
name: video-craft
description: >-
  Narrative-driven video craft for HyperFrames — how to tell stories with motion,
  build readable technical diagrams, and create transitions that carry meaning.
  Auto-loads whenever the user makes, edits, reviews, or asks how to improve any
  video or animation.
---

# Video Craft — Narrative-Driven Motion Design

Use this skill together with the `hyperframes` skill (which holds the render contract
and CLI workflow). This skill is the craft layer: what makes a video good, not just valid.

## The Narrative Arc

Every video is a story about change. It answers three questions, in order:

1. **Where are we?** — the world before the change.
2. **What changes?** — the transformation itself.
3. **Where do we end up?** — the new world, and why it matters.

Each scene earns its place by advancing one of these answers. A scene that advances
none of them gets cut. The viewer should never ask "why am I watching this?"

For technical content this means: do not present a list of facts or a tour of a
system. Pick one concrete example (one request, one call, one user action) and
follow it through the whole change, start to finish. The whole picture emerges
from watching one thing travel through it.

## 1. Show the Whole Picture

- **Start wide, then zoom in.** Establish the full context in the first beat, then
  move into the detail that matters. Never open on an unexplained close-up.
- **One worked example throughout.** The same entity (same id, same names, same
  colors) travels through every scene. Continuity is what makes the change legible.
- **Progressive disclosure.** Add one element per beat, when it is named. Never
  drop a finished diagram on screen at once.
- **Every number and label traces to the source.** A value the source did not give
  is left out or marked illustrative.

## 2. Technical Diagrams That Teach

| Principle | How to apply it |
|-----------|-----------------|
| One element at a time | Each box, service, or participant appears exactly when the narration names it |
| Motion follows causality | An event visibly travels from sender to receiver (a tween along a path), it does not fade in at the destination |
| Highlight by dimming | Show the active state by lowering the rest (`opacity: 0.4`), not by adding badges |
| The diagram builds | Start from the simplest true picture; add one part per beat |

Tells of a weak diagram: the whole system appears at once, icons in circles with
no connections, arrows that never animate, a legend instead of labels on the parts.

## 3. Transitions That Carry Meaning

A transition is caused by something on screen. Use 3–5 kinds per video, each with
a reason. At most a third of the seams are hard cuts, and worlds never crossfade
into each other.

| Transition | When to use it | How it works |
|-----------|----------------|--------------|
| Zoom through | Overview → detail | Camera tracks to the element (0.6 s, with blur), then it scales from ~8% to ~250% of frame in 0.35 s, strong ease-in; its fill becomes the next scene |
| Object becomes the world | Zooming into a component | A card grows past the frame in 0.65 s ease-in-out, radius shrinking; surroundings blur ~15 px and fade; new content fades in while it still grows |
| Morph | Showing a state change | One container widens into the next (e.g. ~110 → ~880 px in 0.2 s `power3.out`) with horizontal blur 12 → 0 |
| Carry across | Following an entity between systems | The element shrinks 1 → 0.6 with blur peaking at 6 px mid-move, lands inside the next context as it builds around it |
| Dip cut | Between unrelated beats | Outgoing frame darkens ~40% for 3 frames before a hard cut, so the cut reads as meant |

If a video "feels like slides", the fix is almost always here: enter the next scene
through an object on screen, or cut a move mid-flight.

## 4. Motion Craft

- **Arrive slow, leave clean.** Long-tailed ease-outs on arrivals (`expo.out`,
  `power4.out`); landings take longer than leavings. An exit is one smooth motion —
  never slide, stop, then leave.
- **Exits are 40–50% shorter than entrances.**
- **Overlap.** The next element starts when the previous is 30–50% done. Fully
  sequential looks robotic; all at once looks cheap.
- **Stagger.** Words 60–120 ms apart, list items 40–80 ms, letters one frame apart.
- **Holds.** A line the viewer must read holds ~0.5 s + 0.3 s per word; the final
  line holds at least 2 s. Then exit with a blur-out/fade of 0.13–0.25 s.
- **Dead still.** A landed title does not move. Motion moves to the next element,
  the camera, or the world behind it.
- **Ease by role.** Arrival: `expo.out`/`power4.out`. Camera move or color flood:
  `power2.inOut`. Exit or zoom-through: `power3.in`. Linear only for rotation,
  progress, and constant speed that is the point.
- **Vary entrances.** Never the same fade-and-slide-up for every title. Per-word
  blur-ins, color sweeps from grey to ink, whole-line blur resolves — pick per beat.

## 5. Defaults That Look Generated (Avoid)

- Breathing, floating, or pulsing loops standing in for motion on titles and UI.
- Titles that keep sliding or scaling after they land.
- A slow creeping scale or push late in a scene.
- Bounce on UI elements (position may bounce; opacity and color never do).
- Click rings on every interaction.
- Every scene entering the same way; every element fading and sliding up.
- The same `power2.out` at 0.5 s on everything — the flat default that makes a
  film feel generated.

## 6. The Review Pass

`check` catches what is broken; review catches what is weak. After
`npx hyperframes check --json` passes:

1. `npx hyperframes snapshot --review` — open all three sheets (scene starts and
   middles, the strip across every cut, the beat frames at 360 px phone width).
2. `npx hyperframes snapshot --range START,END --frames 8` — around the hero move
   and the payoff.
3. Watch the rendered file at full speed. Stills do not reveal timing problems.

Read the beat frames in order as a stranger would: does each one cause the next?
Rank problems: **P0** breaks the read (unreadable, wrong, jump at a cut), **P1**
weakens the film (dead stretch, soft payoff), **P2** is polish. Fix every P0 and
the worthwhile P1s — text first, then timing, then detail.

If the film feels busy: remove a third of the motion and keep the moves that lead
the eye.

## 7. Workflow

```bash
npx hyperframes init <project>                              # new project
npx hyperframes catalog --query "<what the beat does>" --json  # reuse before building
# ... build the timeline ...
npx hyperframes check --json                                # contract + craft warnings
npx hyperframes snapshot --review                           # see it as a viewer
npx hyperframes render                                      # only after review passes
```

## Quick Checklist

Before calling a video done:

- [ ] The three narrative questions each get a clear answer, in order
- [ ] One worked example is traceable through every scene
- [ ] No diagram appears fully formed — it builds
- [ ] 3–5 transition types, each caused by something on screen
- [ ] Every landed title holds dead still
- [ ] No item from the "looks generated" list is on screen
- [ ] Review pass done at full speed, P0s and P1s fixed
