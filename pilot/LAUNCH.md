# Launch one account before paying for automation

This is a manual, low-cost pilot. Nothing in this kit creates an account, posts to Instagram, purchases anything or sends a ChatGPT notification. The API-based daily prototype remains available separately, but is not needed here.

**Editorial update:** the original seven concept/opinion drafts are archived prototypes. New posts must follow the [documentary factual standard](research/FACTUAL-STANDARD.md): named cases, verified sources and attributed quotes, with no editorial opinion. Do not schedule the old concepts as if they meet the updated case-reporting requirement. The first case posts remain blocked pending source access and verification.

## Account setup — user action

**Current status:** You confirmed **@PEUnderScrutiny**. Instagram access is pending appeal as reported on October 25, 2026. Use [tonight's checklist](TONIGHT.md) to prepare assets while waiting. Account creation below is background guidance; do not create a replacement account just to work around the pending appeal.

1. Create a dedicated Instagram account using your own email and enable two-factor authentication. Choose a **professional Business or Creator** account for insights and scheduling. Do not share your password or recovery codes in chat.
2. Suggested display name: **PE Under Scrutiny**. Suggested handle: `@peunderscrutiny`, with `@thebuyoutbrief` as an alternative. Availability has not been checked; choose an available handle during signup. No organization, regulator or news outlet affiliation is implied.
3. Suggested bio (under 150 characters):

   > Private equity, examined. Customers. Workers. Competition. Evidence-led explainers. Opinion labeled. Corrections welcome.

4. Use a simple typographic avatar initially. No domain, paid logo, hosting plan, API key or Meta developer app is required for this pilot.
5. Connect the Instagram professional account to a Facebook Page you manage if required for your Meta Business Suite configuration. Use Meta's official account interfaces to connect it. The manual scheduling route does not require the publishing token used by the custom app.
6. Check that you can create a post and view professional insights. Scheduling and insight availability can differ by account and interface. If scheduling is unavailable, post manually through Instagram; do not buy software just to bypass that initial check.

## First week

The seven JPEGs are headline cards. Each has a matching caption text file. The export contains **drafts, not approved posts**. In this workspace the primary-source sites returned a network-policy error, so all referenced sources require review. The captions avoid company-specific allegations and numerical claims. That does not replace editorial review.

1. Read `REVIEW-BEFORE-PUBLISHING.md`. Open the cited agency documents and verify the passages supporting posts 2, 3 and 4. The merger posts discuss the **2023** document; do not silently describe it as verified current policy. For post 2, confirm that the background reference actually supports the leveraged-buyout description or replace it with a more direct authoritative source.
2. Edit each caption and mark its checklist. For a verified reference, replace “Source reference (review before publishing)” with “Source” in the caption. If verification fails, omit that post until it is corrected. Never publish the review checklist itself as a caption.
3. Review the actual JPEG. The text-file caption and JPEG are separate: editing a caption does not redraw the image. To change a headline, edit the batch JSON and export into a **new** output folder so old reviewed assets remain intact.
4. In Meta Business Suite, choose the connected Instagram account, create the post, upload the matching JPEG, paste the caption, and inspect the preview. After you approve the final version, schedule it for **9 p.m. America/New_York**, one per day. This follows Eastern daylight saving time. Choose your own launch date; the files do not assume you launch today.
5. Respond to substantive comments. Ask for source links, avoid publishing private/confidential information, and correct errors visibly. Do not turn a commenter's story into an unverified accusation.

Aim to learn from seven posts, not to claim a format is proven from one impression. If a batch has only a handful of views, the evidence is too weak to declare that the topic failed. Check distribution and execution as well as the content.

## Repeat weekly in your existing ChatGPT account

Return to the same conversation and paste the measurements plus this request. This is a manual prompt, not a scheduled ChatGPT message:

> Research up to seven case-specific factual Instagram posts for PE Under Scrutiny. No editorial opinions, moral labels or generic mission posts. Use named companies, verified ownership dates, primary documents and credible corroboration. Distinguish allegations, findings, settlements, measured outcomes and research associations. Do not infer causation from timing or call every acquisition a monopoly. Cite exact source URLs and dates and identify sources you actually read. For every direct quote, give exact wording, speaker, date and page/paragraph plus context; omit it if the wording cannot be verified. Include material company responses and limitations. If browsing or evidence is unavailable, return a research queue and verification requirements, not invented facts or substitute opinion drafts. Fewer verified posts are better than filling a quota. For each supported case give a factual hook, a five-card outline, a 30–60-second narration script, a caption under 1,800 characters including sources, a claim/source table, and a review checklist. No paid narration until the script is approved. Nothing is approved, scheduled or published unless I explicitly approve the final assets. Here are last week's measurements: [paste summary].

No API credits are required for this route. Your existing ChatGPT account's model, research and usage limits still apply. It cannot guarantee an automatic message at 9 p.m. without a separately supported scheduled-task feature. No such task is connected here.

Export a future reviewed batch locally:

```sh
.venv/bin/python -m antipe pilot --batch path/to/week-02.json --output .local/pilot/week-02
```

The exporter does not overwrite an existing output directory or ZIP. It never calls OpenAI or Meta. The schema still expects seven uniquely identified drafts. Keep claims in the JSON consistent with the actual evidence; a valid file is not a fact check.

## Measure influence and profitability separately

Use `metrics.csv` for posts and `weekly-review.csv` for the eight-week experiment. Record a post's metrics **48 hours after publication** so comparisons use a similar window. Blank means unavailable/not measured; enter `0` only for a measured zero. Some accounts provide only account-level or different insight metrics; leave unsupported attribution blank. Caption URLs are not clickable on Instagram, so source clicks may be unmeasurable without a separate tracked link-in-bio destination. Do not buy one just for this pilot.

- Save/share rate: `(saves + shares) / reach`, only when reach is positive and the measurements are available. Report the counts alongside the rate; tiny denominators can mislead.
- Follower conversion: `attributed follows / reach` only if post-level attribution is actually provided. Weekly follower change is a separate account-level measure and should not be assigned to one post.
- Cash profit: `actual revenue - cash expenses`.
- Economic profit: `actual revenue - cash expenses - labor hours × your chosen hourly value`. Count research, editing, scheduling and moderation time. A low server bill does not make the project profitable if it consumes many hours.

Do not assume Instagram will pay you. Budget **$0 revenue initially**. Track only money actually earned. Later revenue experiments might include voluntary support or a disclosed sponsorship relevant to the audience; investigate terms and audience trust before committing. Evaluate influence using useful reach, shares, thoughtful responses and follower retention, not follower count alone.

## Eight-week decisions

- Weeks 1–2: establish the account, verify the posting process and capture baseline metrics. Avoid ads and paid tools.
- Weeks 3–4: repeat promising formats and change one variable at a time, such as hook or topic. Compare several posts per format, not a single outlier.
- Weeks 5–6: concentrate on the two formats with the best combination of useful engagement, follower conversion and sustainable production time. Look for recurring audience questions.
- Weeks 7–8: decide whether to continue, narrow the subject, or stop. Write down the evidence and uncertainty. There is no universal follower threshold that proves this business will work.

Add automation only when repetitive work is a meaningful burden and results justify the cost. If research is the time sink, buying a scheduler will not solve it. If you later test another account, give it a distinct editorial focus and track its results separately rather than paying to duplicate the same unvalidated process.

## Costs and next action

Pilot software outlay: **$0 incremental** if your current ChatGPT plan and free Meta tools are sufficient, excluding your time and existing subscription. No purchases have been made. The custom daily automation prototype is optional and still needs credentials, hosting and live validation.

Your account handle is **@PEUnderScrutiny**. Prepare the offline assets now, review the first seven drafts together, and complete profile/account connection after the appeal is resolved and access is restored. There is no supported Instagram connection in this chat, so account settings and the Meta connection must happen in your own account interfaces.
