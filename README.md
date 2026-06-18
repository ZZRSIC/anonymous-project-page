# DriveStack-VLA Anonymous Project Page

Static GitHub Pages site for a strict double-blind review project page. It is designed for an anonymous GitHub account, then a second anonymous link generated through `anonymous.4open.science`.

## Page Content

The deployable page intentionally does not publish or embed PDF files. The appendix content has been extracted into
native webpage sections:

- `Overview`: abstract and headline metrics.
- `Supplementary RFT Details`: KL regularization, joint reward, and GRPO training loop.
- `Additional Experiments`: Navhard, implementation, latency, and ablation summaries.
- `Qualitative Trajectory Process`: extracted text summary of the appendix qualitative section.

Use `materials/` only for local intake from Overleaf exports. Do not commit raw source exports or PDFs unless explicitly
needed for the final release.

## Double-Blind Checklist

- Replace the title, abstract, captions, and section text in `index.html`.
- Keep authors as `Anonymous Authors`.
- Remove names, affiliations, funding, acknowledgments, email addresses, and personal URLs.
- Remove lab logos, terminal usernames, absolute paths, project IDs, and non-anonymous GitHub links from images and videos.
- Clear metadata from any images or videos before committing.
- Add sensitive terms to `tools/anonymity_terms.txt`.
- Run `tools/check-anonymity.sh`.

## Local Preview

Open `index.html` directly in a browser or serve the directory with any static file server.

## GitHub Pages Release

1. Push this repository to a new anonymous GitHub account.
2. Enable GitHub Pages for the repository.
3. Confirm the page and all local assets load without login.
4. Create an anonymous repository link at `https://anonymous.4open.science/`.
5. Put only the 4open anonymous link in the review manuscript and supplementary material.

## Attribution

This page structure is based on the Academic Project Page Template by eliahuhorwitz and adapted for double-blind review.
