

![WashU](/assets/images/BICCN_challenge_schematic.png)

## Summary

Single-cell sequencing technologies enable molecular profiling of millions of cells to define atlases, or catalogs, of cell types across tissues and species. Recent advancements enable measurement of multiple genomic features (e.g. RNA and open chromatin) from the same cell. Multi-omic profiling of the brain across species enables high-resolution alignment of ‘homologous’ cell types that have conserved and specialized molecular features (Hodge et al. 2019, Jorstad et al. 2022, Zemke et al. 2023). 

In the BICCN competition, teams predicted cell type-specific enhancers using new multi-omics and multi-species atlases of cell types in the primary motor cortex. Teams were evaluated against in vivo activity of enhancers in the mouse brain from a collection of several hundred enhancers that were experimentally screened [Ben-Simon et al. 2024](https://www.biorxiv.org/content/10.1101/2024.06.10.597244v2]](https://doi.org/10.1101/2024.06.10.597244)); [addgene](https://www.addgene.org/collections/brain-armamentarium). Progress will serve as a foundation for targeted exploration of cell types in brain circuitry across species.

## Evaluate your method

We designed the benchmark metric for the challenge to be used to evaluate new approaches in the context of the current state-of-the-art enhancer prioritization methods. Following the guidelines in our submissions and data pages please self-evaluate using the [benchmark metric](https://github.com/AllenInstitute/EnhancerBenchmark/blob/main/code/BenchmarkMetric.R), **enhancer validation tables will be provided once published**. We encourage method developers to then create a pull request to our leaderboard page with your results and submission files.

## Pages

-  [About](https://github.com/AllenInstitute/EnhancerBenchmark/blob/main/_pages/about.markdown) : General information about the BICCN Challenge and benchmark metric.
-  [Data](https://github.com/AllenInstitute/EnhancerBenchmark/blob/main/_pages/data.markdown) : Data overview and summary of files.
-  [Submissions](https://github.com/AllenInstitute/EnhancerBenchmark/blob/main/_pages/submissions.markdown) : Detaials for the expected submission format.
-  [Evaluation](https://github.com/AllenInstitute/EnhancerBenchmark/blob/main/_pages/evaluation.markdown) : Benchmark metric summary.

## Leaderboard

-  [Leaderboard](https://github.com/AllenInstitute/EnhancerBenchmark/blob/main/_pages/leaderboard.markdown) : Challenge and running leaderboard for new method submissions.

## Ask a question

We will be using the Github issues page for this website, [found here](https://github.com/AllenInstitute/EnhancerBenchmark/issues), as a means for discussion and questions regarding the challenge. 

## Organizing committee

| | | | |
--- | --- | --- | ---
| <img width="75" alt="" src="/assets/people/nelson.jpg">  **Nelson Johansen** | <img width="75" alt="" src="/assets/people/bosiljka.jpeg"> **Bosiljka Tasic** | <img width="75" alt="" src="/assets/people/trygve.jpeg"> **Trygve Bakken** | <img width="75" alt="" src="/assets/people/ed.jpg"> **Ed Lein** | 
|<img width="75" alt="" src="/assets/people/bing.jpg"> **Bing Ren** | | |
|<img width="75" alt="" src="/assets/people/joe.jpg"> **Joe Ecker** | | |

## Funding support

* Allen Institute for Brain Science
* U19MH11483 to J.R.E and E.M.C
* U19MH114831-04s1 to J.R.E. and B.R.
* 5U01MH121282 to J.R.E and M.M.B
* UM1HG011585 to B.R.

## Links to methods

https://github.com/AllenInstitute/PeakRankR

https://github.com/ytanaka-bio/cisMultiDeep

https://labshare.cshl.edu/shares/gillislab/resource/HiC

[CREsted: Cis Regulatory Element Sequence Training, Explanation, and Design.](https://crested.readthedocs.io/en/latest/)

## Citation

`Johansen, N. J., Kempynck, N., (2024). Evaluating Methods for the Prediction of Cell Type-Specific Enhancers in the Mammalian Cortex. bioRxiv, 2024-08. https://doi.org/10.1101/2024.08.21.609075`
