import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('router', Path(__file__).with_name('route_codex.py'))
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)

class RouterTests(unittest.TestCase):
    def decision(self):
        return dict(model=r.MODELS['sol'], rework_risk='low', reason='Local and verifiable', luna_batch=False)

    def test_validation(self):
        self.assertEqual(r.validate_decision(self.decision())['model'], r.MODELS['sol'])
        for changes in [dict(model='untrusted'), dict(reason=''), dict(luna_batch='false'), dict(rework_risk='high')]:
            with self.assertRaises(ValueError):
                r.validate_decision(self.decision() | changes)

    def test_no_execution_on_classifier_error(self):
        with patch.object(r, 'classify', side_effect=RuntimeError('test failure')), patch.object(r.subprocess, 'run') as run:
            self.assertEqual(r.main(['--prompt', 'task']), 2)
            run.assert_not_called()

    def test_route_only(self):
        with patch.object(r, 'classify', return_value=self.decision()), patch.object(r.subprocess, 'run') as run:
            self.assertEqual(r.main(['--prompt', 'task', '--route-only']), 0)
            run.assert_not_called()

    def test_override_and_exit_code(self):
        with patch.object(r, 'classify') as classify, patch.object(r, 'codex_command', return_value=['codex.exe']), patch.object(r.subprocess, 'run', return_value=subprocess.CompletedProcess([], 7)) as run:
            self.assertEqual(r.main(['--prompt', 'task', '--model', 'astra']), 7)
            classify.assert_not_called()
            self.assertIn('gpt-6-astra', run.call_args.args[0])

    def test_shell_text_stays_stdin(self):
        text = '中文 "quoted"\n$(Get-Content secret) `whoami` & echo NO; --model bad'
        with patch.object(r, 'classify', return_value=self.decision()), patch.object(r, 'codex_command', return_value=['codex.exe']), patch.object(r.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0)) as run:
            self.assertEqual(r.main(['--prompt', text]), 0)
            self.assertNotIn(text, run.call_args.args[0])
            self.assertIn(text, run.call_args.kwargs['input'])
            self.assertFalse(run.call_args.kwargs['shell'])
            self.assertIn('read-only', run.call_args.args[0])

    def test_files_and_context(self):
        with tempfile.TemporaryDirectory() as temp:
            task, context = Path(temp)/'task.txt', Path(temp)/'plan.txt'
            task.write_text('转换一批文件', encoding='utf-8-sig')
            context.write_text('完整计划', encoding='utf-8')
            with patch.object(r, 'classify', return_value=self.decision()) as classify:
                self.assertEqual(r.main(['--prompt-file', str(task), '--context-file', str(context), '--route-only']), 0)
                self.assertEqual(classify.call_args.args[:2], ('转换一批文件','完整计划'))

    def test_empty_input(self):
        with patch.object(r, 'classify') as classify:
            self.assertEqual(r.main(['--prompt','  ']), 2)
            classify.assert_not_called()

    def test_bulk_delegation_propagates(self):
        decision = self.decision() | {'luna_batch': True}
        prompt = r.execution_prompt('Read 100 logs', '', decision)
        self.assertIn('"luna_batch": true', prompt)
        self.assertIn('gpt-5.6-luna', prompt)

    def test_timeout(self):
        with patch.object(r, 'classify', side_effect=subprocess.TimeoutExpired('codex',1)):
            self.assertEqual(r.main(['--prompt','test']), 2)

    def test_real_subprocess_input(self):
        result=r.run_classifier([r.sys.executable, '-c', 'import sys; print(sys.stdin.read())'], 'abc', 5)
        self.assertEqual(result.stdout.strip(), 'abc')

    def test_real_subprocess_timeout(self):
        with self.assertRaises(subprocess.TimeoutExpired):
            r.run_classifier([r.sys.executable, '-c', 'import time; time.sleep(20)'], '', 0.1)

if __name__ == '__main__':
    unittest.main()
