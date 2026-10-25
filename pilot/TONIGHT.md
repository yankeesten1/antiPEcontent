# Tonight: prepare the launch while Instagram reviews the account

The existing Instagram account is under appeal. This kit prepares assets and workflow independently of that account. It does not resolve the appeal, connect accounts, send a scheduled ChatGPT message or publish anything. No purchase or paid API access is required for the selected manual pilot.

## Ready to do tonight

1. **Download and unzip `tonight-kit.zip`.** Extract it before opening `review.html`; images will not load reliably inside a ZIP preview. The review page opens directly in your browser, without hosting or installation. Edit the caption text and choose **Download edited caption** to keep each revision. Edits are not automatically saved to the original files or GitHub. No passwords or API keys belong in the review page.
2. **Confirm the working identity.** Display name: **PE Under Scrutiny**. You confirmed the handle **@PEUnderScrutiny**. The included PNG profile images and SVG design source use a typographic PE mark designed for circular cropping. These are draft brand assets, not a registered mark or a claim of affiliation.
3. **Save the profile copy** from `profile-copy.txt`. The 121-character bio is ready to paste once profile access returns. Review the correction policy and decide whether you want DMs as the correction channel; do not claim a monitored email address or website that does not exist.
4. **Review the introduction first.** See `FIRST-POST-REVIEW.md` and day 1 in `review.html`. It states an editorial position and makes no company-specific factual allegations. It is ready for wording review, not automatically approved. The graphic and caption are separate files; a caption edit does not redraw the graphic.
5. **Review days 2–7.** Posts 2, 3 and 4 need primary-source verification. Open the references yourself, confirm the supporting passages and keep the dated 2023 merger-guideline framing. If a source does not support the statement, revise the statement or replace the source. Leave the post unscheduled until verified. The editorial/question posts still need a final wording and image review.
6. **Prepare your tracking sheet.** Import `metrics.csv` and `weekly-review.csv` into a spreadsheet if you prefer. Leave unavailable measurements blank. Record actual revenue, cash costs and all research/editing/moderation time. Measure each post after roughly 48 hours. There are no actual performance results yet.
7. **Set a local reminder.** If useful, add a reminder in your own phone/calendar to review and schedule the batch. Use **9 p.m. America/New_York** as the posting target. No reminder or ChatGPT scheduled task has been created by this kit. Do not set launch dates that assume the appeal will be resolved tonight.
8. **Prepare GitHub's manual export workflow**, optionally. The branch includes `.github/workflows/build-launch-kit.yml`. Review and merge this branch into your repository's default branch to make its manual trigger available. Then go to **Actions → Build weekly launch kit → Run workflow**. Start with `pilot/week-01.json`. Download the `launch-kit` artifact once the workflow succeeds. This is an on-demand file build, not an Instagram automation or scheduled job. No API secrets are needed. It uses GitHub Actions compute/storage; check your account's included allowance and spending settings before running it, especially for a private repository. The workflow has not been run remotely from this chat because GitHub API access was denied.

## After account access is restored

1. Confirm the restored account's handle, enable two-factor authentication and choose Business or Creator in Instagram's account tools if not already set. Keep recovery codes private.
2. Upload `profile-avatar-1080.png`, set the display name and paste the final bio. Review how the avatar looks in Instagram's circular crop.
3. If needed for your Meta Business Suite configuration, connect the professional Instagram account to a Facebook Page you manage. You can draft the Page name, description and identity tonight using this kit, but account connection and verification require your own logged-in Meta interfaces. No separate Page or developer app has been created here.
4. Confirm the intended Instagram account is selected in Meta Business Suite. Upload one approved JPEG and its matching final caption, inspect the preview, and schedule it for an explicit date at 9 p.m. Eastern. If the interface does not support scheduling for the account, publish manually through Instagram. Do not assume linking succeeded from a Page name alone.
5. Only schedule the remainder after the first preview and account selection are confirmed. Double-check source support and approval for each post.
6. Verify the first live post yourself and record its URL. At 48 hours, record the available insights. Repeat weekly using the prompt in `START-HERE.md` and your measurements.

## What remains outside this kit

- Instagram appeal outcome and restored access to the user-confirmed @PEUnderScrutiny account.
- User approval of the final images/captions and the source checks for factual posts.
- Account changes, Facebook Page creation/linking and scheduling in your own Meta interfaces.
- GitHub default-branch merge and a first successful manual workflow run, if you choose that route.
- Any automatic daily notification inside ChatGPT. There is no supported connection for that here.

The paid daily-generation/publishing prototype remains optional. Do not buy hosting, API credits, ads, a domain or a scheduler for this pilot tonight. The local export and offline review page already work without those services.
