# AAR 20260701.142823: Question prioritization

## Scope

Added an explicit question-prioritization rule to the deep-interview skill.

## What happened

The user pointed out that recursion was blowing up because the question list was too abstract and unprioritized. I updated the skill so questions are prioritized by domain and leverage, and same-domain questions are combined unless splitting materially changes the answer. I also added the corresponding note to the working interview file.

## Process issues

The prior recursive interview structure allowed too many same-domain questions to accumulate.

## Proposed follow-up improvements

- Add a question queue template with domain/leverage tags.
- Consider capping the number of active questions per domain.

## Candidate ADR or implementation topics

- Question queue prioritization and merge policy.

## Current status

Deep interview questions are now explicitly prioritized and mergeable by domain.
