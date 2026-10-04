# A Two-Sided Optimization for Theater Ballistic Missile Defense (Brown, Carlyle, Diehl, Kline, Wood, 2005, Operations Research 53(5), pp.745-763)
- File: no PDF obtained — INFORMS paywalled (DOI 10.1287/opre.1050.0231). Source used: RePEc IDEAS metadata + abstract (https://ideas.repec.org/a/inm/oropre/v53y2005i5p745-763.html), fetched 2026-10-04. Markings: none (journal article).
- Status: PARTIAL NOTE — abstract-level only. Full-text claims/metrics NOT verified. Do not cite numbers beyond abstract.

## Problem & motivation
- Claim (abstract): plan pre-positioning of defensive interceptors to counter attack threat via two-sided optimization (defender minimizes worst-case damage attacker can achieve).
- Motivation stated: complement heuristics/supercomputing planning tools with mathematically grounded, computationally efficient model; illuminate value of secrecy/deception.

## Threat/mission context
- Theater ballistic missile defense vs attacker with known launch sites, target values, weapon capabilities (complete-information baseline variant).
- Demonstration: two hypothetical North Korean scenarios (details not stated in abstract).

## Defense layer / system element
- Pre-positioning of BMD platforms (interceptors) — architecture/resource allocation layer, not sensor or guidance. Relates to VisualSim `InterceptorQueue` inventory + launcher placement.

## Method / approach
- JOINT DEFENDER: defender-attacker bilevel / minimax-type optimization (keywords: bilevel integer linear program, mixed-integer linear program per RePEc).
- Variants restrict attacker/defender information access to value secrecy.
- Claimed runtime: transparent exchange evaluated "in a few minutes on a laptop"; near-optimal secret defenses "in seconds" (abstract, unverified — no hardware/spec/year baseline given).

## Assumptions
- Baseline assumes attacker aware of defensive pre-positioning + both sides complete information on target values, launch sites, capabilities (abstract). Strong/perfect-information assumption — flag as unrealistic for real ops; useful as worst-case bound.
- Other model details, constraints, integer variables: not stated in abstract.

## Data / simulation setup
- Not stated in abstract. No raid size, Pk, geography, seeds. Full paper needed.

## Metrics & results
- No numeric results in abstract. Do not cite effectiveness numbers from this note.

## Baselines & comparisons
- Abstract positions vs "current planning tools that use heuristics or supercomputing" — no named tool, no head-to-head numbers in abstract.

## Claims vs evidence
| Claim | Evidence in accessed source | Strength |
|---|---|---|
| Transparent exchange in minutes, secret defenses in seconds | Abstract assertion only | weak (unverified, no setup) |
| Mathematical foundation + efficiency complements existing tools | Assertion | weak |
| Unique insight into secrecy/deception value | Assertion + 2 scenarios named but not shown | weak |

## Limitations
- Authors' stated: unknown (full text unread).
- Identified: paywalled; this note cannot support quantitative modeling; perfect-information framing overstates attacker knowledge; no sensor noise/latency/fusion discussed at abstract level.

## Reproducibility
- Low from abstract. DOI + citation + keywords available. Need full text + JOINT DEFENDER formulation, scenario data, solver settings.

## Key references worth chasing
- Owen (1969) Minimization of Fatalities in Nuclear Attack Model; Bracken et al. (1987) Robust preallocated preferential defense; Moore & Bard (1990) Mixed Integer Linear Bilevel Programming (per IDEAS refs).
- Full text via library/INFORMS subscription: DOI 10.1287/opre.1050.0231.

## Quotable / page-anchored facts
- "We describe JOINT DEFENDER, a new two-sided optimization model for planning the pre-positioning of defensive missile interceptors" [RePEc abstract].
- "For a realistic scenario, we can evaluate a completely transparent exchange in a few minutes on a laptop computer, and can plan near-optimal secret defenses in seconds" [RePEc abstract — quote for scope, not as validated result].
