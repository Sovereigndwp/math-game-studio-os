# Conversation with Content Expansion Agent

Title: Trig Tower: M1 Rounds Overview

Started on: Apr 9, 2026, 5:59 PM

***

**Dalia P (Apr 10, 2026, 10:17 AM)**

Design 3 new rounds specifically targeting M1 (sin/cos swap) for Trig Tower. Each must have a deliberate trap distractor, a scaffolding hint, and a CCSS tag.

**Content Expansion Agent (Apr 10, 2026, 10:17 AM)**

\## Trig Tower — 3 New Rounds Targeting **M1: sin/cos swap**

Each round below is built to *force* a sin-vs-cos decision via a clear “adjacent vs opposite” or “x vs y” cue, and includes a **deliberate trap distractor** that corresponds to doing the swap.

\---

\### Round M1-1: **Angle at Origin (Coordinate Ratio)**
\- **Difficulty Tier:** D1 (core identification)
\- **Skill Tag:** unit-circle-from-point, ratio-definition
\- **CCSS Tag:** **HSG-SRT.C.6** (understand sine/cosine as ratios in right triangles)

\**Prompt / Stem (in-game):**  
A ray from the origin passes through point **P(3, 4)** in Quadrant I. Let **θ** be the angle the ray makes with the positive x-axis. What is **cos(θ)**?

\**Correct Answer:**  
\\[
\cos(\theta)=\frac{3}{5}
\\]

\**Answer Choices (include trap):**
\- A) \\( \frac{3}{5} \\) **(Correct)**
\- B) \\( \frac{4}{5} \\) **(Trap: sin/cos swap — uses y/r instead of x/r)**
\- C) \\( \frac{5}{3} \\) (Reciprocal error)
\- D) \\( \frac{5}{4} \\) (Reciprocal + swap blend)

\**Scaffolding Hint (non-revealing):**  
“Compute the radius \\(r=\sqrt{x^2+y^2}\\). For an angle from the x-axis, cosine uses the **x-value over r**.”

\**Deliberate M1 Trap Rationale:**  
Choice B matches the common swap: treating cosine like “opposite/hypotenuse” or using \\(y/r\\).

\---

\### Round M1-2: **Right Triangle, Given Angle (Adjacent vs Opposite)**
\- **Difficulty Tier:** D2 (requires mapping sides + selecting ratio)
\- **Skill Tag:** right-triangle-trig, side-identification
\- **CCSS Tag:** **HSG-SRT.C.6**

\**Prompt / Stem (in-game):**  
In a right triangle, angle **θ** is an acute angle. The side **adjacent** to θ is **12**, and the **hypotenuse** is **13**. What is **sin(θ)**?

\**Correct Answer:**  
\\[
\sin(\theta)=\frac{5}{13}
\\]
(because opposite \\(=\sqrt{13^2-12^2}=5\\))

\**Answer Choices (include trap):**
\- A) \\( \frac{5}{13} \\) **(Correct)**
\- B) \\( \frac{12}{13} \\) **(Trap: sin/cos swap — uses adjacent/hypotenuse)**
\- C) \\( \frac{13}{12} \\) (Reciprocal error)
\- D) \\( \frac{5}{12} \\) (Uses opposite/adjacent, i.e., tangent confusion)

\**Scaffolding Hint (non-revealing):**  
“First find the missing leg using the Pythagorean Theorem. Then remember: **sine = opposite/hypotenuse** relative to θ.”

\**Deliberate M1 Trap Rationale:**  
Choice B is exactly cos(θ), chosen by students who swap sine/cosine definitions.

\---

\### Round M1-3: **Angle of Elevation (Context + Representation Shift)**
\- **Difficulty Tier:** D3 (context → diagram → ratio; higher cognitive load)
\- **Skill Tag:** modeling-with-trig, diagram-translation
\- **CCSS Tag:** **HSG-SRT.C.8** (use trig to solve real-world problems)

\**Prompt / Stem (in-game):**  
A drone is **50 m** above the ground and is horizontally **120 m** away from a sensor. Let **θ** be the angle of elevation from the sensor to the drone. Which expression equals **cos(θ)**?

\**Correct Answer:**  
\\[
\cos(\theta)=\frac{120}{\sqrt{120^2+50^2}}=\frac{120}{130}=\frac{12}{13}
\\]

\**Answer Choices (include trap):**
\- A) \\( \frac{120}{130} \\) **(Correct)**
\- B) \\( \frac{50}{130} \\) **(Trap: sin/cos swap — uses opposite/hypotenuse)**
\- C) \\( \frac{50}{120} \\) (Tangent confusion)
\- D) \\( \frac{130}{120} \\) (Reciprocal error)

\**Scaffolding Hint (non-revealing):**  
“Draw the right triangle: horizontal distance is along the ground, height is vertical. Cosine uses **adjacent (ground distance)** over **hypotenuse (line of sight)**.”

\**Deliberate M1 Trap Rationale:**  
Choice B is sin(θ). The context often pushes learners to grab the ‘height’ first and mistakenly use it for cosine.

\---

\### Quick Compliance Check (for these 3 rounds)
\- **M1 trap included:** 3/3 (each has explicit swapped-ratio distractor)  
\- **Hints present:** 3/3 (scaffold without giving the choice)  
\- **CCSS tagged:** yes (HSG-SRT.C.6 and HSG-SRT.C.8)  
\- **Difficulty ramp:** D1 → D2 → D3 (smooth escalation)
