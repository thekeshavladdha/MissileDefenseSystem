# Missile Defense DED-Lite Demo
### Full Video Script | Approx. 8 Minutes

**System:** VisualSim Architect
**Model:** `MissileDefense_DEDlite.xml`
**Demo Objective:** Compare three missile-engagement policies using kills, leakers, latency, and magazine depletion.

---

## 1. Opening: The Problem
**Time:** 0:00–0:50

### MOUSE
Nothing yet. Face the camera, or display a blank title slide.

### SPEAK
> “Imagine two warships defending one asset against a raid of incoming ballistic missiles.
>
> Each ship has ten interceptors.
>
> The question that decides everything is not how fast the missiles fly. It is **who shoots which threat**.
>
> Fire both ships at the same threat and you waste interceptors. Assign statically and one ship saturates while the other sits idle.
>
> So today I will show you a system-level model that compares three engagement policies side by side, and measures **kills, leakers, latency, and magazine depletion**.”

---

## 2. Opening the Model
**Time:** 0:50–1:30

### MOUSE
Open:

**VisualSim Architect → File → Open**

Navigate to:

```text
VS_AR
└── workflow
    └── models
        └── MissileDefense_DEDlite.xml
```

Let the canvas load. Zoom out until the entire pipeline is visible.

### SPEAK
> “This is our model, built in VisualSim Architect.
>
> Threats flow from left to right.
>
> The top row is shared: **threat generation, assignment, and routing**.
>
> Below it sit our two lookup tables, and to the right the flow splits into two lanes, one per ship, merging back into results on the far right.”

### MOUSE
Slowly sweep the pointer from left to right across the entire canvas once.

**Do not click anything.**

---

## 3. The Model Blocks
**Time:** 1:30–3:30

## 3.1 Threat Generation

### MOUSE
Hover over **ThreatGenerator** (far left, yellow block).

### SPEAK
> “Threats arrive here, about one per second.
>
> Each threat gets a random priority from one to five. Think of it as threat severity.”

---

## 3.2 Detection and Assignment

### MOUSE
Hover over **DetectionAssignment** (red diamond, second from left).

### SPEAK
> “This block assigns the threat its properties:
>
> priority, a firm track, a random command delay between fifty and two hundred milliseconds, and a flyout time computed from range divided by interceptor speed.
>
> It also rolls the kill dice against our kill probability parameter.”

---

## 3.3 Engagement and Magazine Tables

### MOUSE
Move down-left and hover over **FES_DB**, then **Magazine_DB**.

### SPEAK
> “These two tables sit below the flow, deliberately outside it.
>
> The engagement schedule maps priority to a preferred ship.
>
> The magazine table holds each ship's remaining interceptors, ten each at the start, and it is real shared state.
>
> Every shot decrements it.”

---

## 3.4 Common Rule and Policy Router

### MOUSE
Move back up. Hover over **CommonRule**, then down to **PolicyRouter** beneath it.

### SPEAK
> “The common rule reads both tables and recommends a preferred ship, skipping any ship whose magazine is empty.
>
> The policy router just below it then makes the final assignment.
>
> And this is where our three policies live. Notice the split happening right here: one wire leaves upward toward Ship 1, one leaves downward toward Ship 2.”

---

## 3.5 Ship Engagement Lanes

### MOUSE
Follow the upper wire. Hover over each block from left to right:

```text
Ship1_Queue
→ Ship1_C2
→ Ship1_Flyout
→ Ship1_Kill
```

Then follow the lower wire and repeat:

```text
Ship2_Queue
→ Ship2_C2
→ Ship2_Flyout
→ Ship2_Kill
```

### SPEAK
> “Each ship is an identical lane:
>
> a bounded queue, the command delay, the flyout delay, and kill assessment.
>
> Kill assessment checks three things:
>
> Did the dice roll succeed?
>
> Did the interceptor finish before the four-second deadline?
>
> And were there missiles left to fire?
>
> Only all three together count as an **effective kill**.”

---

## 3.6 Results Pipeline

### MOUSE
Move to the far right. Hover over, in order:

```text
Merge
DefenseOutcome
KillCount
MissCount
xTime_yData_Plotter
```

### SPEAK
> “Both lanes merge back here.
>
> Every finished threat lands in the outcome table.
>
> Effective kills and misses are counted separately, and latency is plotted over time.”

---

## 4. The Three Engagement Policies
**Time:** 3:30–4:30

### MOUSE
Go back to **PolicyRouter**. Double-click it so the `Policy_Mode` parameter is visible.

Point directly at the parameter.

### SPEAK
> “One parameter switches doctrine.
>
> **Mode zero is sectored:** low-priority threats go to Ship 1, high-priority threats go to Ship 2. Simple, with no coordination.
>
> **Mode one is first-launch:** everything goes to Ship 1. Ship 2 never fires.
>
> **Mode two is our DED-lite policy:** follow the table recommendation, respect empty magazines, and if a threat misses but time remains, it gets routed back for a genuine second attempt.
>
> **Shoot, look, shoot.**”

