# Linux 入门与阶段 0 环境检查命令详解

依据：本项目阶段 0 用户提供的 AutoDL 终端输出。输出是检查时的快照，不代表以后开机的状态。本文中的“注”是解释文字，不是终端原始输出；示例中的提示符不需要复制。

## 1. 最基础的 Linux 命令速查

以下命令在远程 Linux 终端执行。Linux 路径使用 `/`，文件名区分大小写。

| 命令 | 功能 | 入门示例 |
|---|---|---|
| `pwd` | 显示当前工作目录 | `pwd` |
| `ls` | 列出目录内容 | `ls -lah` |
| `cd` | 切换当前目录，是 Shell 内建命令 | `cd /root/autodl-tmp/kitti-AB3DMOT` |
| `mkdir` | 创建目录 | `mkdir -p docs`，父目录不存在时一起创建，目录已存在不报错 |
| `cat` | 显示文本文件全部内容 | `cat /etc/os-release` |
| `less` | 分页阅读文本 | `less README.md`；方向键滚动，`q` 退出 |
| `head` / `tail` | 查看文件开头 / 结尾 | `head -n 20 README.md`；`tail -n 50 run.log` |
| `grep` | 按文本模式筛选行 | `grep CPU info.txt`；默认区分大小写 |
| `cp` | 复制文件 | `cp config.yml config-backup.yml` |
| `mv` | 移动或重命名 | `mv old.txt new.txt` |
| `rm` | 删除文件，通常不会进入回收站 | `rm temporary.txt`；执行前确认对象 |
| `du` | 统计文件或目录占用 | `du -h --max-depth=1 .` |
| `df` | 查看文件系统容量和可用空间 | `df -hT .` |
| `command -v` | 查询 Shell 如何找到一个命令 | `command -v python` |
| `man` / `--help` | 查看手册 / 用法 | `man ls`；`ls --help` |
| `exit` | 退出当前 Shell 会话 | `exit` |

路径基础：`/` 是文件系统根目录，`/root` 是 root 用户的家目录，两者不同；`~` 表示当前用户的家目录；`.` 表示当前目录，`..` 表示上一级；以 `/` 开头的是绝对路径，其他通常是相对路径。路径包含空格时用引号包住。

命令的基本结构是 `命令 选项 参数`。例如 `ls -lah /root` 中，`ls` 是命令，`-lah` 是三个短选项的组合，`/root` 是要查看的路径。不是所有命令都支持同样的选项。

常见终端符号：

| 符号 | 含义 |
|---|---|
| `|` | 管道，把左侧命令的标准输出交给右侧命令 |
| `>` | 将标准输出写入文件，文件已存在时覆盖 |
| `>>` | 将标准输出追加到文件末尾 |
| `2>` | 重定向标准错误；`2` 是标准错误的文件描述符编号 |
| `#` | 在命令语境中可开始注释；提示符末尾的 `#` 则通常表示 root Shell |
| `Ctrl+C` | 中断当前前台命令 |
| `Tab` | 补全命令或路径 |
| 上方向键 | 调出之前执行的命令 |

## 2. 先读懂终端提示符

实际提示符：

```text
(base) root@autodl-container-1a244d9c2a-2cee6640:~/autodl-tmp/kitti-AB3DMOT#
```

- `(base)`：当前激活 Conda 的 base 环境，不是项目专用环境。
- `root`：当前用户名。
- `@` 后、冒号前：容器主机名。
- `~/autodl-tmp/kitti-AB3DMOT`：当前目录；本次 `~` 对应 `/root`。
- 末尾 `#`：常见的 root 提示符；普通用户通常是 `$`。提示符可以自定义，判断身份仍以 `whoami` 为准。

例如执行 `pwd` 时，只输入 `pwd`，不输入前面的提示符。

## 3. 系统与目录验证

### 3.1 `cat /etc/os-release`

`cat` 读取并显示文件；`/etc/os-release` 保存发行版身份信息。它描述用户空间发行版，不能单独证明宿主机系统或 Linux 内核版本。

