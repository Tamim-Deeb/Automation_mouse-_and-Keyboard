# Quickstart: Default Step Delay

## How to Use

1. **Open the application** — the execution panel shows a "Delay (ms)" field with a default value of 200
2. **Build your workflow** — add steps as usual (clicks, typing, hotkeys, etc.)
3. **Adjust the delay** — change the "Delay (ms)" value to control the pause between steps:
   - `0` = no delay (steps run as fast as possible)
   - `200` = 200ms pause after each step (default)
   - `1000` = 1 second pause after each step (good for slow applications)
4. **Click Start** — the workflow runs with the configured delay between each step
5. **Press Esc** to stop at any time, even during a delay pause

## What It Does

- Inserts an automatic pause after every workflow step during execution
- Does NOT add visible steps to the workflow builder — the delay is an execution setting only
- The delay value is remembered between sessions — you don't need to re-enter it

## Testing Checklist

- [ ] Set delay to 1000ms, run a 3-step workflow → observe ~1s pause between each step
- [ ] Set delay to 0ms → steps execute with no artificial pause
- [ ] Press Esc during a delay pause → execution stops within 1 second
- [ ] Close and reopen the app → delay field retains the last value you set
- [ ] Run with Dry Run enabled → delay still applies between simulated steps
- [ ] Enter a non-numeric value → input is rejected
- [ ] Workflow with explicit WAIT steps → both the WAIT duration and the default delay are applied
