"""Opt-in paid live classification checks; never execute the classified tasks."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import route_codex as r

CASES = [
    ('arithmetic', '只回答 2 加 3 的结果，不读取文件，不使用工具。', 'sol', False),
    ('bulk', '读取指定目录的 100 份 JSON 日志，按已给字段 timestamp、level、message 提取并归类。格式已知；各文件独立。由主智能体抽查并汇总。', 'sol', True),
    ('architecture', '为八个在线服务重新设计认证与数据迁移方案，调研选型、实现并验证兼容性；目前方案和依赖尚不明确。', 'astra', False),
    ('short_hard', '查明跨端偶发数据丢失的根因并修复；复现条件未知。', 'astra', False),
    ('local', 'Change the typo teh to the in the supplied sentence and return the sentence.', 'sol', False),
    ('negation', '只把这段话翻成英文：我们不做架构迁移，不部署，不重构八个服务。', 'sol', False),
]

def check(case):
    name, task, model, luna = case
    try:
        decision = r.classify(task, '', Path.cwd())
        return dict(name=name, expected_model=r.MODELS[model], expected_luna=luna,
            decision=decision, passed=decision['model']==r.MODELS[model] and decision['luna_batch']==luna)
    except Exception as error:
        return dict(name=name, passed=False, error=str(error))

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args=parser.parse_args()
    with ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(check, CASES))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(results, ensure_ascii=False, indent=2))
    raise SystemExit(0 if all(x['passed'] for x in results) else 1)
