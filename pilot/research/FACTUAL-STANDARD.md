# Documentary case reporting: the new editorial standard

New case posts must contain **no editorial opinion, moral ranking or generic mission filler**. The goal is to report specific, documented outcomes involving private equity. Engagement is measured after publication; it cannot be promised from how shocking a case sounds.

## What a case needs before writing the final script

1. **Ownership:** named business, investor, transaction date, investment type and ownership at the time of the outcome. Do not label every financial owner “private equity,” or attribute an event to an investor that had already exited without evidence of the connection.
2. **Outcome:** a precise, dated, sourced change in jobs, closures, prices, competition, quality or another defined measure. Preserve geography, denominator, comparator and time window. Do not substitute an impression for a measurement.
3. **Mechanism:** the records supporting the relationship between the transaction and the outcome. A before/after timeline is not enough to establish cause. If the causal link is unestablished, say so in the video itself.
4. **Quotes:** exact wording, speaker/author, role, source date and page/paragraph. Log these in quote-ledger.csv. Keep the surrounding context and a source snapshot/hash. A search snippet, paraphrase or model-generated sentence is not a verified quote. A worker's or customer's account remains attributed testimony, not proof of a population-wide effect.
5. **Status and response:** label allegations, settlements, admitted facts, court findings and research results accurately. Identify the source's date and whether the latest legal status was checked. Include material responses and alternative explanations that change the interpretation.
6. **Final comparison:** check the exact on-screen text, caption and spoken script against the same claim/source list. A careful caption does not correct a misleading headline or voiceover. Put key qualifiers on screen and in the narration.

If those checks cannot be completed, the case remains a research target. Do not pad a weekly quota with invented claims, unverified quotations or unsupported opinions. The automatic generator still creates unapproved drafts and does not independently establish that a source supports a claim; human source review remains necessary.

## Suggested short-video structure

- **Opening:** the strongest verified, concrete outcome, with a date. Use a number or quotation only after verification. No “most evil,” “destroyed,” “monopoly” or causal headline unless the exact proposition is established and properly attributed.
- **Ownership:** who acquired what, and when.
- **Record:** one clear mechanism or documented event, with a visible source/date label.
- **Human consequence:** a verified measure or an exact attributed quote. Do not invent a victim, document, eyewitness or archival image.
- **Context:** material qualification, procedural status and response. Keep it readable rather than hiding it in tiny print.
- **Ending:** the documented outcome and where to find the sources. The caption contains full source URLs; Instagram caption URLs are plain text.

For community/cultural loss, name the institution and document closures or service changes. A statement that a community “lost its soul” is someone's attributed opinion, not an objective fact. Report who said it and why, rather than turning it into the account's conclusion.

## First research queue

See case-queue.json: Toys R Us (jobs and community retail), U.S. Anesthesia Partners / Welsh Carson (competition), and a hospital-safety study (quality). The USAP case now has a primary-source-checked **review draft** in `pilot/cases/usap/`, with an exact quote matched to the complaint. The underlying communication was not independently authenticated, so it is explicitly reported as a quote reproduced in the filing. The other cases remain unverified targets. No case post is approved or published.

On October 25, 2026, subsequent requests successfully retrieved FTC records, the GAO report page and SEC search. The initial FTC release URL was wrong; it was corrected using the agency's September 2023 index. Some medical-publisher/abstract requests still return access challenges. Do not assume all research access is blocked or that a CAPTCHA page is the requested article. Preserve source dates, source snapshots and their hashes. Supplied original PDFs can also be reviewed; do not include private or confidential records.

## Audio

Use clear documentary narration, with music below speech. Quotes are read as attributed quotations, never presented as a real recording of the quoted person. No voice cloning or simulated company/witness audio. A modest bed can support pacing without manufacturing evidence. The selected narrator is local Kokoro **Heart**. Videos use fixed frames and clean cuts. No paid voice service is connected here.

## Readability and spoken wording (user feedback)

Build each short reel around one outcome or allegation, using three or four cards with one main idea each. Keep card bodies to one short sentence where possible. Retain attribution, material denials and necessary qualifications in the reel; put the detailed procedural chronology in the caption and source notes. Never simplify a claim into a stronger assertion than the evidence supports.

Write narration to be spoken naturally: spell out unfamiliar acronyms, avoid sound-effect words such as “cha-ching,” and do not force a quotation into the voiceover. An exact quote can stay in the source record without appearing in the reel. Preview the actual speech before approving a post. The simplified USAP revision is `pilot/cases/usap-simple/`; the original dense cut remains archived in `pilot/cases/usap/`.

## Consumer relevance and quiet sourcing (user feedback)

Lead with a specific consumer consequence supported by the complaint, investigation summary or other primary record. Explain the mechanism in familiar terms (for example, limited provider choice and how coverage is funded), without turning an alleged total cost into a verified bill or premium increase. FTC allegations can establish what the plaintiff alleged, not that the alleged harm was adjudicated true.

Do not narrate source dates, document numbers, source-checking process or instructions to read the sources. Keep brief on-screen attribution and necessary allegation labels; put full URLs, dates, historical coverage and legal chronology in the caption and review notes. A historical story must not imply current breaking news. Include the material company response in the reel. The current consumer-focused USAP review is `pilot/cases/usap-consumer/`.
