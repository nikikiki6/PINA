# PINA: Prompt Injection Attack against Navigation Agents


<p align="center">
  <a href="https://arxiv.org/abs/2601.13612">arXiv</a> ·
  <a href="https://doi.org/10.1109/ICASSP55912.2026.11462407">IEEE Xplore</a> ·
  <a href="./poster_PINA.pdf">Poster</a> ·
  <a href="#citation">BibTeX</a>
</p>

<p align="center">
  <a href="https://arxiv.org/abs/2601.13612">
    <img src="https://img.shields.io/badge/arXiv-2601.13612-b31b1b.svg" alt="arXiv">
  </a>
  <a href="https://doi.org/10.1109/ICASSP55912.2026.11462407">
    <img src="https://img.shields.io/badge/IEEE-ICASSP%202026-00629B.svg" alt="IEEE ICASSP 2026">
  </a>
  <a href="./poster_icassp_jiani_2.pdf">
    <img src="https://img.shields.io/badge/Poster-PDF-D32F2F.svg" alt="Poster PDF">
  </a>
</p>

<p align="center">
  <a href="#abstract">Abstract</a> ·
  <a href="#method">Method</a> ·
  <a href="#poster">Poster</a> ·
  <a href="#repository-structure">Repository Structure</a> ·
  <a href="#code-and-reproducibility">Code</a> ·
  <a href="#citation">Citation</a>
</p>

> **Publication:** IEEE International Conference on Acoustics, Speech, and Signal Processing (**ICASSP**), 2026.  
> **Code:** The implementation is being prepared and will be released in the `code/` directory.

## Abstract

Navigation agents powered by large language models (LLMs) convert natural-language instructions into executable plans and actions. Compared with text-based applications, the security stakes are substantially higher: a successful prompt injection attack can misguide physical navigation, leading to unsafe routes, mission failure, or real-world harm.

Despite this setting, the vulnerability of navigation agents to prompt injection remains largely unexplored. In this paper, we propose **PINA**, an adaptive prompt optimization framework designed for navigation agents under black-box, long-context, and action-executable constraints. Experiments on indoor and outdoor navigation agents show that PINA achieves a high attack success rate (ASR), with an average ASR of **87.5%**, surpassing all baselines and remaining robust under ablation and adaptive-attack conditions.

This work presents a systematic investigation of prompt injection attacks in navigation and highlights their security implications for embodied LLM agents.

## Method

<p align="center">
  <img width="747" alt="Overview of the PINA framework" src="https://github.com/user-attachments/assets/cb2764b3-7951-433d-bfc4-50c9d7601d65" />
</p>

PINA combines three components in an adaptive optimization loop:

1. **Attack Evaluator** — quantifies attack impact using navigation metrics.
2. **Distribution Analyzer** — captures global KL divergence and local key tokens.
3. **Adaptive Refinement** — iteratively updates injection prompts according to the analysis results.

Together, these components enable effective black-box prompt injection attacks against navigation agents.

## Poster

The ICASSP 2026 presentation poster is available here:

<p align="center">
  <a href="./poster_icassp_jiani_2.pdf"><strong>View or download the PINA poster (PDF)</strong></a>
</p>

## Repository Structure

```text
PINA/
├── code/                 # Implementation, to be released
├── poster_icassp_jiani_2.pdf  # ICASSP 2026 presentation poster
├── README.md             # Project overview and usage guide
└── LICENSE               # License file (to be added)
```

The `code/` directory is intentionally left empty for now. Implementation files, environment requirements, and reproduction commands will be added there when the code is released.

## Code and Reproducibility

The implementation is under preparation. Its release will include:

- the PINA implementation;
- evaluation pipelines for supported navigation agents;
- configuration files and dependency instructions;
- commands for reproducing the reported experiments.

## Citation

If you find this work useful, please cite it as follows:

```bibtex
@inproceedings{liu2026pina,
  title     = {PINA: Prompt Injection Attack against Navigation Agents},
  author    = {Liu, Jiani and He, Yixin and Fan, Lanlan and Zhong, Qidi and
               Cheng, Yushi and Zhang, Meng and Chen, Yanjiao and Xu, Wenyuan},
  booktitle = {2026 IEEE International Conference on Acoustics, Speech, and Signal Processing (ICASSP)},
  year      = {2026},
  doi       = {10.1109/ICASSP55912.2026.11462407}
}
```

## Contact

For questions, feedback, or collaboration inquiries, please open an [issue](../../issues) in this repository.
