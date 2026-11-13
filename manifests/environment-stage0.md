# AB3DMOT-fork 环境记录

更新：2026-11-12。当前项目重新建立环境，不继承其他项目环境或资源结论。

## 本地只读检查

以下最初的空环境检查为历史记录；安装后的状态见文末“安装与功能验证”。

- Windows，项目 C:/Users/naihui.zhang/self-improvement/AB3DMOT-fork。
- Python：C:/Program Files/Python311/python.exe，3.11.8；py 启动器可用。
- 已发现 Conda 命令，未盘点其解释器与环境，不修改已有环境。
- 项目 .venv 已存在，Python 3.11.8；本轮直接运行其解释器，确认 sys.executable 和 sys.prefix 位于项目 .venv，sys.base_prefix 为 C:/Program Files/Python311。
- pyvenv.cfg：include-system-site-packages=false；pip 24.0 来自项目 .venv/Lib/site-packages，pip list 仅列出 pip 24.0、setuptools 65.5.0。未安装或验证项目依赖。
- .idea/misc.xml 的 ProjectRootManager 已选择本项目 Python 3.11 virtualenv；用户于 2026-11-12 提供 PyDev Console 输出，sys.executable、sys.prefix 均指向本项目 .venv，sys.base_prefix 为 C:/Program Files/Python311。IDE 实际解释器验证通过，不需重建 .venv。

## 远程

AutoDL 是计划中的验证平台。当前工作区路径、代码版本、解释器、CPU/内存配额、磁盘余量和连接方式均待重新核实。不假定任何项目目录已存在。

### 远程重新盘点（2026-11-12，用户终端输出）

- 通过 AutoDL Linux 终端执行，当前用户 root、初始工作目录 /root；提示符处于 base 环境，项目解释器尚未核实。
- /root/autodl-tmp 数据盘：282G，总占用 250G，可用约 33G，使用率 89%（df -h 显示值）。
- /root/autodl-tmp/AB3DMOT-fork 与 /root/autodl-tmp/kitti-workspace 均存在；尚未检查内部结构及代码 SHA，不直接认定可运行。
- 历史路径 /root/autodl-tmp/kitti-AB3DMOT 不存在。
- 同盘还有 ComfyUI、RGBD_fusion、fusion_data、video-agent 等目录；不修改其他项目。
- 下一步只读检查两个候选目录、Git 状态、工作区 Python 及 cgroup 配额，不重复下载或创建环境。

### 远程代码、目录及资源确认（同日后续输出）

- 代码目录 /root/autodl-tmp/AB3DMOT-fork，HEAD 为 cc59ee2ff8caff8cf38d89c2afef796a943b5c4a；git status --short 无输出，工作区干净。当前本地未提交的文档更新不视为已同步。
- 运行工作区 /root/autodl-tmp/kitti-workspace 已存在，含 .venv/lib/python3.10、cache、datasets/KITTI/tracking、datasets/downloads、dependencies/Xinshuo_PyToolbox、environment 和 runs。目录存在不等于环境、数据已验证。
- 已发现 runs/baseline_car_20261112T064639Z_35e2fde7/pointrcnn_Car_val_H1；运行状态、日志、结果内容待检查，不据目录名宣称成功。
- cpu.max 为 50000 100000，相当于 0.5 核 CPU 时间配额；memory.max 为 2147483648，即 2GiB。
- 下一步复核现有 .venv、辅助库 SHA、0001 数据和已存在 run.json，不重复创建环境或盲目复跑。

### 远程解释器及源码确认（用户后续输出）

- /root/autodl-tmp/kitti-workspace/.venv/bin/python 为 Python 3.10.8；sys.prefix 指向工作区 .venv，sys.base_prefix=/root/miniconda3。
- 该解释器执行 pip check 返回 No broken requirements found；实际发行包版本及完整导入仍需另行归档/验证，不据此假定与本地 Windows 版本相同。
- 辅助库 HEAD 为 1918b9e37ec5fb8148b8a089f226a4864d67b153，status --short 无输出，工作区干净。
- 现有运行记录、日志及结果行数相互印证跟踪完成，详见 smoke-0001.md；正式评测尚未执行。

## 依赖可见性检查（2026-11-12）

用户在已确认解释器的 PyDev Console 使用 importlib.util.find_spec 检查 numpy、scipy、filterpy、yaml、xinshuo_io，五项均返回 None。结论为当前 Console 的模块搜索路径无法找到这些模块，尚未执行功能验证。

下一步指导用户安装 numpy==1.23.5，再验证版本、模块路径及基本状态向量运算；安装和检查均待用户执行。已核对 PyPI 该版本提供 CPython 3.11 / Windows x86-64 wheel：https://pypi.org/project/numpy/1.23.5/ 。这只确认有适配发行包，不代表完整项目兼容性已验证。

## 批量安装预检（2026-11-12）

用户随后明确要求不逐包安装，上述单包安装计划由本节替代。使用当前 .venv Python 3.11.8 / Windows x86-64 执行：

```powershell
.\.venv\Scripts\python.exe -m pip install --dry-run --ignore-installed --report .venv/dependency-plan.json -r requirements-project.txt --index-url https://pypi.org/simple
```

退出码 0，直接依赖及其传递依赖可解析，计划包含 26 个发行包；未向项目环境安装包。默认 USTC 镜像首次访问 DNS 失败，改用官方 PyPI 完成预检。报告保存在被忽略的 .venv 下，仅供本地检查，不是最终环境锁文件。

结论：原始 requirements.txt 的旧版本组合不用于当前解释器；requirements-project.txt 可以进入一次安装和统一验证阶段。解析通过不代表构建、实际导入或跟踪已经成功。FilterPy、easydict、glob2 使用源码发行包，dry-run 已完成构建元数据准备，实际安装构建仍待验证。Xinshuo_PyToolbox 源码尚未获取核查，不能保证辅助库的全部间接导入已覆盖；nuScenes 和视频生成等可选功能不在本清单验收范围。安装后执行 pip check、关键数值检查与入口导入，再导出实际环境。

## 安装与功能验证（2026-11-12）

用户完成整份清单安装并提供 pip check 成功输出；助手随后在同一项目 .venv 直接验证：

- 13 个模块导入通过：numpy、scipy、numba、llvmlite、matplotlib、filterpy、yaml、easydict、glob2、cv2、skimage、terminaltables、PIL。
- Numba njit 编译数组求和通过；SciPy linear_sum_assignment 二目标分配结果符合预期。
- 直接使用项目 AB3DMOT_libs.kalman_filter.KF，10 维状态预测到预期位置，7 维观测更新后数值有限，innovation matrix 为 7×7。
- 助手复查 pip check：No broken requirements found。

实际 pip freeze 保存至 environment-local-py311-windows.txt，仅为当前 Windows / Python 3.11.8 环境快照；尚未验证从快照重建，不直接当作远程 Linux 锁文件。完整 tracking/evaluation 导入仍需获取固定 SHA 的 Xinshuo_PyToolbox 并检查间接依赖。

后续入口验证：辅助库固定版本获取后，进程级 sys.path 指向 .work/dependencies/Xinshuo_PyToolbox，xinshuo_io、xinshuo_miscellaneous、当前 main 导入成功；添加 scripts/KITTI 后 evaluate 模块导入成功且 evaluate 函数可调用。退出码 0，无新增依赖安装；未启动跟踪或评测。警告及版本记录见 upstream-version.md。
