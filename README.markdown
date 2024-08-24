---
title: "Predicting functional cell type-specific enhancers from cross-species multi-omics"
#header:
#  image: /assets/images/biccn-logo-3.png
layout: single
classes: wide
author_profile: true
author: BICCN
---

<br>
![WashU](/assets/images/BICCN_challenge_schematic.png)

## Summary

Single-cell sequencing technologies enable molecular profiling of millions of cells to define atlases, or catalogs, of cell types across tissues and species. Recent advancements enable measurement of multiple genomic features (e.g. RNA and open chromatin) from the same cell. Multi-omic profiling of the brain across species enables high-resolution alignment of ‘homologous’ cell types that have conserved and specialized molecular features (Hodge et al. 2019, Jorstad et al. 2022, Zemke et al. 2023). 

In this competition, teams will predict cell type-specific enhancers using new multi-omics and multi-species atlases of cell types in the primary motor cortex. Teams will be evaluated against the on-target and off-target in vivo activity in mouse brain of a collection of several hundred enhancers that were experimentally screened. Progress will serve as a foundation for targeted exploration of cell types in brain circuitry across species.

## Timeline

* **September 19, 2023** - Start date.

* **October 19, 2023** - First submission by teams.

* **December 15, 2023** - Final submission by teams.

* **January 21, 2024** - Leaderboard finalized! Challenge closed, congrats Aerts lab for finishing 1st!

All deadlines are at 11:59 PM UTC on the corresponding day unless otherwise noted. The competiton organizers reserve the right to update the contest timeline if they deem it necessary.

## Submission File

For each `peak` called and reported in `Mouse_atac.h5ad`, you should report the **rank** of top 10,000 peaks for each unique annotation in `subclass_Bakken_2022`. Thus, each element of the submission will correspond to a `peak` / `subclass_Bakken_2022` pair and contain the corresponding rank as determined by your method.

Your submission should contain a header and have the following format:

```
chr,start,end,subclass_Bakken_2022,rank
chr1,1,500,"Pvalb",1
chr1,501,1000,"Pvalb",2
...
chr1,1,500,"Astro",1000
chr1,501,1000,"Astro",10000
```

Each team should create a Team directory at [Dropbox](https://www.dropbox.com/scl/fo/64k04s0nd07rk4lwya6ax/h?rlkey=dqt10h8t3l5u1v93adwiof18i&dl=0) and place their submission file within.

## Ask a question

We will be using the Github issues page for this website, [found here](https://github.com/UCDNJJ/ucdnjj.github.io/issues), as a means for discussion and questions regarding the challenge. 

## Join the challenge!
Now that the challenge has started, any additional teams wishing to join should reach out to nelson.johansen@alleninstitute.org. 

## Organizing committee

--- | --- | --- | ---
| <img width="75" alt="" src="/assets/people/nelson.jpg">  **Nelson Johansen** | <img width="75" alt="" src="/assets/people/bosiljka.jpeg"> **Bosiljka Tasic** | <img width="75" alt="" src="/assets/people/trygve.jpeg"> **Trygve Bakken** | <img width="75" alt="" src="/assets/people/ed.jpg"> **Ed Lein** | 

--- | --- | ---
|<img width="75" alt="" src="/assets/people/bing.jpg"> **Bing Ren** | | |

--- | --- | ---
|<img width="75" alt="" src="/assets/people/joe.jpg"> **Joe Ecker** | | |

## Funding support

* Allen Institute for Brain Science
* U19MH11483 to J.R.E and E.M.C
* U19MH114831-04s1 to J.R.E. and B.R.
* 5U01MH121282 to J.R.E and M.M.B
* UM1HG011585 to B.R.
