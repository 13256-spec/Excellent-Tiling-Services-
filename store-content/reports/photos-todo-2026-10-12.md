# Photos still to source (saved 12 Oct 2026, for a Claude in Chrome session)

20 products carry the `photo-needed` tag and have no usable photo online that this cloud session could reach.
BAT Trims' website (battrims.com) returns "403 Forbidden" to the cloud session's addresses, and no stockist
lists these items. **Claude in Chrome runs in the owner's own browser, so it can open battrims.com and the
Raimondi dealer pages that block us.** When the owner is at his computer with the Claude Chrome extension
and this session connected, run the plan below.

## Plan for the Chrome session

1. Open https://battrims.com/catalogues/ and download the Tools catalogue and the BATSEAL catalogue PDFs
   (if they exist); product photos can be cut from the PDFs with `pdfimages`.
2. Search battrims.com (search box, or `https://battrims.com/?s=<term>&post_type=product`) for each item
   below; open the product page, copy the largest image URL (right-click → copy image address, or the
   `og:image`), note the SKU on the page.
3. Load each photo with `productCreateMedia` (originalSource = the image URL, alt = our product title),
   link variant images where the product has colour/size variants, then `tagsRemove` `photo-needed`.
   Record source, size and confidence in `photos-sourced-2026-10-11.csv`.

Rules: manufacturer or official-distributor photos only; the photo must show the exact item (check the
code on the label); never a watermarked retailer photo; never show the tile supplier's name.

## The 20 products

| Product (handle) | Our SKUs | Where to look |
|---|---|---|
| BAT 20 Ltr Bucket (`bat-20-ltr-promotional-bucket`) | BAT-20LPB | battrims.com search "bucket"; Tools catalogue |
| BAT 20 Ltr Bucket Lid (`bat-20-ltr-promotional-bucket-lid`) | BAT-20LPBLID | same |
| Panther 20 Ltr Bucket (`panther-20-ltr-promotional-bucket`) | PAN-20LPB | battrims.com search "panther bucket"; Panther catalogue |
| Panther 20 Ltr Bucket Lid - Orange (`panther-20-ltr-promotional-bucket-lid-orange`) | PAN-20LPBLID | same |
| BAT Luxe Square Inspection Drain - 100mm Outlet (`bat-luxe-square-inspection-drain-100mm-outlet`) | BL-SID100, BL-SID100MB | battrims.com BAT Luxe range (product tag `batluxe`); may be listed as a square floor waste/inspection drain |
| BAT Utility Knife (`bat-utility-knife`) | UK-1 | battrims.com search "utility knife" (not the folding BP-FKS) |
| BAT Pro Folding Utility Knife Spare Blade Set 10 pce (`bat-pro-folding-utility-knife-spare-blade-set-10-pce`) | BP-FKSB10 | battrims.com folding knife page / "blade" |
| BAT Floor Scraper 300mm Replacement Blade (`bat-floor-scraper-300mm-replacement-blade`) | FS-300-SB | battrims.com floor scraper page (a 160 px thumbnail exists at wp-content/uploads/F...; look for the full size) |
| BATSEAL De-Scale Phosphoric Acid Cleaner (`batseal-de-scale-phosphoric-acid-cleaner`) | BC-DSC1, BC-DSC4 | battrims.com BATSEAL range / BATSEAL catalogue |
| BATSEAL Matt Look Solvent Based Sealer (`batseal-matt-look-solvent-based-sealer`) | BC-SML1, BC-SML4, BC-SML20 | same |
| BATSEAL Silcopel Solvent Based Sealer (`batseal-silcopel-solvent-based-sealer`) | BC-SPELSB1, BC-SPELSB4 | same |
| BATSEAL Wet Look Solvent Based Sealer (`batseal-wet-look-solvent-based-sealer`) | BC-SWL1, BC-SWL4, BC-SWL20 | same |
| BATSEAL Pristine Water Based Sealer 1 Ltr (`batseal-pristine-water-based-sealer-1-ltr`) | BC-PRISWB1 | same |
| BATSEAL Eversol Solvent (`batseal-eversol-solvent`) | BC-EVSOL1, BC-EVSOL4 | same |
| Raimondi Easymove LFT Carrying Bar Set with 4 RV175 Suction Cups (`raimondi-easymove-lft-carrying-bar-set-with-4-rv175-suction-cups`) | RAI-EASYMOVE3-4RV | raimondispa.com Easy-Move page (only a 6-cup photo online; ask BAT Trims for the 4-cup kit photo) |
| Raimondi Rai-Cut Grooving Tool Spare Blade (`raimondi-rai-cut-grooving-tool-spare-blade`) | RAI-RAICUT-SB | raimondispa.com RAI-CUT accessories; thefloorbox.ca (Raimondi dealer) |
| Raimondi Lupetto 11 Row Roller Plate Assembly (`raimondi-lupetto-11-row-roller-plate-assembly`) | RAI-LUPETTO-RA | tsptrims.com.au (listed it before, page now 404); Raimondi Lupetto catalogue PDF |
| Raimondi Lupetto Flat Vibrating Plate (`raimondi-lupetto-flat-vibrating-plate`) | RAI-LUPETTO-VP | Raimondi Lupetto catalogue PDF |
| Raimondi 300W / 42V Transformer for Terranova (`raimondi-300w-42v-transformer-suit-terranova`) | RAI-TERRATF | raimondispa.com Terranova page; dealers |
| Raimondi Ipertitina Splash Guard Skirt (`raimondi-ipertitina-splash-guard-skirt`) | RAI-IPERSGSK | raimondispa.com Ipertitina accessories (art. 121IP03A splash guard ring); thefloorbox.ca |

Fallback if the web has nothing: a phone photo of each item in the showroom, or ask BAT Trims
(info@battrims.com) for the Tools, BATSEAL and Panther catalogue PDFs.
