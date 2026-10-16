# Pattern: Command Safety

Classifies a proposed tool call as SAFE, REVIEW, or BLOCK before it runs.

## Inputs

Tool name, arguments, target environment, and the user request.

## Options

`SAFE`, `REVIEW`, `BLOCK`.

## Wiring

Map the choice and confidence to an action: run, ask a human, or refuse.
See `app/guard.py`.

## Limits

Accuracy depends on the labeled set in `eval/`.
