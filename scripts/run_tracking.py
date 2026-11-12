import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import time
from uuid import uuid4


CODE_ROOT = Path(__file__).resolve().parents[1]


def parse_args():
    parser = argparse.ArgumentParser(description="Run KITTI Car tracking")
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--sequences", nargs="+", required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    workspace = args.workspace.resolve()

    tracking_root = workspace / "datasets/KITTI/tracking"
    toolbox_root = workspace / "dependencies/Xinshuo_PyToolbox"
    detection_dir = CODE_ROOT / "data/KITTI/detection/pointrcnn_Car_val"

    if not toolbox_root.is_dir():
        raise FileNotFoundError(toolbox_root)

    # 在线程库导入前设置，适应当前无卡模式的 CPU 配额。
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    os.environ["OMP_NUM_THREADS"] = "1"

    sys.path.insert(0, str(toolbox_root))
    sys.path.insert(0, str(CODE_ROOT))

    import main as tracking_module
    from AB3DMOT_libs.utils import Config

    if Path(tracking_module.__file__).resolve() != CODE_ROOT / "main.py":
        raise RuntimeError("Imported an unexpected tracking module")

    cfg, _ = Config(str(CODE_ROOT / "configs/KITTI.yml"))
    cfg.dataset = "KITTI"
    cfg.split = "val"
    cfg.det_name = "pointrcnn"
    cfg.cat_list = ["Car"]

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"baseline_car_{timestamp}_{uuid4().hex[:8]}"
    run_dir = workspace / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    cfg.save_root = str(run_dir)

    metadata = {
        "run_id": run_id,
        "code_root": str(CODE_ROOT),
        "workspace": str(workspace),
        "sequences": args.sequences,
        "tracking_root": str(tracking_root),
        "detection_dir": str(detection_dir),
        "config": dict(cfg),
        "command": sys.argv,
        "status": "running",
    }

    def save_metadata():
        (run_dir / "run.json").write_text(
            json.dumps(metadata, indent=2),
            encoding="utf-8",
        )

    save_metadata()
    print("Run directory:", run_dir, flush=True)
    print("Sequences:", args.sequences, flush=True)

    start = time.perf_counter()
    try:
        with (run_dir / "tracking.log").open("x", encoding="utf-8") as log:
            tracking_module.main_per_cat(
                cfg,
                "Car",
                log,
                1,
                tracking_root=tracking_root,
                detection_dir=detection_dir,
                sequences=args.sequences,
            )
        metadata["status"] = "tracking_completed"
    except Exception as error:
        metadata["status"] = "failed"
        metadata["error"] = repr(error)
        raise
    finally:
        metadata["wall_time_sec"] = time.perf_counter() - start
        save_metadata()

    print(f"Wall time: {metadata['wall_time_sec']:.3f}s")
    print("Tracking completed; evaluation has not been performed.")


if __name__ == "__main__":
    main()