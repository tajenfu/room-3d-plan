# room-3d-plan

Interactive 3D furniture planner for a 370 × 470 cm room with an arched alcove,
in a single HTML file built on three.js.

## Run

Open `room.html` in Chrome or Edge. This copy loads three.js from jsDelivr, so
it needs an internet connection.

## Features

- Drag, rotate, add and remove furniture
- Live clearances, overlap and blocked-door warnings
- Named saved versions, with export and import. `room-versions.json` is a sample
  arrangement: press **Import**, choose it, then **Load**
- Download the scene as `.glb`

Furniture sizes, alcove size and all heights are estimates.

## Build the offline copy

The offline copy embeds three.js 0.170.0 and runs without internet.

```
npm pack three@0.170.0
tar -xzf three-0.170.0.tgz
python build_offline.py package
```

This writes `room-offline.html` and `room-3d-plan.zip`. The zip is what to send
to someone else; `README.txt` inside it explains the controls in English and
Chinese.
