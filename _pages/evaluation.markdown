---
layout: single
classes: wide
title: Evaluation
permalink: /evaluation/
author_profile: true
author: BICCN
---

### Overview

Teams will be evaluated based on the ranked ordering of enhancers that have been screened in enhancer AVVs in-vivo at the Allen Institute for Brain Science. 

## Validation data

<p align="center">
  <img src="/assets/images/enhancer_screening_pipeline.png" />
</p>

Each enhancer AAV in our collection has been scored to determine specificity of the enhancer element with respect to a target cell type as well as density and intensity of cell labeling.

Briefly, each enhancer is screened as follows:

* Enhancer elements were cloned upstream of a minimal beta-globin promoter driving fluorescent protein SYFP2 and packaged in PHP.eB-serotype viruses that enable crossing of the blood brain barrier.
* Mice were injected retroorbitally (RO) with the enhancer AAV, sliced sagittally, and imaged confocally.
* Enhancer specificity was scored by manually evaluating SYFP2 fluorescence in serial brain slices. We defined enhancer specificity based on the density (relative to the expected distribution; from 0 to 2) and fluorescence intensity (from 0 to 2) of labeling. We also provide a combined score (0 - 3) of these values. 

In total, the Allen Institue has experimentally validated **hundreds** of enhancer elements selected to be specific for a given cortical cell population. For further details of the Allen Institues enhancer screening efforts please refer to [Graybuck and Daigle et al. 2021](https://www.cell.com/neuron/fulltext/S0896-6273(21)00159-8?_returnURL=https%3A%2F%2Flinkinghub.elsevier.com%2Fretrieve%2Fpii%2FS0896627321001598%3Fshowall%3Dtrue) or [Mich et al. 2021](https://www.cell.com/cell-reports/fulltext/S2211-1247(21)00067-X?_returnURL=https%3A%2F%2Flinkinghub.elsevier.com%2Fretrieve%2Fpii%2FS221112472100067X%3Fshowall%3Dtrue).

## Evaluation metrics

<p align="center">
  <img src="/assets/images/evalutaion_schematic.png" />
</p>

Metrics for evaluating cell type-specific functional enhancer prediction aim to characterize how well the ranked list of enhancers correspond to experimentally validated enhancer collections.

<p align="center">
  <img src="/assets/images/evaluation_layout.png" />
</p>