| 实际输出行 | 逐行注释 |
|---|---|
| `PRETTY_NAME="Ubuntu 22.04.3 LTS"` | 面向人的完整发行版名称；LTS 表示长期支持版本 |
| `NAME="Ubuntu"` | 发行版通用名称 |
| `VERSION_ID="22.04"` | 供程序判断的版本标识 |
| `VERSION="22.04.3 LTS (Jammy Jellyfish)"` | 详细版本及代号 |
| `VERSION_CODENAME=jammy` | 本发行版代号 |
| `ID=ubuntu` | 机器可读的发行版 ID |
| `ID_LIKE=debian` | 所属或相近的发行版家族 |
| `HOME_URL="https://www.ubuntu.com/"` | 发行版主页 |
| `SUPPORT_URL="https://help.ubuntu.com/"` | 支持页面 |
| `BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"` | 问题报告入口 |
| `PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"` | 隐私政策入口 |
| `UBUNTU_CODENAME=jammy` | Ubuntu 专用的代号字段 |

### 3.2 `whoami`

输出 `root`：当前有效用户名是 root。它权限较高，但在容器中仍受容器权限、挂载和资源限制约束，不等于拥有宿主机全部权限。

### 3.3 `pwd`

输出 `/root/autodl-tmp/kitti-AB3DMOT`：当前工作目录。相对路径通常从这里开始解析；它不是 Windows 本地项目路径。

### 3.4 `ls -lah`

`-l` 使用详细列表，`-a` 包括以点开头的隐藏项，`-h` 使用便于阅读的大小单位。

```text
total 4.0K
drwxr-xr-x  2 root root   10 Nov  5 17:23 .
drwxr-xr-x 10 root root 4.0K Nov  5 17:24 ..
```

- 第一行：列出项占用的文件系统块总量经换算后的结果，不是目录内全部文件大小的递归统计。
- 第二行：当前目录 `.`。首字符 `d` 表示目录；随后 `rwx` 是所有者可读、可写、可进入；`r-x` 是所属组可读、可进入；最后 `r-x` 是其他用户可读、可进入。`2` 为硬链接计数；两个 `root` 分别是所有者和所属组；`10` 是目录自身的大小字段，不是内部数据总量；日期是修改时间。
- 第三行：上一级目录 `..`，字段解释同上。`10` 是硬链接计数，`4.0K` 是该目录自身大小。

只显示 `.` 和 `..`，说明当时项目目录没有其他条目。

### 3.5 `ls -ld /root/autodl-tmp`

`-l` 显示详细信息；`-d` 查看目录条目本身，而不是列出其内部文件。

```text
drwxr-xr-x 10 root root 4096 Nov  5 17:24 /root/autodl-tmp
```

这一行的字段依次是：目录类型及权限、硬链接计数 10、所有者 root、所属组 root、目录自身大小 4096 字节、修改时间、目录路径。首字符为 `d`，说明该条目是目录；若是符号链接，通常为 `l` 并显示 `->` 目标。目录也可能是挂载点，不能因它不是链接就认定属于系统盘。

### 3.6 `readlink -f /root/autodl-tmp/kitti-AB3DMOT`

`readlink` 处理符号链接；`-f` 规范化路径并解析沿途链接。它解决“路径最终指向哪里”，不回答“哪个文件系统提供容量”。后者用 `df`。

用户贴出的记录是：

```text
readlink -f /root/autodl-tmp/kitti-AB3DMOT/root/autodl-tmp/kitti-AB3DMOT
```

命令和可能的输出疑似粘连，无法据此认定命令成功或认定真实路径。如果确实输入了这一整串，就是查询了错误的长路径；若没有输出，也不应把预期路径当作实测结果。需要时重新单独执行正确命令。

## 4. CPU、内存与容器配额验证

### 4.1 `lscpu | head -n 20`

