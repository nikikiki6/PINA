import argparse
import json
import random
from pathlib import Path
from adapters.navgpt import NavGPTAdapter

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--evaluate-only', action='store_true')
    args = parser.parse_args()
    config = json.loads(Path(args.config).read_text())
    random.seed(config.get('seed', 0))
    adapter = NavGPTAdapter(**config['victim'], seed=config.get('seed', 0))
    output = Path(config['output_dir']).expanduser().resolve()
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f'Use a fresh output directory: {output}')
    output.mkdir(parents=True, exist_ok=True)
    (output / 'config.json').write_text(json.dumps(config, indent=2))
    if args.evaluate_only:
        result = adapter.evaluate(config['initial_prompt'], output / 'evaluation')
        (output / 'metrics.json').write_text(json.dumps(result, indent=2))
        return
    from pina.optimizer import SimplifiedLogitsAPOOptimizer
    records = json.loads(Path(config['annotations']).expanduser().read_text())
    instructions = []
    for record in records:
        if 'instructions' in record:
            instructions.extend(record['instructions'])
        elif 'instruction' in record:
            instructions.append(record['instruction'])
    optimizer = SimplifiedLogitsAPOOptimizer(adapter, instructions, output, config['surrogate_model'], config.get('scoring_config', 'default'))
    best_prompt, best_score, _ = optimizer.optimize(config['initial_prompt'], config.get('rounds', 5))
    optimizer.save_results(best_prompt, best_score)
if __name__ == '__main__':
    main()
