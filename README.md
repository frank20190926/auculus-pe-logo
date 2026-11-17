# Auculus Capital identity suite

Local design delivery for contest #2800950. No submission or publication performed.

Open `index.html` directly, or serve this folder with `python3 -m http.server 8048` and visit http://localhost:8048.

## Collection

- Marque I: Oculus Vault, architectural A/C monogram.
- Marque II: Sovereign Seal, shield, negative-space counter and gold meridian.
- Marque III: typographic signature with champagne A/U and diagonal cuts.
- All SVG letters are original outlined vector paths. No font installation is required for the vectors.
- Google Fonts supplies Cormorant Garamond, Cinzel and Plus Jakarta Sans for the presentation UI; internet is required to load these fonts.
- The three required canonical SVG filenames use Marque I. The selector updates all contextual previews and downloads to the active direction.
- Each direction includes dark, reversed, square and optically simplified micro SVG variants. Use the micro asset for favicons, not the detailed square master.

## Print and application

Screen colour values are authoritative. CMYK values are simple unprofiled conversions and need printer-specific proofing. Pantone 871 C is a proposed metallic production reference, not an exact match to the screen gradient. Financial figures in the deck are illustrative, not claims about the company.

The construction overlay specifies 29-unit clear space around a 94-unit reference box; the 94/58 ratio approximates the golden ratio. It is a layout guide, not a claim that every curved outline derives from phi.

## Verification, 2026-11-07

- 1440 x 920 viewport: document 1440 x 920, no overflow.
- 390 px mobile: no horizontal overflow; all images loaded.
- Three selectors, nine download URLs, grid toggle and deck toggle checked in Chromium.
- 15 SVGs parsed as XML; all letterforms are paths, no text nodes.
- Screenshot review completed for all three directions and mobile.
- Evidence: `evidence/board-desktop.png`, `evidence/board-mobile.png`, `evidence/sovereign-seal.png`, `evidence/ligature-metrics.png`.

Source: `build_vectors.py` regenerates the nine main direction SVGs, three canonical aliases and `vector-manifest.js`. Micro SVGs are independently drawn optical adaptations and retained separately.
