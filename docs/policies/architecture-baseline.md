# Architecture Baseline

## Purpose

This document is the empty architecture-baseline template for future reviews.
It records the shape of the observed-state baseline that reviewers should fill
from current evidence when a review scope needs architecture context.

It is not a list of decisions.

It is not a refactor plan.

It is not, by itself, an observed architecture claim until its placeholder rows
are replaced with evidence-backed entries.

## Observed modules

| area | modules/files | notes |
|---|---|---|
| core/schema | replace with evidence-backed paths | template row |
| runtime | replace with evidence-backed paths | template row |
| UI | replace with evidence-backed paths | template row |
| Petri-net/backend | replace with evidence-backed paths | template row |
| adapters | replace with evidence-backed paths | template row |
| tests | replace with evidence-backed paths | template row |

## Observed dependency edges

| source | target | status |
|---|---|---|
| replace with evidence-backed source | replace with evidence-backed target | intended / questionable / legacy / unknown |

## Known problems

| id | area | issue | status | next action |
|---|---|---|---|---|
| example | replace with area | replace with observed issue | candidate / accepted legacy | replace with next action |

## Current target assumption

The working assumption is:

Core schema should remain independent of runtime, UI, Petri-net backends,
process-mining libraries, and external adapters.

This assumption can be changed only by human decision.
