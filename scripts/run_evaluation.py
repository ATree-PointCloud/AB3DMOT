import argparse
import json
from pathlib import Path

from datetime import datetime, timezone
import shutil
from uuid import uuid4

from contextlib import redirect_stdout, redirect_stderr
import os
import sys
import time
import traceback

CODE_ROOT = Path(__file__).resolve().parents[1]


def parse_args():
    parser = argparse.ArgumentParser(description='Evaluate KITTI Car tracking')
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--iou", type=float, default=0.25)
    return parser.parse_args()


def main():
    args = parse_args()
    run_dir = args.run_dir.resolve()
    metadata = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))

    config = metadata["config"]
    result_name = f"{config['det_name']}_Car_{config['split']}_H1"
    sequences = metadata["sequences"]
    result_dir = run_dir / result_name

    print("Result directory:", result_dir)
    print("Sequences:", sequences)
    print("3D IoU threshold:", args.iou)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    evaluation_id = f"eval_{timestamp}_{uuid4().hex[:8]}"
    evaluation_dir = run_dir / "evaluations" / evaluation_id
    evaluation_dir.mkdir(parents=True, exist_ok=False)

    target = evaluation_dir / result_name / "data_0"
    target.mkdir(parents=True)

    for sequence in sequences:
        shutil.copy2(
            result_dir / "data_0" / f"{sequence}.txt",
            target / f"{sequence}.txt",
        )

    print("Evaluation directory:", evaluation_dir)

    workspace = Path(metadata["workspace"])
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    os.environ["OMP_NUM_THREADS"] = "1"

    sys.path[:0] = [
        str(CODE_ROOT),
        str(CODE_ROOT / "scripts/KITTI"),
        str(workspace / "dependencies/Xinshuo_PyToolbox"),
    ]
    os.chdir(CODE_ROOT)

    evaluation_info = {
        "source_run": str(run_dir),
        "result_name": result_name,
        "sequences": sequences,
        "iou": args.iou,
        "status": "running",
    }
    info_path = evaluation_dir / "evaluation.json"
    info_path.write_text(
        json.dumps(evaluation_info, indent=2), encoding="utf-8"
    )

    start = time.perf_counter()
    with (evaluation_dir / "evaluation.log").open("x", encoding="utf-8") as log:
        with redirect_stdout(log), redirect_stderr(log):
            try:
                from scripts.KITTI.evaluate import evaluate
                from scripts.KITTI.mailpy import Mail

                success = evaluate(
                    result_sha=result_name,
                    mail=Mail(""),
                    num_hypo=1,
                    eval_3diou=True,
                    eval_2diou=False,
                    thres=args.iou,
                    results_root=evaluation_dir,
                    sequences=sequences,
                )
                if not success:
                    raise RuntimeError("Evaluation returned failure")
                evaluation_info["status"] = "completed"
            except Exception:
                evaluation_info["status"] = "failed"
                traceback.print_exc()
                raise
            finally:
                evaluation_info["wall_time_sec"] = time.perf_counter() - start
                info_path.write_text(
                    json.dumps(evaluation_info, indent=2), encoding="utf-8"
                )

    print("Evaluation completed. Log:", evaluation_dir / "evaluation.log")

if __name__ == '__main__':
    main()
