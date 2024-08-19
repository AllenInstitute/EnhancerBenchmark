---
layout: single
classes: wide
title: Challenge phases
permalink: /tasks/
author_profile: true
author: BICCN
---

This challenge is comprised of a single phase:

### Identifying functional enhancers for each annotated cell type

Here the goal is to define novel machine learning algorithms to predict functional enhancers specific to individual cell types, using multi-modal genomic and cross-species profiling of the motor cortex. The data sets provided for this task are a diverse collection of multi-omics profiles from four species (human, macaque, marmoset and mouse) that can be integrated as well as incorporated with biological priors.

Teams will optimize models that provide a ranked list of genomic regions (enhancers) for each cell annotation. The predictions will be evaluated against several hundred experimentally validated enhancers.

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