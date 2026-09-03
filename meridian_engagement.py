"""
Module 8 Practice - Meridian Health Services credentialing engagement.

Quantitative backbone of the lab, so every number in the README is
reproducible by someone else:

  1. Flow analysis of the current credentialing workflow (Exercise 1a)
  2. Driveshaft vs. redesign estimates (Exercise 2c)
  3. Outcome measure with falsification and anti-gaming guard (Exercise 2a)

Run:  python meridian_engagement.py
No dependencies beyond the standard library.
"""

from dataclasses import dataclass, field
from typing import List, Optional

WORKING_DAY_HOURS = 8.0


# ---------------------------------------------------------------------------
# 1. Current state, straight from Meridian's operations table
# ---------------------------------------------------------------------------

@dataclass
class Step:
    name: str
    owner: str
    working_min: float
    wait_days: float            # wait *before* the step starts
    parallel_with: Optional[str] = None  # redesign only: runs alongside this step


CURRENT: List[Step] = [
    Step("Application received, logged", "Intake", 20, 0),
    Step("Completeness check", "Intake", 45, 1.5),
    Step("Primary source verification", "Verification", 210, 5),
    Step("Malpractice history review", "Verification", 90, 2),
    Step("Reference outreach and follow-up", "Verification", 120, 11),
    Step("Committee review preparation", "Analyst", 120, 3),
    Step("Committee decision", "Committee", 15, 7),
    Step("Contract generation and countersign", "Contracting", 60, 2),
    Step("System enablement across 4 systems", "Operations", 90, 1),
]

REPORTED_AVG_DAYS = 34
REPORTED_P90_DAYS = 41
CONTRACT_SLA_DAYS = 30
REPORTED_MISS_RATE = 0.40


def flow_analysis(steps: List[Step]) -> dict:
    working_min = sum(s.working_min for s in steps)
    working_days = working_min / 60 / WORKING_DAY_HOURS
    wait_days = sum(s.wait_days for s in steps)
    elapsed_days = wait_days + working_days
    longest = sorted(steps, key=lambda s: s.wait_days, reverse=True)[:3]
    return {
        "working_min": working_min,
        "working_hours": working_min / 60,
        "working_days": working_days,
        "wait_days": wait_days,
        "elapsed_days": elapsed_days,
        "flow_eff_working_days": working_days / REPORTED_AVG_DAYS,
        "flow_eff_calendar_hours": (working_min / 60) / (REPORTED_AVG_DAYS * 24),
        "longest_waits": [(s.name, s.wait_days) for s in longest],
    }


# ---------------------------------------------------------------------------
# 2a. Driveshaft: AI applied to working time, shape unchanged
# ---------------------------------------------------------------------------

DRIVESHAFT_WORKING_MIN = {
    "Application received, logged": 20,
    "Completeness check": 15,
    "Primary source verification": 120,
    "Malpractice history review": 60,
    "Reference outreach and follow-up": 45,
    "Committee review preparation": 45,
    "Committee decision": 15,
    "Contract generation and countersign": 30,
    "System enablement across 4 systems": 60,
}


def driveshaft(steps: List[Step]) -> List[Step]:
    return [
        Step(s.name, s.owner, DRIVESHAFT_WORKING_MIN[s.name], s.wait_days)
        for s in steps
    ]


# ---------------------------------------------------------------------------
# 2b. Redesign: shape changed. Reference outreach, PSV and malpractice start
#     at day 0 in parallel; consent agenda for clean files; packet generated
#     from the record; enablement driven by a checklist off the record.
# ---------------------------------------------------------------------------

def redesign(clean: bool) -> List[Step]:
    committee_wait = 1.5 if clean else 7.0   # chair consent vs. full committee
    return [
        Step("Logging + completeness pre-screen", "Intake + agent", 30, 0),
        Step("PSV evidence (agent) + human verification", "Verification", 90, 2),
        Step("Malpractice review", "Verification", 60, 0,
             parallel_with="PSV evidence (agent) + human verification"),
        Step("Reference outreach (agent sends, human escalates)", "Verification",
             60, 6, parallel_with="PSV evidence (agent) + human verification"),
        Step("Packet generated, analyst review", "Analyst + agent", 30, 0.5),
        Step("Chair consent (clean) / committee (flagged)", "Committee", 15,
             committee_wait),
        Step("Contract generation", "Contracting", 30, 1),
        Step("Enablement checklist", "Operations", 45, 0.5),
    ]


def critical_path_days(steps: List[Step]) -> float:
    """Elapsed days: parallel branches contribute only their longest member."""
    groups: dict = {}
    order: List[str] = []
    for s in steps:
        key = s.parallel_with or s.name
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(s)
    total = 0.0
    for key in order:
        branch = groups[key]
        total += max(s.wait_days + s.working_min / 60 / WORKING_DAY_HOURS
                     for s in branch)
    return total


# ---------------------------------------------------------------------------
# 3. Outcome measure (Exercise 2a): the number, its guard, its falsifiers
# ---------------------------------------------------------------------------

