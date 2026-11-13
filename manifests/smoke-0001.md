# AB3DMOT-fork 单序列验证记录

更新：2026-11-12。

状态：当前 fork 已有远程 Car/0001 跟踪冒烟成功证据；数据对齐、完整输出验收及正式评测仍待完成，不是基线复现通过。

## 远程运行证据（用户于 2026-11-12 提供）

- 代码根：/root/autodl-tmp/AB3DMOT-fork；本次盘点 HEAD 为 cc59ee2ff8caff8cf38d89c2afef796a943b5c4a 且干净。run.json 未保存运行时 SHA/dirty diff，不能仅据盘点反推运行时版本。
- 工作区：/root/autodl-tmp/kitti-workspace。
- run_id：baseline_car_20261112T064639Z_35e2fde7。
- 命令记录：scripts/run_tracking.py --workspace /root/autodl-tmp/kitti-workspace --sequences 0001。
- run.json：status=tracking_completed，wall_time_sec=18.978275753557682。
- 配置：KITTI / pointrcnn / val / Car / H1，ego_com=true，vis=false，affi_pro=true，score_threshold=-10000。
- 日志处理到 0001/446，报告 447 帧、跟踪累计计时约 16 秒、28.1 FPS、giou_3d 阈值 -0.20；该计时不等于入口墙钟耗时，不与论文 FPS 直接比较。
- 结果：pointrcnn_Car_val_H1/data_0/0001.txt，共 3590 行。此时尚未验证结果各列、数值、ID 对唯一性及逐帧文件完整性。
- 日志中出现的内部 ID 不直接当作唯一轨迹数或真实目标数。

## 输出验收（用户后续执行，2026-11-12）

结果为 3590×18，唯一轨迹 ID 为 226；逐帧文件 447 个，空输出文件 18 个。以下断言全部通过：Car 类别、有限数值、帧号为 0–446 范围整数、ID 为正整数、三维尺寸为正、无重复帧/ID 对、逐帧文件名完整覆盖 000000.txt–000446.txt。空输出帧不等于无检测帧，ID 数不等于真实目标数。尚待验证二维输出框边界、数据对齐及标定数值；正式评测仍未执行。

后续基本数据对齐已通过：447 张非空且文件名完整图像、447×30 有限值 OXTS、4271×17 且帧号合法的 GT、1616 字节标定。详见 kitti-inputs.md。标定矩阵数值一致性和评测 GT 一致性待核对。

后续标定四个原始矩阵与解析结果逐元素一致、0001 工作区 GT 与评测器默认 GT 逐字段一致，均由用户远程执行检查通过。下一步为评测路径和序列清单适配；尚无实测评测指标。

后续逐项记录：代码 SHA/dirty diff、解释器及依赖、输入哈希、配置和序列、运行命令、日志、耗时、输出 schema/帧完整性、标定数值检查及原始评测输出。跟踪返回成功不等于基线复现通过。
