# Claude Evaluation Prompt For Top 5 Math Concepts

Use the five concept briefs in `top_5_math_concepts_claude_packet.md` as the next evaluation batch.

Work in this order:

1. Bakery Rush
2. Pharmacy Counter
3. Chef's Fractions
4. Galaxy Coordinates
5. Trade Floor

For each concept:

- evaluate it through the current Math Game Studio OS logic
- identify the strongest likely interaction type
- identify likely family placement
- define the likely smallest meaningful loop
- assess whether it should cleanly reach `prototype_spec`
- assess whether it should cleanly reach `prototype_build_spec`
- identify the biggest ambiguity, weakness, or monetization opportunity

Then summarize:

1. which concept should be built first
2. which concepts belong in the same family
3. which concept is easiest to monetize first
4. whether Pharmacy Counter should become:
   - a level-up path inside Bakery
   - a sibling concept in the same family
   - or a separate family
5. which middle-grade concept should follow Bakery

Constraints:

- do not build anything yet
- do not broaden beyond evaluating this batch
- stay math-only for this pass
- treat Bakery as the current reference concept unless the evaluation strongly overturns that assumption
