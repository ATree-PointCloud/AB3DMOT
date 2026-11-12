# KITTI 输入文件清单

依据：用户在 AutoDL 无卡模式下提供的检查输出；记录日期 2026-11-11。
用户从 KITTI tracking 官方页面下载并上传；远程原包目录为项目根目录下 data/downloads。未将原始数据提交本地 Git。

| 文件 | 字节数 | SHA-256 |
|---|---:|---|
| data_tracking_calib.zip | 89829 | 281b8824e82a0710685d0ab641d3f243cffb7af05aebfda550ecfa225742c463 |
| data_tracking_label_2.zip | 2259128 | 6ad1fa0125e3cddcbe4d182e41cd12a854a11b0c733b26c706595f6db5c254e0 |
| data_tracking_oxts.zip | 8352970 | 0b93e47a01d9479b7aeffcad50c0a08566f723119b6dfb7a11da3466acaf02de |

三个 ZIP 的 CRC 检查均返回 None；分别有 52、23、52 个条目。training/calib/0001.txt、training/label_02/0001.txt、training/oxts/0001.txt 均存在。SHA-256 是本项目输入指纹，未与官方发布哈希比对。

远程检测目录覆盖 Car、Pedestrian、Cyclist 的全部 11 个官方验证序列，尚未逐文件校验 schema 和哈希。仓库 tracking 链接指向作者失效路径。mini 仅有稀疏图像和标定，没有 OXTS、标签，不能直接用于连续序列基线。

用户确认训练元数据解压通过：共 63 个文件，远程目标 /root/autodl-tmp/kitti-AB3DMOT/data/KITTI/tracking。calib、label_02、oxts 各有 21 个 txt；序列 0001 对应字节数分别为 1616、598346、192591。未解压 testing 部分。

下一步：准备序列 0001 的完整左目图像；图像尚未下载，尚未开始跟踪或评测。优先本地获取官方图像包，再选择性提取并上传，避免远程同时保存大型原包和全部解压数据。

## 序列 0001 图像子包

本地原包：C:/Users/naihui.zhang/Downloads/data_tracking_image_2.zip，15813146295 字节，19155 个 ZIP 条目。已读取其中 training/image_02/0001/ 下全部 447 个文件，成员读取及 CRC 校验成功；按文件名排序验证帧名完整覆盖 000000.png 至 000446.png。原包其他序列未做 CRC 检查，整个原包 SHA-256 尚未计算。

已在本地创建 data/downloads/kitti_training_image_02_0001.zip，保留 training/image_02/0001/ 结构；370079502 字节，SHA-256 为 8a038370614c5fe44cefccaa398972a42e6d1dae8aa408c8bdc561a4671e80a2。图像未重新编码，子包仅重新组织 ZIP 容器。data/ 已由 .gitignore 排除。远程上传与解压待验证。

用户后续确认远程文件为 370079502 字节，SHA-256 与本地子包完全一致，上传验证通过。此前 66MiB 的中间检查不作为最终输入版本；远程解压与帧对齐检查待执行。

用户后续确认序列 0001 解压及基本对齐检查通过：447 张图像，文件名 000000.png 至 000446.png；OXTS 非空行 447；标签帧号范围 0 至 446 且未越界；标定存在非空。完整内容/坐标验证及检测 schema 检查仍待执行。

用户确认 Car/0001 检测 schema 检查通过：4418×15；帧范围 0–446，442 帧有检测；分数范围 -0.8469 至 15.6118；SHA-256 a64353d4f9da8911fb18891c6f343f26b8d7fea3e47a5c429b201f982fd883bf。

代码复核：main_per_cat 会将 get_subfolder_seq 返回的数据根追加 tracking，然后交给 initialize。因此仅添加上游 data/KITTI/training 链接不足以解决实际入口路径。尚未运行跟踪；下一步先阅读调用链并确定路径适配方式。

指导约定：用户要求不得自动创建脚本后让其直接上传运行。每一步先解释要做什么及原因，再指导用户逐步编写。本地编辑、远程验证的具体步骤需清楚区分。此前自动创建的冒烟脚本已按用户要求撤回。
