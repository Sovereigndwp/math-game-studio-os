# Trig Tower — HS Trigonometry Game

# Game Concept

## Core Fantasy: You are a siege engineer. Solve trig problems to aim your cannon and demolish enemy towers.

# Question Templates (TT1–TT12)

- [ ] TT1 — SOH right triangle: find missing side
- [ ] TT2 — CAH right triangle: find missing side
- [ ] TT3 — TOA right triangle: find missing side or angle
- [ ] TT4 — Unit circle: exact value of sin/cos at standard angles
- [ ] TT5 — Angle in standard position / reference angle
- [ ] TT6 — Radian–degree conversion
- [ ] TT7 — Law of Sines: find missing side
- [ ] TT8 — Law of Cosines: find missing side or angle
- [ ] TT9 — Trig identities: Pythagorean identity simplification
- [ ] TT10 — Amplitude/period of sine/cosine from equation
- [ ] TT11 — Angle of elevation/depression word problem
- [ ] TT12 — Projectile launch angle from range formula

# Game Design: Trig Tower

- Core interaction: Solve trig problem → unlock correct angle/power → fire cannon → hit target tower
- 3 Districts: The Foothills (SOH-CAH-TOA), The Fortress (Unit Circle + Radians), The Citadel (Law of Sines/Cosines)
- 15 missions: 5 per district. Each mission: 3–5 trig problems to set cannon angle → fire arc → score
- Scoring: accuracy bonus + speed bonus + no-hint bonus + streak multiplier
- Misconception traps: sin/cos swap (M1), degree/radian confusion (M2), inverse function confusion (M3), wrong ratio setup (M4)

# P1 Build Status

- [x] Game concept approved and added to Studio OS pipeline
- [x] 12 question templates defined (TT1–TT12)
- [x] P1 prototype built as inline React component (TrigTower.tsx)
- [x] Wired into Studio OS as Tab 12 (view='trigtower')