@dataclass
class OutcomeReading:
    """One cohort reading, produced by outcome_measure.sql against ServiceNow."""
    on_time_rate: float          # share of files enabled within 30 days
    p90_days: float
    intake_volume: int           # files received in the cohort window
    baseline_volume: int         # files received in the baseline window
    defect_rate: float           # blind 10% re-review, material errors
    baseline_defect_rate: float
    billable_mismatch: float     # share of "enabled" files not yet billable
    notes: List[str] = field(default_factory=list)


TARGET_ON_TIME = 0.85
TARGET_P90 = 30
MAX_VOLUME_DROP = 0.20
MAX_DEFECT_INCREASE = 0.01
MAX_BILLABLE_MISMATCH = 0.02


def evaluate(reading: OutcomeReading) -> dict:
    """Returns pass/fail plus every falsifier that fired. Failing any one
    means the primary result does not count, whatever the on-time rate."""
    fired = []
    if reading.on_time_rate < TARGET_ON_TIME:
        fired.append(f"on-time {reading.on_time_rate:.0%} < {TARGET_ON_TIME:.0%}")
    if reading.p90_days > TARGET_P90:
        fired.append(f"p90 {reading.p90_days} > {TARGET_P90} days")
    drop = 1 - reading.intake_volume / reading.baseline_volume
    if drop > MAX_VOLUME_DROP:
        fired.append(f"intake volume down {drop:.0%} (less work, not a faster process)")
    if reading.defect_rate - reading.baseline_defect_rate > MAX_DEFECT_INCREASE:
        fired.append("verification defect rate rose above baseline + 1pt (gaming guard)")
    if reading.billable_mismatch > MAX_BILLABLE_MISMATCH:
        fired.append("'enabled' set before provider is billable (checked vs mainframe)")
    return {"passed": not fired, "falsifiers_fired": fired}


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def pct(x: float) -> str:
    return f"{x * 100:.1f}%"


def main() -> None:
    cur = flow_analysis(CURRENT)
    print("== Exercise 1a: current state ==")
    print(f"Working time      : {cur['working_min']:.0f} min = "
          f"{cur['working_hours']:.1f} h = {cur['working_days']:.2f} working days")
    print(f"Wait time         : {cur['wait_days']} days")
    print(f"Elapsed (computed): {cur['elapsed_days']:.1f} days  "
          f"(reported {REPORTED_AVG_DAYS} avg, {REPORTED_P90_DAYS} p90)")
    print(f"Flow efficiency   : {pct(cur['flow_eff_working_days'])} on working days, "
          f"{pct(cur['flow_eff_calendar_hours'])} on calendar hours")
    print("Longest waits     :")
    for name, d in cur["longest_waits"]:
        print(f"  - {name}: {d} days ({d / cur['wait_days']:.0%} of wait)")
    verif_wait = sum(s.wait_days for s in CURRENT if s.owner == "Verification")
    print(f"Wait queued in front of the verification team: {verif_wait} of "
          f"{cur['wait_days']} days -> the true constraint")

    print("\n== Exercise 2c: driveshaft (shape unchanged) ==")
    ds = flow_analysis(driveshaft(CURRENT))
    print(f"Working time {cur['working_min']:.0f} -> {ds['working_min']:.0f} min "
          f"({1 - ds['working_min'] / cur['working_min']:.0%} less)")
    print(f"Elapsed {cur['elapsed_days']:.1f} -> {ds['elapsed_days']:.1f} days "
          f"({1 - ds['elapsed_days'] / cur['elapsed_days']:.1%} less). "
          "The 30-day miss rate barely moves.")

    print("\n== Exercise 2c: redesign (shape changed) ==")
    clean = critical_path_days(redesign(clean=True))
    flagged = critical_path_days(redesign(clean=False))
    print(f"Clean file critical path  : {clean:.1f} days")
    print(f"Flagged file critical path: {flagged:.1f} days")
    for share in (0.6, 0.7, 0.8):
        blended = share * clean + (1 - share) * flagged
        print(f"  blended avg if {share:.0%} of files are clean: {blended:.1f} days")
    print("Clean/flagged split is an ASSUMPTION until measured in week 1.")

    print("\n== Exercise 2a: outcome evaluation, worked examples ==")
    good = OutcomeReading(0.88, 27, 190, 200, 0.031, 0.030, 0.01)
    gamed = OutcomeReading(0.90, 26, 195, 200, 0.055, 0.030, 0.01)
    starved = OutcomeReading(0.91, 25, 120, 200, 0.030, 0.030, 0.00)
    for label, r in (("genuine improvement", good),
                     ("fast but quality slipped", gamed),
                     ("fast because volume collapsed", starved)):
        res = evaluate(r)
        verdict = "PASS" if res["passed"] else "FAIL"
        print(f"  {label:32s}: {verdict} {res['falsifiers_fired']}")


if __name__ == "__main__":
    main()
