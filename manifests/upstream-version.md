# AB3DMOT-fork 来源与依赖状态

更新：2026-11-12。只记录当前项目可确认的代码事实，不继承其他项目验证结论。

## AB3DMOT

- 来源：https://github.com/xinshuoweng/AB3DMOT.git
- 当前采用直接 fork 布局，上游基点 61f3bd72574093e367916c757b4747ca445f978c。
- 本地已有标定兼容、显式路径和序列选择、Car 运行入口补丁，详见 docs/project/当前状态与下一步.md。
- 当前项目环境导入、跟踪及评测均待验证。

## Xinshuo_PyToolbox

- 预期来源：https://github.com/xinshuoweng/Xinshuo_PyToolbox.git
- 固定提交：1918b9e37ec5fb8148b8a089f226a4864d67b153；用户已克隆并切到 detached HEAD，status --short 无输出。
- 本地目录 .work/dependencies/Xinshuo_PyToolbox，符合当前入口 <workspace>/dependencies/Xinshuo_PyToolbox 契约；本地 --workspace 对应 .work。
- 需检查 xinshuo_io 等间接导入；KITTI 评测目录自带 munkres.py、mailpy.py，实际导入来源待验证。

2026-11-12：助手在当前 .venv 中将上述源码目录加入进程级 sys.path，成功导入 xinshuo_io、xinshuo_miscellaneous 和当前 fork 的 main；将 scripts/KITTI 加入进程级 sys.path 后成功导入 evaluate，evaluate.evaluate 可调用。未执行跟踪或评测。未安装辅助库 requirements，当前入口导入未出现缺包。旧 @jit 的 NumbaDeprecationWarning 和字面量 is/is not 的 SyntaxWarning 仍保留，未因此改动算法或辅助库。

## 依赖策略

requirements.txt 保留上游旧版本声明，不直接安装。requirements-project.txt 为项目直接依赖清单，不是完整锁文件。用户于 2026-11-12 明确要求不逐包安装：完成兼容性与解析检查后，使用 pip install -r requirements-project.txt 一次安装，再统一验证导入和关键功能；最后导出环境，并验证重建流程。不修改全局 Python 或已有 Conda 环境。源码辅助库仍需单独获取和固定 SHA。
