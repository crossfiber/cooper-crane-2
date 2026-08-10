# Cooper Crane LLC - Website v3 (USA rebrand)

**Business:** Cooper Crane LLC - Southeast Florida crane & boom truck service
**Old site:** https://www.coopercrane.com (Wix) · Previous build kept live as reference: https://crossfiber.github.io/cooper-crane/
**Build date:** 2026-08-10
**Repo:** crossfiber/cooper-crane-2
**Live URL:** https://crossfiber.github.io/cooper-crane-2/

## Scope changes vs v2
- Fort Myers / Southwest yard removed entirely per client: East coast only, West Palm Beach to South Miami (Palm Beach, Broward, Miami-Dade). The (239) number and Coopercranefm@gmail.com are retired sitewide, including schema.
- Single phone (954) 445-6186 everywhere; the yard-routing select is gone from the contact form (4 fields now).

## Fonts (confirmed on Google Fonts)
- Headlines: Big Shoulders 600-800 (variable, opsz 10-72) - American industrial display
- Body: Public Sans 400-700 - the U.S. government's own typeface
- URL: https://fonts.googleapis.com/css2?family=Big+Shoulders:opsz,wght@10..72,600..800&family=Public+Sans:wght@400;500;600;700&display=swap
- No Font Awesome: zero icon dependency. Stars are text glyphs, phone icons are two inline SVGs.

## Palette (flag-derived AND fleet-derived: the trucks are red and white)
- `--navy #16233B` deep flag navy (dark sections) · raised `#20304F` · footer `#0D1524`
- `--red #B22335` fleet/flag red, CTA and action ONLY · hover `#8F1727`
- `--porcelain #F6F5F1` light bg · alt `#EBEAE3` · ink `#17202F` · bone `#F4F3EE`

## Design direction
Confident American iron, not costume patriotism. Signature: the Fleet Board, four riveted navy steel plates whose widths scale with rated tonnage (2T to 40T full-width flagship with red star). Motif budget: ONE stripe seam (hero bottom), stars only as structural marks (nav, flagship, chip). Deliberately avoided: charcoal+orange AI-industrial default, icon-card grids, flag clip-art, Font Awesome comfort icons.

## Placeholders / client asks
- [LOGO ASSET NEEDED FROM CLIENT] - typographic star+wordmark lockup stands in; nav has a marked slot.
- West Park yard street address unverified; footer says "West Park, Broward County, FL" only.
- Form is a mailto: handoff with a visible call fallback. Upgrade to Formspree (free) when client confirms destination inbox.
- GA4 block is in the head, commented, with call_click + quote_form_submit events pre-wired; paste property ID and uncomment.

## SEO layer (structure ready, engagement not started)
LocalBusiness schema (single yard, matches existing GBP listing cid=972231914882425130, real 4.0/20 rating), FAQPage schema, robots.txt with AI crawlers, llms.txt, sitemap.xml. GBP claim/optimization + city pages are the paid-tier work; the old repo's /crane-rental-broward/ page is the architecture template.

## Assets
All photos are Cooper Crane's real photos carried from v2 (originally extracted from the old Wix site / client). og-card.png and favicon.png generated in-brand. cross-designs.png is the footer credit mark.