`lscpu` 汇总 CPU 架构信息；管道交给 `head`；`-n 20` 只保留前 20 行。因此这是截取的输出，不是完整信息。

| 实际输出行 | 逐行注释 |
|---|---|
| `Architecture: x86_64` | 64 位 x86 架构 |
| `CPU op-mode(s): 32-bit, 64-bit` | CPU 支持的运行模式，不表示当前同时运行两种系统 |
| `Address sizes: 46 bits physical, 57 bits virtual` | 物理和虚拟地址位宽，不是已分配内存大小 |
| `Byte Order: Little Endian` | 多字节数据按小端字节序存储 |
| `CPU(s): 192` | 系统可见逻辑 CPU 数量；容器中不等于可使用 192 核算力 |
| `On-line CPU(s) list: 0-191` | 可见的在线逻辑 CPU 编号 |
| `Vendor ID: GenuineIntel` | CPU 厂商标识 |
| `Model name: Intel(R) Xeon(R) Platinum 8474C` | CPU 型号 |
| `CPU family: 6` | 处理器家族编号，用于硬件识别 |
| `Model: 143` | 家族内的型号编号 |
| `Thread(s) per core: 2` | 每个物理核心呈现两个硬件线程 |
| `Core(s) per socket: 48` | 每个插槽 48 个物理核心 |
| `Socket(s): 2` | 可见拓扑包含两个 CPU 插槽；48 × 2 × 2 = 192 个逻辑 CPU |
| `Stepping: 8` | 硬件修订标识 |
| `Frequency boost: enabled` | 显示动态加速功能启用，不保证实例持续获得特定频率 |
| `CPU max MHz: 2101.0000` | 系统报告的频率上限字段，不是当前实测吞吐或云端配额 |
| `CPU min MHz: 800.0000` | 系统报告的频率下限字段 |
| `BogoMIPS: 4200.00` | 内核延时校准相关值，不能用于比较项目性能 |
| `Flags: fpu vme ... arch_capabilities` | 一整行 CPU 功能标记；省略号仅为本文缩写。包括基础指令、虚拟化及向量计算能力，例如 `vmx`、`avx2`、`avx512f`；不是已安装的软件包列表 |
| `Virtualization: VT-x` | CPU 暴露 Intel 虚拟化能力，不证明容器获准创建嵌套虚拟机 |

以上主要用于辨认硬件与架构，不能替代 cgroup 配额检查。

### 4.2 `free -h`

`free` 显示内存和交换空间统计；`-h` 自动选择便于阅读的单位。

```text
               total        used        free      shared  buff/cache   available
Mem:           1.0Ti        72Gi       168Gi       8.3Gi       766Gi       920Gi
Swap:             0B          0B          0B
```

- 表头：`total` 总量；`used` 已用量；`free` 完全空闲量；`shared` 共享内存相关量；`buff/cache` 缓冲和缓存；`available` 系统估计无需交换即可提供给新工作负载的内存。字段算法依工具版本而异，不能把各列随意重复相加。
- `Mem` 行：当前接口报告总内存约 1TiB，已用 72GiB、空闲 168GiB、共享 8.3GiB、缓存 766GiB、估计可用 920GiB。这里显示更大范围的内存，并未体现本容器 2GiB 上限。
- `Swap` 行：该视图下交换空间总量、使用量、剩余量都为 0。不能据此跳过容器独立的资源限制检查。

`GiB = 1024³` 字节，`TiB = 1024⁴` 字节；十进制 `GB = 1000³` 字节，两者不相同。

### 4.3 `nproc`

查询当前进程可用处理单元数量，输出为整数，本次是 `1`。具体计算受工具版本、进程限制及环境影响；它不是精确的小数 CPU 配额报告。本次应结合 `cpu.max`，不能把 1 解读为独占完整一核。

### 4.4 `cat /proc/self/cgroup`

`/proc` 是内核提供的进程信息接口；`self` 表示读取该路径的进程自身。

```text
0::/
```

