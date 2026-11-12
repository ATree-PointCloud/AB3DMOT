# 阶段 0 环境记录

记录日期：2026-11-10。依据：用户贴回的远程命令输出、控制台截图及存储规则确认；助手未直接登录服务器。

状态：阶段 0 基础盘点完成。终端接入已验证，SSH 接入方式未单独验证。

## 运行环境

- 系统：Ubuntu 22.04.3 LTS，x86_64；用户：root。
- 远程项目目录：/root/autodl-tmp/kitti-AB3DMOT，初始为空，位于数据盘。
- 当前启动方式：无卡模式。
- CPU：Intel Xeon Platinum 8474C；宿主机可见 192 个逻辑 CPU，不是实例配额。
- 当前 cpu.max：50000 100000，即 0.5 核 CPU 时间配额；Cpus_allowed_list 为 0-191；nproc 为 1。
- 当前 memory.max：2147483648 字节，即 2GiB；free 显示的宿主机内存不能作为实例额度。
- 控制台标称配置：15 vCPU、80GB 内存、RTX 4090D 24GB × 1。正常开机后的实际配额待检查。

## 存储

- 系统盘：30GB，检查时剩余约 3.1GB。
- 数据盘：282GB，已用约 248GB，剩余约 35GB；挂载于 /root/autodl-tmp。
- 主要已有占用：fusion_data 约 202GB、ComfyUI 约 45GB、agent 约 1.2GB、RGBD_fusion 约 447MB。保留其他项目数据。
- 用户确认：普通关机后保留数据；释放实例后删除，无需另考虑保留期限。
- /autodl-pub 等公共挂载容量不计为个人可用存储。

## 已有工具

- Python：/root/miniconda3/bin/python，3.10.8；当前 base 环境。
- Conda 环境：base、h3。conda env list 成功，但出现 RequestsDependencyWarning，涉及 requests 的依赖版本兼容；暂不改动 base 或 h3。
- Git：2.34.1。
- tmux：command -v 未找到。

## 执行约定与下一步

- 本地项目为准，维护文档、学习记录、脚本和配置；远程只负责脚本运行和验证，不要求维护 Markdown 文档。
- 远程产生的原始日志、结果和环境导出需回收至本地，避免释放实例后丢失；后续确定同步方式。
- 项目建立独立 Python 环境；因系统盘空间紧张，优先评估数据盘上的环境及缓存位置。
- 当前不配置 CUDA，不下载完整数据。先获取并锁定上游代码，检查实际依赖，再选择 Python 版本。
- 无卡模式用于轻量准备；正式评测前根据冒烟耗时和内存占用决定是否切换正常模式，并复查配额。
