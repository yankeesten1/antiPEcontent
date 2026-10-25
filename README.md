# PE / Under scrutiny

A private editorial inbox for educational Instagram content about private equity's impact on customers, workers and competition. Five researched drafts per day, automatic JPEG graphics, editable captions, source links and explicit approval before publication. Defaults to **9 p.m. America/New_York** (Eastern local time, including daylight saving time).

**Current editorial direction:** named, documented cases; no editorial opinion or moral labels. Read the [factual standard and source requirements](pilot/research/FACTUAL-STANDARD.md), [research queue](pilot/research/case-queue.json), and [audio plan](pilot/AUDIO-PLAN.md). The original weekly opinion/concept drafts and ZIPs are archived prototypes, not the publication plan. FTC, GAO and SEC pages are now accessible; some medical-publisher/abstract requests still return access challenges.

**First case for review:** [USAP case video with Heart](pilot/cases/usap/case-heart.mp4), [six-card preview](pilot/cases/usap/carousel-preview.jpg), [source notes](pilot/cases/usap/SOURCES.md), [caption](pilot/cases/usap/caption.txt), and [full review kit](pilot/cases/usap/review-kit.zip). It quotes an FTC complaint and reports the denial, dismissal, separate consent order and April 2026 preliminary agreement. The source snapshots and quote were checked against primary records; the case is **not approved, scheduled or published**. Coverage ends April 23, 2026; later docket events and final implementation were not independently verified. This is a dated case file, not a current-status news alert.

Reproduce this case locally after the voice setup:

```sh
.venv/bin/python -m antipe case --file pilot/cases/usap/case.json --output .local/cases/usap-new-review
```

The renderer checks snapshot hashes, verbatim quoted wording, claim/source references and caption length before creating assets. These structural checks are not an automatic fact checker. A user must review and approve the final content before posting.

**Account setup:** the user can access Instagram's profile editor and has uploaded the logo. Public-name editing, Creator conversion and the Facebook Page/Business Suite connection are covered in [the account guide](pilot/ACCOUNT-SETUP.md). A live connection or publication has not been verified.

**Selected voice: Heart (`af_heart`).** [Watch the Heart-narrated cut](pilot/introduction-heart.mp4) or [download the Heart production kit](pilot/heart-production-kit.zip). Fixed frames, clean cuts and the established music mix are retained. Voice selection does not approve publication. The earlier [Sarah cut](pilot/introduction-fixed-neural.mp4) and [music-only comparison](pilot/music-only-fixed.mp4) remain available for reference. The user rejected the older Flite/zoom cut; old audio/video ZIPs remain archived and should not be treated as the latest version. The replacement uses local Kokoro neural narration and a newly arranged instrumental, with no paid speech service. See [model provenance and setup](pilot/VOICE-SOURCES.md). This is still an introduction/style preview, not a verified case report.

**Free voice choices:** [compare six same-script auditions](pilot/voice-comparison/README.md), [listen to the combined MP3](pilot/voice-comparison/all-six-voices.mp3), or [download the audition pack](pilot/voice-comparison.zip). It includes Sarah (the previous voice), Heart, Bella, Michael, Emma and George. You selected Heart; all new video exports default to `af_heart`. To export auditions locally: `.venv/bin/python -m antipe compare-voices --output .local/pilot/voices-new`. To render a selected voice, add `--voice af_heart --voice-speed 1.0` to the social audio command (using the selected key). British voices use British-English phonemization. No paid speech service or additional model download is needed for these voices.

## Start with the free manual pilot

**Latest visual direction:** [preview the five-card carousel](pilot/introduction-preview.jpg). Videos now use stationary frames and clean cuts, with no slow zoom, pan or scale animation. The fixed-frame/neural-audio links above are the current cuts. Both formats remain drafts for review, and the rest of the week has not yet been redesigned.

Reproduce the new visual prototype locally:

```sh
.venv/bin/python -m antipe social --video --output .local/pilot/introduction-v2
```

For the replacement local neural narrator:

```sh
.venv/bin/python -m pip install -r requirements-voice.txt
.venv/bin/python -m antipe prepare-voice
.venv/bin/python -m antipe social --audio-preview --output .local/pilot/fixed-frames-new
```

FFmpeg with H.264 encoding is required for `--video`; omit that flag for carousel-only export. Rendering uses Pillow and local FFmpeg, with no model/API calls. DejaVu Sans Condensed is used when installed, with a Pillow font fallback. This video feature has been validated on the current machine, not in the optional Docker image, which does not install FFmpeg by default.

The selected launch path is now **one account, seven weekly drafts, and manual Meta Business Suite scheduling**. It requires no OpenAI API key, paid hosting or developer token. The daily automation below remains an optional prototype and has not been connected to live services.

Download the prepared [first-week launch kit](pilot/launch-week-01.zip), or read the [launch guide](pilot/LAUNCH.md) and [editable draft content](pilot/week-01.json) on GitHub. The ZIP contains seven graphics, matching captions and tracking sheets; its factual drafts still require source review before publication.