这一行按冒号分成三段：`0` 表示 cgroup v2 统一层级；中间为空是 v2 的格式；`/` 是当前命名空间视图内的 cgroup 路径。它不表示“没有资源限制”，也不一定是宿主机的全局根 cgroup。

### 4.5 `grep Cpus_allowed_list /proc/self/status`

`grep` 从进程状态文件中筛选包含 `Cpus_allowed_list` 的行。

```text
Cpus_allowed_list:      0-191
```

允许被调度的逻辑 CPU 编号范围为 0 到 191。它回答“可以在哪些 CPU 上执行”，没有回答“每单位时间可以执行多久”。调度范围和 CPU 时间额度是不同维度。

### 4.6 `cat /sys/fs/cgroup/cpu.max`

读取当前 cgroup 视图根目录的 CPU 带宽限制文件：

```text
50000 100000
```

两个数单位都是微秒，分别是配额和周期：每 100000 微秒（100ms），该组最多消耗 50000 微秒（50ms）的 CPU 时间。比值 `50000 / 100000 = 0.5`，即平均相当于 0.5 核算力。多线程共享这份额度，不会因启动多个进程而成倍增加。

若第一个字段是 `max`，表示这一层没有该项上限，仍可能受祖先 cgroup 等限制。本次结果已经足以说明当前容器受到显著限制。

### 4.7 `cat /sys/fs/cgroup/memory.max`

```text
2147483648
```

单位为字节：`2147483648 / 1024 / 1024 / 1024 = 2GiB`。这是该 cgroup 内相关进程共同使用的上限，不是每个 Python 进程各有 2GiB；内存计费还包含相应缓存等内容。触及限制可能触发回收或 OOM 处理，不保证每次都以友好的 Python 异常结束。

总结本次判断：`lscpu` / `free` 展示硬件或系统视图，控制台展示标称实例配置，cgroup 文件揭示当前无卡模式的实际限制。模式切换后应重新读取，不能沿用这次额度。

## 5. 磁盘与目录占用验证

### 5.1 `df -hT`

`df` 查询已挂载文件系统；`-h` 换算容量单位；`-T` 显示类型。每行的列依次为 `Filesystem` 来源、`Type` 类型、`Size` 总容量、`Used` 已用、`Avail` 可用、`Use%` 使用率、`Mounted on` 挂载位置。

以下逐行对应首次输出。容量为当时的显示值，带 `-h` 的值经过取整。

| 来源与挂载位置 | 容量字段与解释 |
|---|---|
| `overlay` → `/`，类型 `overlay` | `30G 27G 3.1G 90%`：容器根文件系统，空间紧张 |
| `/dev/md0` → `/autodl-pub`，类型 `xfs` | `7.0T 6.7T 303G 96%`：这个挂载视图的统计，不是个人数据盘配额 |
| `AutoFS:fs1` → `/autodl-pub/data`，类型 `fuse.autofs` | `4.0T 2.6T 1.5T 65%`：另一个挂载文件系统；不能直接当作个人可写空间 |
| `tmpfs` → `/dev`，类型 `tmpfs` | `64M 0 64M 0%`：设备目录的内存型文件系统，不是额外持久磁盘 |
| `shm` → `/dev/shm`，类型 `tmpfs` | `2.0G 0 2.0G 0%`：共享内存文件系统；大小是挂载容量，不代表额外赠送 2GiB 内存 |
| `/dev/mapper/ubuntu--vg-ubuntu--lv` → `/usr/bin/nvidia-smi`，类型 `ext4` | `98G 16G 78G 18%`：文件级挂载所关联的文件系统统计，不表示该可执行文件有 78G 可用存储 |
| `tmpfs` → `/proc/driver/nvidia` | `504G 12K 504G 1%`：内存型挂载视图，不是可用于存数据的个人磁盘 |
| `tmpfs` → `/etc/nvidia/nvidia-application-profiles-rc.d` | `504G 0 504G 0%`：同样不能算作个人持久容量 |
| `tmpfs` → `/proc/asound` | `504G 0 504G 0%`：内核相关路径上的挂载视图 |
| `tmpfs` → `/proc/acpi` | `504G 0 504G 0%`：同上 |
| `tmpfs` → `/proc/scsi` | `504G 0 504G 0%`：同上 |
| `tmpfs` → `/sys/firmware` | `504G 0 504G 0%`：同上 |