### MOUSE
Close the parameter window.

### SPEAK
> “Our headline result from ninety batch runs: mode one is clearly worst, with Ship 2 idle and the most leakers.
>
> Modes zero and two both use both ships. Mode two edges ahead at high kill probability.
>
> I will show you a live run of mode two now.”

---

## 5. Running the Model
**Time:** 4:30–5:00

### MOUSE
Confirm:

```text
Policy_Mode = 2
```

Press the green **GO** button.

Let the simulation run for approximately ten seconds.

Point at threats moving through both lanes.

### SPEAK
> “Running now.
>
> Watch the two lanes share the raid.”

### BACKUP CONDITION

If the license dialog appears:

### SPEAK
> “The license manager needs a moment. Here is the identical recorded run.”

Immediately switch to the backup clip.

**Do not debug on camera.**

---

## 6. Reading the Four Result Windows
**Time:** 5:00–7:00

## 6.1 DefenseOutcome

### MOUSE
Open **DefenseOutcome**.

Scroll slowly through two or three records.

### SPEAK
> “Every finished threat lands here.
>
> We can see the arrival time, completion time, priority, assigned ship, dice result, whether it beat the deadline, shots fired, and magazine remaining.
>
> Follow one threat.
>
> This one arrived at second five and finished at eight-point-five, past the four-second deadline.
>
> It won the kill dice, yet it still counts as a leaker.
>
> That is the whole lesson:
>
> **Even perfect interceptors leak if the timeline slips.**”

---

## 6.2 KillCount

### MOUSE
Open **KillCount**.

Point at the rising numbers.

### SPEAK
> “This is the running total of effective kills, with one line per kill and its timestamp.”

---

## 6.3 MissCount

### MOUSE
Open **MissCount**.

Point at the entries.

### SPEAK
> “And this records everything else: misses and late kills.
>
> Kills plus misses always equals the total number of threats.
>
> That is how we verify that nothing vanished from the simulation.”

---

## 6.4 Latency Plot

### MOUSE
Open **xTime_yData_Plotter**.

Trace the curve from left to right with the pointer.

### SPEAK
> “And here is latency over time.
>
> Early threats finish in about two seconds.
>
> As the queue saturates, latency climbs toward eight.
>
> That slope is the cost of congestion.”

---

## 7. The Money Slide: One Run
**Time:** 7:00–7:40

### MOUSE
Return to **DefenseOutcome**.

Find the final record.

Point at:

```text
Inventory_Left = 0
Magazine_Empty = true
```

### SPEAK
> “In this run: nine threats, four effective kills, with the magazines falling from ten to zero on the final threat.
>
> Ship 1 fired seven times. Ship 2 fired twice.
>
> Nothing went negative, empty ships were routed around, and every number I quoted traces back to a row in this table.”

---

## 8. Summary and Close
**Time:** 7:40–8:30

### MOUSE
Return to the full canvas view.

### SPEAK
> “So what did we build?
>
> A two-ship missile defense model with **file-backed engagement rules, live per-ship magazines with reload, a real shoot-look-shoot loop, and three selectable doctrines**, all validated across ninety seeded runs.
>
> What did we learn?
>
> First, single-ship doctrine loses decisively.
>
> Second, the deadline binds harder than the kill dice. **Late kills are leakers.**
>
> Third, magazines matter. **The defense that runs dry stops defending.**
>
> What is simplified?
>
> There is no radar physics, communications loading is abstracted, and flyout times are simplified. All of those assumptions are documented in our report.
>
> Thank you.”

### MOUSE
Stop recording.

---

## Delivery Notes

### 1. Memorize the structure, not the script

Do **not** try to memorize every sentence.

Memorize this sequence:

```text
Problem
   ↓
Model
   ↓
ThreatGenerator
   ↓
DetectionAssignment
   ↓
FES_DB + Magazine_DB
   ↓
CommonRule
   ↓
PolicyRouter (the split!)
   ↓
Ship1 lane / Ship2 lane
   ↓
Merge
   ↓
Results (table, counters, plot)
   ↓
Three policies
   ↓
Live run
   ↓
Read the four windows
   ↓
Money record (magazine hits zero)
   ↓
Three lessons, close
```

### 2. The anchor story

Your most important demonstration is the **won-the-dice-but-leaked record**:

> **Won the kill dice → missed the deadline → became a leaker.**

Find this record **before** you start narrating that section.

### 3. The four result windows

| Window | What it proves |
|---|---|
| **DefenseOutcome** | What happened to each threat |
| **KillCount** | Effective kills |
| **MissCount** | Misses + late kills |
| **xTime_yData_Plotter** | Latency and congestion |

### 4. Emergency rule

If anything stalls for **more than five seconds**, cut to the backup recording.

Do not debug VisualSim during the presentation.

### 5. The three numbers to emphasize

**4 seconds** — engagement deadline

**10 interceptors per ship** — initial magazine

**90 seeded runs** — validation basis

And the three conclusions:

> **Single-ship doctrine loses.**
> **Late kills are leakers.**
> **Empty magazines stop defense.**
