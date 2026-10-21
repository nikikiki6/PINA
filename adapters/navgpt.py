import math
import os
from pathlib import Path
import subprocess

def parse_metrics(text):
    records = []
    for line in text.splitlines():
        if 'Env name:' not in line:
            continue
        metrics = {}
        for field in line.split(',')[1:]:
            key, separator, value = field.strip().partition(':')
            if separator:
                try:
                    metrics[key] = float(value)
                except ValueError:
                    pass
        if {'sr', 'spl', 'nav_error'}.issubset(metrics):
            if not all((math.isfinite(value) for value in metrics.values())):
                raise ValueError('Non-finite navigation metrics')
            records.append(metrics)
    if not records:
        raise ValueError('No complete navigation metrics found')
    return records[-1]

class NavGPTAdapter:

    def __init__(self, nav_src, data_root, python, model, mode='observation', split='R2R_val_unseen_instr', iters=10, seed=0, timeout=3600):
        self.nav_src = Path(nav_src).expanduser().resolve()
        self.data_root = Path(data_root).expanduser().resolve()
        if not (self.nav_src / 'NavGPT.py').is_file():
            raise FileNotFoundError(self.nav_src / 'NavGPT.py')
        if not self.data_root.is_dir():
            raise FileNotFoundError(self.data_root)
        if mode not in ('none', 'instruction', 'observation'):
            raise ValueError(mode)
        if iters < 1:
            raise ValueError('iters must be positive')
        self.python, self.model, self.mode = (python, model, mode)
        self.split, self.iters, self.seed, self.timeout = (split, iters, seed, timeout)

    def evaluate(self, prompt, output_dir):
        output = Path(output_dir).resolve()
        if output.exists() and any(output.iterdir()):
            raise FileExistsError(f'Use a fresh output directory: {output}')
        output.mkdir(parents=True, exist_ok=True)
        command = [self.python, 'NavGPT.py', '--root_dir', str(self.data_root), '--output_dir', str(output), '--llm_model_name', self.model, '--val_env_name', self.split, '--iters', str(self.iters), '--batch_size', '1', '--seed', str(self.seed), '--injection_mode', self.mode, '--injection_prompt', prompt if self.mode == 'instruction' else '']
        env = os.environ.copy()
        env['PINA_OBSERVATION_PAYLOAD'] = prompt if self.mode == 'observation' else ''
        with (output / 'process.log').open('w') as log:
            subprocess.run(command, cwd=self.nav_src, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=self.timeout, check=True)
        return parse_metrics((output / 'logs' / 'valid.txt').read_text())
