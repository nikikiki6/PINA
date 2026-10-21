import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from adapters.navgpt import NavGPTAdapter, parse_metrics

class AdapterTests(unittest.TestCase):

    def test_parse(self):
        self.assertEqual(parse_metrics('Env name: x, sr: 10, spl: 2, nav_error: 8')['spl'], 2)
        with self.assertRaises(ValueError):
            parse_metrics('incomplete')

    def test_modes_and_stale_results(self):
        for mode in ('none', 'instruction', 'observation'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                (root / 'NavGPT.py').touch()
                adapter = NavGPTAdapter(root, root, 'python', 'test-model', mode)

                def run(command, **kwargs):
                    expected = 'payload' if mode == 'observation' else ''
                    self.assertEqual(kwargs['env']['PINA_OBSERVATION_PAYLOAD'], expected)
                    self.assertEqual(command[command.index('--injection_prompt') + 1], 'payload' if mode == 'instruction' else '')
                    logs = root / 'run' / 'logs'
                    logs.mkdir()
                    (logs / 'valid.txt').write_text('Env name: x, sr: 10, spl: 2, nav_error: 8')
                with patch('adapters.navgpt.subprocess.run', side_effect=run):
                    self.assertEqual(adapter.evaluate('payload', root / 'run')['nav_error'], 8)
                with self.assertRaises(FileExistsError):
                    adapter.evaluate('payload', root / 'run')
if __name__ == '__main__':
    unittest.main()
