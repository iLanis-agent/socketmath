# Socket math

The socket names the amps, the inverter names the ceiling, and the battery names the hours.

Every car promises a wall socket and delivers a flashlight battery. Socket math turns a load in watts into the three answers that matter: the amps it pulls against the socket's fuse, the headroom against an inverter's labeled ceiling, and the hours a starter battery can actually give while keeping enough back to start the engine.

## The three tools

- **Socket plan** - load (W) becomes amps at a labeled 12 V, then the verdict against a labeled 10 A fuse: comfortably under the fuse (80% rule), at the fuse's edge, or past the fuse.
- **Inverter plan** - load against inverter rating becomes the share of the ceiling asked for: an easy ride (80% or less), at its labeled ceiling, or past its ceiling.
- **Runtime plan** - a labeled battery (Ah) at 12 V, with half held back as starter reserve and an 85% inverter efficiency, becomes safe reserve watt-hours and the hours a load gets: a lunch break, an afternoon, a workday, or an all-nighter.

## Honesty notes

Illustrative planning arithmetic only. Every figure is a labeled default. Your fuse box, your inverter's label and your battery's sticker outrank every number here. Motors and compressors ask for multiples of their running watts to start, and an inverter's surge rating covers seconds, not minutes. A starter battery hates deep discharge: for a long session, idle the engine or bring a jump plan.

## Files

- `index.html` - the pitch
- `app.html` - the calculators
- `engine.js` - the arithmetic (browser and node)
- `oracle.py` - the same arithmetic, float-for-float, writing `expected.json`
- `test.js` - runs every case in `expected.json` through `engine.js` and compares results and renders exactly

Run the check:

```
python3 oracle.py && node test.js
```
