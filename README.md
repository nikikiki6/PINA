# PINA: Prompt Injection Attack against Navigation Agents

Jiani Liu, Yixin He, Lanlan Fan, Qidi Zhong, Yushi Cheng, Meng Zhang,
Yanjiao Chen, and Wenyuan Xu.

[![arXiv](https://img.shields.io/badge/arXiv-2601.13612-b31b1b)](https://arxiv.org/abs/2601.13612)
[![ICASSP 2026](https://img.shields.io/badge/IEEE-ICASSP%202026-00629B)](https://doi.org/10.1109/ICASSP55912.2026.11462407)
[Poster](poster_PINA.pdf)

PINA studies prompt injection against LLM navigation agents. It combines navigation
metric evaluation, surrogate-model distribution analysis, and iterative feedback
to refine injection prompts.

## Quick Start


### 1. Set Up the Victim

Clone [NavGPT](https://github.com/GengzeZhou/NavGPT).


Follow the [NavGPT installation and data preparation instructions](https://github.com/GengzeZhou/NavGPT/blob/b3fc8a21b8a1f66b09dde833bcfc25767ef1962d/README.md)
to install its dependencies in a separate environment and obtain the R2R resources.
Set `victim.python` below to that environment's Python executable. Victim data and
model weights are obtained separately.

### 3. Configure the Experiment

```bash
cp configs/navgpt.example.json configs/local.json
```

Edit `configs/local.json`:

The example uses [Mistral-7B-Instruct-v0.2](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2)
as the surrogate model.

Export credentials and the feedback model identifier in the shell used to run PINA:

```bash
export PINA_API_KEY=OPENAI_API_KEY or "your-own-model"
export PINA_OPTIMIZER_MODEL= OPENAI_API_KEY or "your-optimizer-model"
```

### 4. Run Attack Optimization

```bash
python -m scripts.run_attack --config configs/local.json
```

The optimizer evaluates prompts on NavGPT and refines them over the configured rounds.

### 5. Evaluate a Fixed Prompt

Set `initial_prompt` to the prompt to evaluate and choose a fresh `output_dir`:

```bash
python -m scripts.run_attack --config configs/local.json --evaluate-only
```

For a no-attack baseline, set `victim.mode` to `none` and run the same command with
another fresh `output_dir`.

### 6. View Results

Results are saved under `output_dir`


## Repository

```text
PINA/
├── adapters/
├── configs/
├── patches/
├── pina/
├── scripts/
├── tests/
├── .env.example
├── .gitignore
├── poster_PINA.pdf
├── requirements.txt
└── README.md
```

## Citation

```bibtex
@inproceedings{liu2026pina,
  title = {PINA: Prompt Injection Attack against Navigation Agents},
  author = {Liu, Jiani and He, Yixin and Fan, Lanlan and Zhong, Qidi and Cheng, Yushi and Zhang, Meng and Chen, Yanjiao and Xu, Wenyuan},
  booktitle = {2026 IEEE International Conference on Acoustics, Speech, and Signal Processing (ICASSP)},
  year = {2026},
  doi = {10.1109/ICASSP55912.2026.11462407}
}
```
