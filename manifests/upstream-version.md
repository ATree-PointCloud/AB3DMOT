# 上游版本与依赖检查

## AB3DMOT

- 来源：https://github.com/xinshuoweng/AB3DMOT.git
- 本地目录：third_party/AB3DMOT
- 固定提交：61f3bd72574093e367916c757b4747ca445f978c
- 用户及本地检查确认：该提交工作区无修改。
- 远程已获取；用户输出确认 SHA 与本地一致，切换前工作区干净，已使用 detached HEAD。
- 后续远程使用此 SHA，不以移动的分支名作为复现版本。

## 静态检查结果

- docs/INSTALL.md 声明原测试组合为 Ubuntu 18.04、Python 3.6；当前远程为 Ubuntu 22.04、base Python 3.10.8，不能直接假设兼容。
- requirements.txt 包含旧版 scikit-learn 0.19.2、numba 0.43.1、llvmlite 0.32.1 等，暂不在 base 或本地 .venv 中直接安装。
- 安装文档与 requirements 的 Pillow 要求不同：文档列 6.2.2，文件要求 >=8.3.2。
- 还需作者辅助库 Xinshuo_PyToolbox，入口直接导入 xinshuo_io、xinshuo_miscellaneous。辅助库提交及实际依赖尚待检查。
- Python 与依赖方案尚未确定；先检查辅助库和实际导入，再确定隔离环境与必要兼容补丁。任何方案都需导入及运行验证。

## Xinshuo_PyToolbox

- 来源：https://github.com/xinshuoweng/Xinshuo_PyToolbox.git
- 本地目录：third_party/Xinshuo_PyToolbox
- 固定提交：1918b9e37ec5fb8148b8a089f226a4864d67b153
- 用户确认本地工作区无修改；远程切换前工作区干净，已使用 detached HEAD，SHA 与本地一致。
- 辅助库 requirements 未固定版本，包含 scikit-learn、scikit-image、scikit-video、OpenCV 等，不直接无约束批量安装。
- xinshuo_io 的 __init__.py 会同时导入 file_io、images_io、pts_io；实际依赖检查需追踪间接导入，不能只看 main.py。
- KITTI evaluate.py 还直接依赖 munkres，而 AB3DMOT 根 requirements 未列出它；需纳入评测环境检查。

本地为代码及记录依据；远程负责运行验证。已完成获取、静态检查和核心依赖验证，尚未完成跟踪/评测入口验证或运行基线。

## 下一步环境方案（待执行验证）

先使用远程已有 /root/miniconda3/bin/python3（3.10.8）通过 venv 在数据盘创建隔离环境，不继承 base 的第三方包。此方案旨在探索现代 Python 兼容运行，不是原作者 Python 3.6 环境的原样重建；是否可用需经依赖导入、运行与基线评测验证。

环境路径：/root/autodl-tmp/kitti-AB3DMOT/.venv。缓存和临时目录也放在数据盘。暂不直接安装旧 requirements，不修改 base 或 h3。

用户输出已验证：远程 .venv 创建成功；Python 3.10.8，pip 22.2.2；sys.executable 和 sys.prefix 指向项目 .venv，sys.base_prefix 为 /root/miniconda3。

## 核心依赖验证结果

用户贴回：numpy 1.23.5、scipy 1.10.1、numba 0.57.1、llvmlite 0.40.1、matplotlib 3.7.5、filterpy 1.4.5；Numba 编译计算、分配计算、卡尔曼预测/更新均为 OK；pip check 返回 No broken requirements found。

本地根 requirements.txt 已记录这些版本，尚未包含完整运行依赖或全部间接依赖；从该文件全新安装尚未单独验证。后续入口验证通过后补齐，并导出最终环境版本清单。

## 配置依赖验证（2026-11-11）

- 用户远程输出确认 PyYAML 6.0.1、easydict 1.9；yaml.safe_load 与 EasyDict 属性访问的联合检查通过。
- easydict 使用 setup.py install 安装成功；缺少 wheel 的提示未阻止本次安装，不因此升级 pip 或改动其他环境。
- 跟踪入口此前依次阻塞于 yaml、easydict；安装后的 main.py --help 结果待用户提供。
- main.py 的字符串 is not 比较产生 SyntaxWarning，尚未修改上游代码。
- 按用户当前约定，远程继续逐步执行安装与验证，不通过 requirements.txt 批量安装；验证结果保留本地。

## 辅助库导入推进

- 用户确认 glob2 0.6 导入成功，并通过 AB3DMOT_libs/*.py 搜索找到 box.py 的功能检查。
- 当前入口阻塞：xinshuo_io → images_io → xinshuo_images → image_processing，缺少 cv2。
- 下一步拟安装 opencv-python-headless 4.8.1.78（待验证），供无界面图像处理；无需为导入 cv2 安装 GPU 或桌面环境。它替代上游的 opencv-python，环境中不同时安装两者。

- 用户后续确认 cv2 报告 4.8.1、NumPy 1.23.5；灰度转换检查通过，pip check 无冲突。cv2 版本不含安装发行包的 .78 后缀，该后缀尚未通过包元数据单独核实。
- 当前 main.py --help 阻塞于 xinshuo_visualization/geometry_vis.py 导入 skimage.measure.find_contours，缺少 skimage；下一步拟安装 scikit-image 0.21.0，待验证。
- 导入时出现 NumbaDeprecationWarning：旧 @jit 未显式指定 nopython；当前版本未因此退出，暂保留警告，不改代码、不升级 Numba。

- 用户确认 scikit-image 0.21.0，find_contours 轮廓提取检查通过；pip check 无冲突。
- 最新入口阻塞于 xinshuo_visualization/prob_stat_vis.py 导入 terminaltables.AsciiTable；拟安装 terminaltables 3.1.10，尚待验证。

- 后续用户输出确认 terminaltables 3.1.10 表格生成检查通过，pip check 无冲突；main.py --help 成功显示 dataset、split、det_name 参数，跟踪入口导入检查通过。SyntaxWarning 与 NumbaDeprecationWarning 仍保留。
- 此结果尚不代表实际跟踪或评测通过；下一步独立检查评测模块导入，避免评测脚本的命令行副作用。

- 用户后续确认评测模块加载成功，evaluate 函数可调用；munkres 和 mailpy 均来自仓库 scripts/KITTI。没有启动评测或发送消息。evaluate.py 第 296 行另有 is -1 的 SyntaxWarning，尚未修改。
- 跟踪与评测入口静态导入关卡通过；实际数据读取、JIT 运行兼容性和正式指标尚未验证。