不要把这些行的容量相加作为实例总空间。挂载可能来自公共目录、单文件绑定或内存型文件系统；持久化规则也无法仅凭 `df` 判断。

### 5.2 `df -hT /root/autodl-tmp/kitti-AB3DMOT`

增加路径参数后，只查询包含该路径的文件系统。本次输出：

```text
Filesystem     Type  Size  Used Avail Use% Mounted on
/dev/md0       xfs   282G  248G   35G  88% /root/autodl-tmp
```

- 表头：含义同上一节。
- 数据行：项目目录属于挂载在 `/root/autodl-tmp` 的数据盘视图，来源 `/dev/md0`，类型 XFS，总量约 282G，已用 248G，可用 35G，使用率 88%。各容量独立取整，不要求显示值精确相加相等。

这个结果比从全部挂载中猜测项目位置更直接。虽然与公共挂载出现相同来源名，也不应把两者容量互换使用；本项目按路径查询结果规划空间。

### 5.3 `du -h --max-depth=1 /root/autodl-tmp 2>/dev/null`

- `du`：遍历目录，统计磁盘占用。
- `-h`：显示可读的容量单位。
- `--max-depth=1`：只打印根目录及第一层子目录的汇总；统计子目录总量仍需要遍历其内部，不是只扫描一层。
- `/root/autodl-tmp`：统计目标。
- `2>/dev/null`：把标准错误丢弃。若遇到访问错误，结果可能不完整而你看不到原因；排障时去掉这一部分重跑。

| 输出行 | 注释 |
|---|---|
| `3.2M /root/autodl-tmp/.autodl` | 该隐藏目录约占 3.2M |
| `45G /root/autodl-tmp/ComfyUI` | 已有 ComfyUI 项目约占 45G |
| `0 /root/autodl-tmp/kitti-AB3DMOT` | 当时该目录未计得数据块占用，不表示它不存在 |
| `80M /root/autodl-tmp/.Trash-0` | 此目录约占 80M；仅凭名字不自动执行清理 |
| `0 /root/autodl-tmp/.ipynb_checkpoints` | 未计得数据块占用 |
| `q202G /root/autodl-tmp/fusion_data` | 其中 `q` 是终端误输入或显示混入的字符；容量部分为 202G，后续可复查，不能把 `q` 当单位 |
| `1.2G /root/autodl-tmp/agent` | 该目录约占 1.2G |
| `447M /root/autodl-tmp/RGBD_fusion` | 该目录约占 447M |
| `248G /root/autodl-tmp` | 目标目录汇总约占 248G，已包含上面的子目录，不再重复相加 |

`df` 关注整个文件系统容量；`du` 关注指定目录树的占用。它们可能因为配额、其他目录、已删除但仍打开的文件、权限、取整等因素出现差异。

## 6. Python、Conda、Git 与 tmux 验证

### 6.1 `command -v python` 与 `command -v python3`

这是 Shell 对命令的解析查询，不会运行 Python。

```text
/root/miniconda3/bin/python
/root/miniconda3/bin/python3
```

第一行对应 `python`，第二行对应 `python3`。二者当前都由 Miniconda 目录提供，不能仅凭名字认为 `python3` 来自系统安装。激活其他环境后路径可能改变。

### 6.2 `python3 --version`

运行当前解析到的 `python3` 并请求版本号。

```text
Python 3.10.8
```

这一行说明当前解释器版本，不证明 AB3DMOT 依赖已兼容或安装。项目 Python 版本要在检查上游依赖后决定。

### 6.3 `command -v conda`