While Instagram reviews the account, use the expanded [tonight kit](pilot/tonight-kit.zip) and [tonight's checklist](pilot/TONIGHT.md). Unzip the kit and open `review.html` for offline caption editing and downloads. It also includes a circular-crop profile image, copy-ready bio, and a first-post review sheet. Nothing connects to Instagram or publishes from that page.

```sh
.venv/bin/python -m antipe pilot --launch-assets --output .local/pilot/tonight-kit
```

An optional, manually triggered [GitHub Actions workflow](.github/workflows/build-launch-kit.yml) builds future kits without a server or API secrets. It must first be available on your default branch. See the checklist for steps, artifact downloads and GitHub allowance considerations. No remote workflow run or Meta account connection has been verified.

```sh
.venv/bin/python -m antipe pilot --output .local/pilot/week-01
```

This exports seven 1080×1080 JPEGs, matching caption files, a review checklist, post metrics, an eight-week review sheet, and a ZIP. It never calls OpenAI or Meta and refuses to overwrite existing exports. Read [the launch guide](pilot/LAUNCH.md). First-week sources could not be retrieved through this workspace's network policy, so the factual drafts are **not source-verified or approved**. Review their references before publication. The user-confirmed account is **@PEUnderScrutiny**, under appeal as reported on October 25, 2026. This program has not connected to it, scheduled posts, connected ChatGPT notifications or made purchases.

## Try it locally

Requires Python 3.12+.

```sh
cd /workspace/antiPEcontent
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m antipe generate --demo
.venv/bin/python -m antipe serve
```

On your own computer, open the local server on port 8000. Cloud onboarding does not provide a supported localhost preview. The five sample concepts are labeled and **cannot be published**. Graphics and SQLite data are retained under `.local/`, which is excluded from Git.

## Available features and external requirements

| Feature | Status |
| --- | --- |
| Sample concepts, JPEG cards, inbox and caption editing | Works locally without credentials |
| Five sourced daily drafts | Implemented; requires OpenAI API key, web-search/model access and billing |
| Approval and immediate Instagram publication | Implemented; requires Meta credentials and public JPEG hosting |
| Daily messages inside ChatGPT | **Not implemented or connected.** An ordinary external program cannot inject messages into this conversation. This needs a supported ChatGPT integration or a separately configured ChatGPT scheduled task, if available in your account. |
| Conversational editing | Bring a draft to ChatGPT for collaborative editing, then paste the revision into the inbox. There is no in-app chat. |
| Always-on scheduling | Works while the server stays running; this development environment is not production hosting |

The app does not provision accounts, hosting or Meta app approval. Tests simulate external providers. Live generation and publication remain unverified until credentials and hosting are configured.

## Go live

1. Create the dedicated Instagram account and switch to **Business or Creator**. This implementation uses **Instagram API with Facebook Login**: link the professional account to a Facebook Page you manage. Instagram Login is a different integration. Consumer personal accounts cannot publish through this API.
2. Create a Meta developer app, configure Instagram publishing, and obtain the numeric professional account ID and a suitable user access token. Common permissions include `instagram_basic`, `instagram_content_publish`, `pages_show_list`, and `pages_read_engagement`; exact requirements, app roles, review and live mode depend on the app and account. Follow Meta's current documentation. An Instagram password is not an API token. Token renewal is not implemented.
3. Deploy on a host that stays awake with persistent storage for the database **and** JPEGs, behind an HTTPS reverse proxy. Set a strong `ANTIPE_PASSWORD` before binding to a public interface. The inbox uses HTTP Basic authentication; HTTPS is required on a deployed site. Only `/media/<hash>.jpg` is public so Meta can fetch post graphics. Do not expose port 8000 directly to the Internet. This is a single-editor application, not a public multi-user service.
4. Inject `OPENAI_API_KEY`, `META_ACCESS_TOKEN`, `INSTAGRAM_ACCOUNT_ID`, and `ANTIPE_PASSWORD` securely through the host's environment settings. Do not paste them into chat or commit them. `.env.example` documents names; the app does not load that file automatically. Set `ANTIPE_PUBLIC_URL` to the public HTTPS origin **before** generating drafts; generated JPEGs then receive public URLs automatically. A path prefix is not supported. For existing drafts, enter the image URL in the editor.
5. Run `python -m antipe serve --host 0.0.0.0`. The scheduler checks every 30 seconds and claims at most one batch per local day. Restarting after 9 p.m. generates today's missing batch. Previous missed days are not backfilled. Failed batches require an explicit retry after fixing the cause.
6. Review sources, edit your chosen caption and review the exact public image. **Approve & publish** saves that revision and immediately sends it to Instagram. Nothing publishes on a timer. At most one draft per daily batch can enter publication. Editing clears previous approval. The automatic graphic is a headline typography card; its art-direction brief is informational. Supply another public JPEG URL to replace the graphic.

Container build:

```sh
docker build -t antipe .
```

Configure hosting to inject environment variables and mount persistent storage at `/app/.local`, writable by UID 10001. Place it behind HTTPS. Use one scheduler deployment; SQLite deduplicates processes sharing the same filesystem, not separate replicas with separate volumes. Back up the database and images together. Docker deployment has not been exercised in this workspace.

Required outbound hosts: `api.openai.com` and `graph.facebook.com`. OpenAI handles research search requests. Meta must be able to fetch your image host without authentication. Built-in graphics are 1080×1080 JPEGs; custom images must satisfy Meta's current size and format requirements. Captions are limited to 2,200 characters including source URLs. Instagram caption URLs are plain text, not clickable; a separate link-in-bio source page is not implemented.

## Research and review

The first OpenAI Responses API request uses web search to research five ideas, preferring regulatory documents, court records, company disclosures and credible studies. A second request turns that research into five drafts. Citation IDs must match URLs actually returned in the research response. Those source URLs are appended to captions. This validates citation references, **not** the truth of every claim or interpretation. Check source support, dates, figures and causal claims before approval. Caption edits can change whether a citation supports the text.

The current generator prompt requires case-specific factual reporting without editorial opinions. It distinguishes allegations, established findings, settlements, research associations and measured outcomes, and requires ownership dates, attribution and material responses. It must not pad a quota when research is insufficient. Source-ID validation does not verify quotations or establish causation: the human source-review requirement remains. It does not monitor Instagram comments, automate engagement or provide legal review.

## Schedule and recovery

- Defaults: `ANTIPE_TIMEZONE=America/New_York`, `ANTIPE_DAILY_TIME=21:00`. For fixed EST year-round instead of Eastern local time, use `ANTIPE_TIMEZONE=Etc/GMT+5`.
- `python -m antipe generate`: generate now, at most once per local day. Two model requests plus search can incur charges. Scheduled and manual runs share the same daily claim.
- `python -m antipe generate --retry`: explicitly retry a failed daily batch. Successful batches are retained.
- A crash during generation leaves the batch `generating`. Confirm no generation process is active, back up SQLite, then have an operator mark the abandoned batch `failed` before using `--retry`. Automatic crash recovery is not implemented, to avoid unexpected repeated API charges.
- A publishing failure leaves `publishing` or `publish_unknown`. **Do not blindly retry:** Meta might already have accepted the post. Check Instagram and the saved `container_id` using Meta's container-status API. Manual reconciliation is required; there is no recovery button in this version.
- Keep custom image URLs immutable. Generated image filenames are derived from their contents and version; generated cards do not change after creation.

## Cost-conscious pilot

The default workflow makes two model requests per successful day: one research request (at most one web-search tool call) and one drafting request. Research is capped at 5,000 output tokens and drafting at 6,000; these are request limits, not a dollar budget or quality guarantee. Paid retries are explicit. Graphics use local Pillow rendering, with no image-model charges. No paid scheduler, database service or social-media management subscription is required. Model choice is configurable, but a cheaper model must support web search and structured output and should be evaluated for research quality.

Planning estimates for one account: **$3–$10/month API usage**, **$5–$12/month shared hosting**, and an optional **$10–$20/year domain**, roughly **$10–$25/month total** before ads, subscriptions, taxes and editorial labor. These are estimates, not verified current provider prices or quotes. Check current model, search, hosting and renewal prices before purchasing. ChatGPT subscriptions do not include API credits. Public posting through Meta's standard publishing API does not normally have a per-post fee, but account access and permissions are still required.

For a lower-risk demand test, use an existing ChatGPT plan to prepare a weekly batch and schedule posts manually in Meta Business Suite. That can have $0 incremental software cost within existing plan limits, removes API/hosting integration work, and makes it easier to test the editorial idea before automating it. Weekly batching is a suggested alternative; the implemented default remains five drafts daily at 9 p.m. Eastern.

The current app connects one Instagram account per configured instance. Multiple instances can share a small host if resources allow, with separate databases and credentials, so each additional account need not require a separate hosting subscription. This has not been load-tested. Start with one account and several distinct content formats, measure shares/saves, follower conversion, source clicks, production time and actual revenue over 6–8 weeks. Assume $0 revenue in the initial budget; influence and profitability are separate outcomes, and monetization eligibility or payment from Instagram is not guaranteed.

## Validate

```sh
python -m unittest discover -s tests -v
```

Tests cover daily deduplication, Eastern scheduling, source-reference validation, JPEG generation, approval invalidation, single-choice publication, duplicate prevention, uncertain publication and HTTP/CSRF behavior. Verify real OpenAI results, Meta authorization and public image access after connecting external services.

The introduction redesign is checked by rendering five 1080×1350 JPEGs, inspecting the 1080×1920, 24 fps H.264/YUV420p video with FFprobe, and sampling frames within each scene to check that their geometry remains stationary. Audio duration, streams and loudness are checked separately. These checks do not establish Instagram reach, subjective voice quality or publishing success.

Official references: [OpenAI web search](https://platform.openai.com/docs/guides/tools-web-search), [Meta publishing](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/content-publishing), [Meta access tokens](https://developers.facebook.com/docs/facebook-login/guides/access-tokens).
