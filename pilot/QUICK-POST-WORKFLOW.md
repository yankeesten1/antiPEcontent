# Five pitches → one finished reel

The user selected automatic preparation with manual Business Suite upload. The
editorial reference is the consumer-focused USAP reel. Use Heart, music, stationary
frames and clean cuts, a specific consumer/worker consequence, plain language,
brief attribution and the material response. Full sourcing and dates belong in
the caption. Each new post needs approval of its own final video and caption.

## What the user does

1. Open the daily pitch pack, skim the five numbered stories and reply in our
   working conversation with a number and any changes.
2. Review the selected story's finished video and caption after source review and
   rendering. Ask for edits or approve that version.
3. Download the video, paste the caption into Meta Business Suite, check the crop
   and audio, and publish or schedule. Nothing in this workflow publishes.

The selected pitch still needs editorial work: check the primary records, exact
quotes, ownership and material response; create a source-reviewed `case.json`
and captured source text. The assistant can do that in an active work session.
That step is **not an unattended fact-checker** and is not yet automatically
triggered by picking a number. The HTML review pack is an offline reading page;
it does not send a selection or notify this chat.

## GitHub setup and activation

The workflow is `.github/workflows/next-post.yml` on branch
`codex/pe-content-pilot`. It must reach the repository's default branch before its
scheduled runs work and before it normally appears for manual dispatch in Actions.
No merge, paid API connection or scheduled activation has been performed here.

1. Review and merge the branch's workflow/code into the default branch.
2. In GitHub Actions, open **Prepare next post → Run workflow → sample**. This
   creates a sample review pack without calling a paid model. Samples are not
   researched post candidates. Download the run's `daily-pitches-...` artifact;
   open `review.html` or `PITCHES.md`.
3. Before paid runs, review current model/search pricing and configure provider
   spending controls. ChatGPT subscription billing does not cover API usage.
   Token limits and attempt suppression are not a hard dollar cap; provider
   alerts may also be advisory. Private-repository Actions minutes/storage may
   incur charges beyond the account's allowance. Heart has no speech API fee.
4. Add an OpenAI API key as repository **Actions secret `OPENAI_API_KEY`** using
   GitHub's settings. Never paste it in chat or commit it. Optionally set repository
   variable `ANTIPE_MODEL` (code default: `gpt-4.1`). Adding the secret and running
   `pitches` makes paid research/generation requests.
5. Run **pitches** once manually and review quality/usage before enabling recurring
   runs. Set repository **Actions variable `ENABLE_DAILY_PITCHES` to `true`** only
   when ready for daily paid generation. Remove it or set it to `false` to stop.

The schedule targets approximately **9 p.m. America/New_York**, switching between
standard and daylight time. GitHub schedules can be delayed or skipped. The job
checks the local hour; a run delayed beyond that hour may be skipped. There are
no ChatGPT messages or external notification integrations. Retrieve packs from
GitHub Actions; notification behavior depends on the user's GitHub settings.

Each pitch batch makes up to two Responses API calls, with one web-search tool
call allowed in the research stage, and output-token limits. It generates five
text candidates and no video. The SQLite batch record prevents automatic retries
in the same persisted state. Actions caches the daily attempt, including failures,
to suppress duplicate requests. Cache eviction, runner interruption or deliberate
cache deletion can defeat this safeguard; it is not a financial guarantee. Check
the original run and provider usage before retrying a failed batch. No research
can be guaranteed sufficient for five distinct source-supported stories; the
generator is instructed to refuse rather than invent missing cases.

## Render the selected case

After editorial source review and case preparation, commit the reviewed case and
source snapshots to the chosen branch. In **Prepare next post → Run workflow**,
choose **render**, that branch, and the case file under `pilot/cases/.../case.json`.
Download the `post-ready` artifact. It contains the video, caption, card preview,
spoken script and review notes. Rendering uses local Heart and FFmpeg without
model API calls. GitHub execution/storage allowances still apply.

Hash/quote/reference checks validate the input records' integrity; they do not
establish the truth or semantic support of a claim. Final approval is separate
from source review and never inherited from approval of an earlier post.

## Local equivalents

```sh
# No API calls; sample review-flow check only.
.venv/bin/python -m antipe pitches --demo --output .local/sample-pitches-new

# Paid research and generation, only with securely configured API credentials.
.venv/bin/python -m antipe pitches --output .local/daily-pitches-new

# No paid API; requires the optional local voice setup and FFmpeg.
.venv/bin/python -m antipe case --file pilot/cases/SELECTED/case.json --output .local/post-ready-new
```

The local pitch command uses the configured Eastern editorial date, preserves
earlier output folders, and records failed attempts rather than silently retrying.
