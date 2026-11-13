# AB3DMOT-fork KITTI 输入清单

更新：2026-11-12。

当前本地可见 data/KITTI 下 detection、mini、tracking 等目录；目录存在不证明完整性。Car/0001 检测检查见下文；其他序列覆盖、图像/OXTS/标签帧对齐及标定数值仍未验证。

后续本地盘点：data/KITTI/tracking 实际为普通文本文件，不是数据目录；.work 下目前仅见 dependencies，未准备 datasets。此前提及的 Downloads/data_tracking_image_2.zip 当前不存在。不可依赖这些位置直接运行，先重新核实数据实际存放位置。

运行入口从代码根目录 data/KITTI/detection/pointrcnn_Car_val 读取检测；其他运行数据期望位于 <workspace>/datasets/KITTI/tracking/training。数据准备前核对真实文件和空间，不预设下载包仍然存在，不修改原始输入。

后续清单需包含来源、许可、相对路径、字节数、SHA-256、序列和检查结果。原始 KITTI 下载数据不提交 Git；仓库已有上游输入保留其来源说明。

## 本地 Car/0001 检测检查（2026-11-12）

- 文件：data/KITTI/detection/pointrcnn_Car_val/0001.txt，上游仓库随附 PointRCNN 检测；不是 GT。
- 用户输出：4418×15，帧范围 0–446，类别仅 2，分数范围 -0.8469 至 15.6118；列数、有限值和正尺寸断言通过。
- 助手直接复核并补查：帧号为非负整数，类别均为 Car，二维框 right≥left、bottom≥top；检查通过。
- 442 个帧号含检测；在名义区间 0–446 中，177、178、179、180、441 无检测。此处仅依据检测文件，实际图像帧清单及对齐仍待核实。
- 当前 Windows 文件 480242 字节；原始字节 SHA-256：8263a8cb8dd400a1439ee9c78e91b4adf4ac7eae99cdbf833703662fbedb675d。后续远程需对实际文件单独校验，不推定原始字节一致。

代码映射已静态核查：get_frame_det 取第 7:14 列得到 h,w,l,x,y,z,rotation_y；info 顺序为 alpha,type,left,top,right,bottom,score。process_dets 调用 Box3D.array2bbox_raw，再由 bbox2array 在更新/出生时转为 x,y,z,rotation_y,l,w,h。此转换只重排字段，不执行坐标系变换或底面中心转几何中心。

## 远程 0001 基本数据对齐（2026-11-12，用户执行输出）

数据根：/root/autodl-tmp/kitti-workspace/datasets/KITTI/tracking/training。

- image_02/0001：447 个非空 PNG 文件，文件名完整覆盖 000000.png–000446.png；尚未逐张解码。
- oxts/0001.txt：447×30，有限数值检查通过。
- label_02/0001.txt：4271×17，帧号为 0–446 范围内整数；未修改标签或过滤类别。
- calib/0001.txt：存在非空，1616 字节；原始矩阵与项目解析器输出的一致性待验证。
- 此次结果证明基本文件与帧范围对齐，不代表坐标链路、图像内容、GT 来源或正式评测已经全部验证。

后续用户执行的数值核查通过：独立读取原始 calib/0001.txt，与项目 Calibration 输出逐元素精确比较，P2=(3,4)、R_rect=(3,3)、Tr_velo_cam=(3,4)、Tr_imu_velo=(3,4) 均有限且数值一致。此检查验证解析映射，不等于完整坐标变换链路已通过几何验证。

工作区 training/label_02/0001.txt 与代码 scripts/KITTI/label/0001.txt 经空白分词加载后逐字段完全一致；此处只核对 0001，不外推其他序列。单序列评测的数据前置核查通过，下一步适配评测入口的结果路径和序列选择。