```text
conda
```

输出为命令名而非绝对路径。Shell 中 Conda 可能以函数方式初始化，因此不能据此判断安装目录。已验证事实是当前 Shell 能解析这个命令；后面的 `conda env list` 进一步验证它能够运行。

### 6.4 `git --version`

```text
git version 2.34.1
```

请求 Git 程序版本，输出表示 Git 可运行且版本为 2.34.1；不证明当前目录已经是 Git 仓库，也不证明远程网络连通。

### 6.5 `conda env list`

`env list` 是 Conda 的环境列表子命令。本次先出现两次相同警告，每次由两行组成：

```text
/root/miniconda3/lib/python3.10/site-packages/requests/__init__.py:109: RequestsDependencyWarning: urllib3 (1.26.13) or chardet (7.7.0)/charset_normalizer (2.0.4) doesn't match a supported version!
  warnings.warn(
```

- 第一行：警告来自 base 环境中的 requests 包，第 109 行；当前组合的 urllib3、chardet 或 charset_normalizer 版本不符合其支持检查。它没有证明究竟哪一个包应升级或降级。
- 第二行：显示触发警告的源代码片段，不是要求用户输入 `warnings.warn(`。
- 再次出现的同样两行：重复发出的警告，不是新增了一个不同问题。之后列表仍成功显示，所以不能把它解释为命令完全失败。

后续列表逐行如下：

```text
# conda environments:
#
base                  *  /root/miniconda3
h3                       /root/miniconda3/envs/h3
```

- `# conda environments:`：输出标题，表示下面是 Conda 环境；这里是显示文本，不是让你执行的命令。
- `#`：分隔行。
- `base ... * ... /root/miniconda3`：环境名 base，星号表示当前激活，路径是其安装位置。
- `h3 ... /root/miniconda3/envs/h3`：另一个已有环境，当前未激活；本项目不直接修改它。

### 6.6 `command -v tmux`

本次没有输出，随后回到提示符，表示 Shell 没有在当前解析范围内找到 `tmux`。准确说是“当前找不到”，不能据此证明整个磁盘绝对不存在该程序。后续需要时安装或配置路径。

`tmux` 用于管理终端会话，可以让远程任务在 SSH 断开后继续运行；前提是服务器和对应进程仍在运行，不能让任务跨越实例关机或释放。

## 7. 误输入与没有输出时如何判断

实际误输入：

```text
q
bash: q: command not found
```

第一行是在 Bash 提示符下输入了 `q`；第二行说明 Bash 尝试寻找名为 q 的命令但没有找到。这次没有执行删除或修改动作。`q` 只在 less 等特定程序内表示退出，不是通用的 Linux 退出键；在 Shell 中退出使用 `exit`，中断前台程序通常使用 `Ctrl+C`。

命令没有输出并不总表示成功或失败。可以在命令之后立即执行 `echo $?` 查询上一条命令的退出状态，通常 0 为成功、非零为失败或其他状态。若中间执行了其他命令，读到的就是其他命令的状态。对于管道，默认通常只得到最后一个命令的状态，因此也要结合日志和实际结果判断。

## 8. 本次检查形成的项目决策

1. 当前无卡模式只有 0.5 核 CPU 时间配额和 2GiB 内存，先用于轻量准备；正式实验前重新检查资源。
2. 项目在数据盘，约剩 35G；系统盘仅剩约 3.1G。安装环境与缓存前先规划路径，不批量下载全部数据。
3. 不改动已有 ComfyUI、fusion_data、base 和 h3；项目单独建立 Python 环境。
4. 用户确认普通关机保留数据，释放实例删除数据。这是用户确认的规则，不是从 `df` 推导出来的。
5. 本地项目维护文档、脚本、配置和最终记录；远程负责执行和验证，日志与结果需回收本地。

对应环境摘要见 [environment-stage0.md](../manifests/environment-stage0.md)。本文用于解释命令，摘要用于记录项目当前环境事实。
