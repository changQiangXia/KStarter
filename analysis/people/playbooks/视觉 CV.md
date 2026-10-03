# 视觉 CV：前 50 选手决策增量（P3）

> 来源：`people/claims/gm_claims.csv` 中该领域的 106 条断言，按受控标签聚合；每条断言可经 `scripts/people/verify_claims.py` 回链原文。
> 系统方法论见 `playbook/cv.md`；本页只保留有跨人/跨队复现证据的决策项。

## 损失设计（证据单位 17）

- **条件**：相对位置编码参数多、训练与推理开销大  
- **动作**：用 Llama rotary embedding 替换相对位置编码；旋转嵌入缓存一次并在各层共享  
- **机制**：减少每层重复参数与计算，为更深模型腾出空间  
- **结果**：训练约 2X 加速、tf-lite 推理约 3X 加速；参数量减少 20%  
- **证据**：[asl-fingerspelling#434485-02](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)（@christofhenkel｜A）
- 其他案例：[@christofhenkel](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)、[@christofhenkel](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)、[@christofhenkel](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)、[@christofhenkel](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)

## 提交/推理工程（证据单位 17）

- **条件**：图像回归、训练集小（9912 张）；可用大量 ImageNet-1k 预训练模型；提交时限 9 小时  
- **动作**：用预训练模型做特征提取把图像回归转成表格回归：取 ImageNet-1k 线性头输出（优于内部 embedding 层）；cuML SVR 加前向爬山多起点选特征集合；最终三组 SVR 特征集合与 5 个图像模型加权融合  
- **机制**：1k 类含猫狗品种故线性头特征更贴合；RAPIDS SVR 让数千次 SVR 折可行；多特征集合提供多样性  
- **结果**：单组 SVR 的 CV 16.997 到 17.148；最终 CV 16.81、public LB 17.72、private LB 16.82（private top10，金区）  
- **证据**：[petfinder-pawpularity-score#301686-01](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301686)（@titericz｜A）
- 其他案例：[@christofhenkel](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)、[@christofhenkel](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)、[@harshitsheoran](https://www.kaggle.com/competitions/waveform-inversion/discussion/587388)、[@cdeotte](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301015)

## 目标编码/类别特征（证据单位 16）

- **条件**：图像回归、训练集小（9912 张）；可用大量 ImageNet-1k 预训练模型；提交时限 9 小时  
- **动作**：用预训练模型做特征提取把图像回归转成表格回归：取 ImageNet-1k 线性头输出（优于内部 embedding 层）；cuML SVR 加前向爬山多起点选特征集合；最终三组 SVR 特征集合与 5 个图像模型加权融合  
- **机制**：1k 类含猫狗品种故线性头特征更贴合；RAPIDS SVR 让数千次 SVR 折可行；多特征集合提供多样性  
- **结果**：单组 SVR 的 CV 16.997 到 17.148；最终 CV 16.81、public LB 17.72、private LB 16.82（private top10，金区）  
- **证据**：[petfinder-pawpularity-score#301686-01](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301686)（@titericz｜A）
- 其他案例：[@christofhenkel](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)、[@christofhenkel](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)、[@harshitsheoran](https://www.kaggle.com/competitions/waveform-inversion/discussion/587388)、[@harshitsheoran](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/340612)

## 验证设计（证据单位 15）

- **条件**：图像回归、训练集小（9912 张）；可用大量 ImageNet-1k 预训练模型；提交时限 9 小时  
- **动作**：用预训练模型做特征提取把图像回归转成表格回归：取 ImageNet-1k 线性头输出（优于内部 embedding 层）；cuML SVR 加前向爬山多起点选特征集合；最终三组 SVR 特征集合与 5 个图像模型加权融合  
- **机制**：1k 类含猫狗品种故线性头特征更贴合；RAPIDS SVR 让数千次 SVR 折可行；多特征集合提供多样性  
- **结果**：单组 SVR 的 CV 16.997 到 17.148；最终 CV 16.81、public LB 17.72、private LB 16.82（private top10，金区）  
- **证据**：[petfinder-pawpularity-score#301686-01](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301686)（@titericz｜A）
- 其他案例：[@harshitsheoran](https://www.kaggle.com/competitions/waveform-inversion/discussion/587388)、[@cdeotte](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301015)、[@yiheng](https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/325646)、[@yiheng](https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/325646)

## 集成/融合（证据单位 14）

- **条件**：图像回归、训练集小（9912 张）；可用大量 ImageNet-1k 预训练模型；提交时限 9 小时  
- **动作**：用预训练模型做特征提取把图像回归转成表格回归：取 ImageNet-1k 线性头输出（优于内部 embedding 层）；cuML SVR 加前向爬山多起点选特征集合；最终三组 SVR 特征集合与 5 个图像模型加权融合  
- **机制**：1k 类含猫狗品种故线性头特征更贴合；RAPIDS SVR 让数千次 SVR 折可行；多特征集合提供多样性  
- **结果**：单组 SVR 的 CV 16.997 到 17.148；最终 CV 16.81、public LB 17.72、private LB 16.82（private top10，金区）  
- **证据**：[petfinder-pawpularity-score#301686-01](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301686)（@titericz｜A）
- 其他案例：[@harshitsheoran](https://www.kaggle.com/competitions/waveform-inversion/discussion/587388)、[@cdeotte](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301015)、[@cdeotte](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301015)、[@yiheng](https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/325646)

## 后处理/校准（证据单位 13）

- **条件**：损坏或极短输入会产生垃圾预测  
- **动作**：额外预测 confidence（目标为历史 OOF 预测的归一化 Levenshtein 距离）；confidence<0.15 或序列<15 帧时替换为 dummy phrase '2 a-e -aroe'  
- **机制**：dummy phrase 与训练/测试分布 Levenshtein 距离小，替换垃圾预测可降损失  
- **结果**：消融增益 +0.006；阈值 confidence 0.15、序列 15 帧  
- **证据**：[asl-fingerspelling#434485-04](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)（@christofhenkel｜A）
- 其他案例：[@brendanartley](https://www.kaggle.com/competitions/byu-locating-bacterial-flagellar-motors-2025/discussion/583143)、[@brendanartley](https://www.kaggle.com/competitions/byu-locating-bacterial-flagellar-motors-2025/discussion/583143)、[@brendanartley](https://www.kaggle.com/competitions/byu-locating-bacterial-flagellar-motors-2025/discussion/583143)、[@philippsinger](https://www.kaggle.com/competitions/dfl-bundesliga-data-shootout/discussion/359932)

## CNN/视觉架构（证据单位 12）

- **条件**：输入 350x350；空间不对齐使 Unet skip 无意义  
- **动作**：用无解码器 ViT 直接回归；对比 EVA02 与 ViT 后定位到 RoPE 是主要增益来源；最终 backbone 为 vit_small_patch14_reg4_dinov2  
- **机制**：RoPE 贡献主要性能差异；encoder+decoder 重复无提升且过拟合  
- **结果**：ViT+RoPE 降到 26 MAE 以下（原文）  
- **证据**：[waveform-inversion#587388-02](https://www.kaggle.com/competitions/waveform-inversion/discussion/587388)（@harshitsheoran｜A）
- 其他案例：[@cdeotte](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301015)、[@philippsinger](https://www.kaggle.com/competitions/dfl-bundesliga-data-shootout/discussion/359932)、[@christofhenkel](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561510)、[@tascj0](https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/429060)

## 集成权重选择（证据单位 12）

- **条件**：需要 tf-lite fp16 推理，且模型文件受 40MB 限制  
- **动作**：用 mixed precision 训练（cosine 400 epochs、peak LR 0.0045、weight decay 0.08、10 epochs warmup、effective batch 512），并以 fp16 导出 tf-lite  
- **机制**：训练与推理精度一致，避免 fp32 训练到 fp16 推理的性能掉点  
- **结果**：fp32 训练 + fp16 推理会掉约 0.01 CV vs LB；最终两个 seed 的 tf-lite 文件 39988kb（限额 40MB）  
- **证据**：[asl-fingerspelling#434485-05](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)（@christofhenkel｜A）
- 其他案例：[@cdeotte](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301015)、[@brendanartley](https://www.kaggle.com/competitions/byu-locating-bacterial-flagellar-motors-2025/discussion/583143)、[@philippsinger](https://www.kaggle.com/competitions/tensorflow-great-barrier-reef/discussion/307707)、[@philippsinger](https://www.kaggle.com/competitions/tensorflow-great-barrier-reef/discussion/307707)

## 规模/Scaling（证据单位 11）

- **条件**：相对位置编码参数多、训练与推理开销大  
- **动作**：用 Llama rotary embedding 替换相对位置编码；旋转嵌入缓存一次并在各层共享  
- **机制**：减少每层重复参数与计算，为更深模型腾出空间  
- **结果**：训练约 2X 加速、tf-lite 推理约 3X 加速；参数量减少 20%  
- **证据**：[asl-fingerspelling#434485-02](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)（@christofhenkel｜A）
- 其他案例：[@harshitsheoran](https://www.kaggle.com/competitions/waveform-inversion/discussion/587388)、[@philippsinger](https://www.kaggle.com/competitions/dfl-bundesliga-data-shootout/discussion/359932)、[@cnumber](https://www.kaggle.com/competitions/drawing-with-llms/discussion/581024)、[@christofhenkel](https://www.kaggle.com/competitions/rsna-breast-cancer-detection/discussion/391208)

## 数据增广（证据单位 10）

- **条件**：训练签名者有限，需要泛化到新签名者并支撑深层模型  
- **动作**：组合增广：时间缩放/平移、左右翻转、同签名者内 CutMix、手指/面部/姿态 dropout、时间与空间 masking；多数增广作用 50% 样本，resize/affine 约 80%  
- **机制**：增广抑制过拟合并创造容纳深层模型的训练空间  
- **结果**：粗消融增益：CutMix +0.005、FingerDropout +0.005、Face/PoseDropout +0.005、decoder input masking +0.003  
- **证据**：[asl-fingerspelling#434485-03](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)（@christofhenkel｜A）
- 其他案例：[@christofhenkel](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)、[@harshitsheoran](https://www.kaggle.com/competitions/waveform-inversion/discussion/587388)、[@cdeotte](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301015)、[@cdeotte](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301015)

## dtype/内存优化（证据单位 10）

- **条件**：损坏或极短输入会产生垃圾预测  
- **动作**：额外预测 confidence（目标为历史 OOF 预测的归一化 Levenshtein 距离）；confidence<0.15 或序列<15 帧时替换为 dummy phrase '2 a-e -aroe'  
- **机制**：dummy phrase 与训练/测试分布 Levenshtein 距离小，替换垃圾预测可降损失  
- **结果**：消融增益 +0.006；阈值 confidence 0.15、序列 15 帧  
- **证据**：[asl-fingerspelling#434485-04](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)（@christofhenkel｜A）
- 其他案例：[@brendanartley](https://www.kaggle.com/competitions/byu-locating-bacterial-flagellar-motors-2025/discussion/569921)、[@brendanartley](https://www.kaggle.com/competitions/byu-locating-bacterial-flagellar-motors-2025/discussion/583143)、[@philippsinger](https://www.kaggle.com/competitions/dfl-bundesliga-data-shootout/discussion/359932)、[@cnumber](https://www.kaggle.com/competitions/drawing-with-llms/discussion/581024)

## 信号/频谱处理（证据单位 9）

- **条件**：相对位置编码参数多、训练与推理开销大  
- **动作**：用 Llama rotary embedding 替换相对位置编码；旋转嵌入缓存一次并在各层共享  
- **机制**：减少每层重复参数与计算，为更深模型腾出空间  
- **结果**：训练约 2X 加速、tf-lite 推理约 3X 加速；参数量减少 20%  
- **证据**：[asl-fingerspelling#434485-02](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)（@christofhenkel｜A）
- 其他案例：[@christofhenkel](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)、[@christofhenkel](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)、[@christofhenkel](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)、[@christofhenkel](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)

## 类别不平衡（证据单位 9）

- **条件**：完整滑窗太慢，限制 TTA 次数与 overlap  
- **动作**：匹配 patch 高宽、只沿深度滑窗：快 4 倍；用高 overlap 0.875 与更多 TTA；边缘预测用 roi_weight_map 降权（中间 40% 权重 1.0，其余 0.001）  
- **机制**：减少重复计算换取更多 TTA 与更平滑的窗口聚合  
- **结果**：快 4 倍；overlap 0.875；权重 1.0 与 0.001；中间 40%  
- **证据**：[byu-locating-bacterial-flagellar-motors-2025#583143-04](https://www.kaggle.com/competitions/byu-locating-bacterial-flagellar-motors-2025/discussion/583143)（@brendanartley｜A）
- 其他案例：[@christofhenkel](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561510)、[@christofhenkel](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561510)、[@ren4yu](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744484)、[@ren4yu](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744484)

## 预训练/域适应（证据单位 8）

- **条件**：图像回归、训练集小（9912 张）；可用大量 ImageNet-1k 预训练模型；提交时限 9 小时  
- **动作**：用预训练模型做特征提取把图像回归转成表格回归：取 ImageNet-1k 线性头输出（优于内部 embedding 层）；cuML SVR 加前向爬山多起点选特征集合；最终三组 SVR 特征集合与 5 个图像模型加权融合  
- **机制**：1k 类含猫狗品种故线性头特征更贴合；RAPIDS SVR 让数千次 SVR 折可行；多特征集合提供多样性  
- **结果**：单组 SVR 的 CV 16.997 到 17.148；最终 CV 16.81、public LB 17.72、private LB 16.82（private top10，金区）  
- **证据**：[petfinder-pawpularity-score#301686-01](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301686)（@titericz｜A）
- 其他案例：[@harshitsheoran](https://www.kaggle.com/competitions/waveform-inversion/discussion/587388)、[@cdeotte](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301015)、[@yiheng](https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/325646)、[@tatamikenn](https://www.kaggle.com/competitions/drawing-with-llms/discussion/565396)

## 混合精度/量化（证据单位 7）

- **条件**：需要 tf-lite fp16 推理，且模型文件受 40MB 限制  
- **动作**：用 mixed precision 训练（cosine 400 epochs、peak LR 0.0045、weight decay 0.08、10 epochs warmup、effective batch 512），并以 fp16 导出 tf-lite  
- **机制**：训练与推理精度一致，避免 fp32 训练到 fp16 推理的性能掉点  
- **结果**：fp32 训练 + fp16 推理会掉约 0.01 CV vs LB；最终两个 seed 的 tf-lite 文件 39988kb（限额 40MB）  
- **证据**：[asl-fingerspelling#434485-05](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)（@christofhenkel｜A）
- 其他案例：[@christofhenkel](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)、[@brendanartley](https://www.kaggle.com/competitions/byu-locating-bacterial-flagellar-motors-2025/discussion/583143)、[@christofhenkel](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561510)、[@ren4yu](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744484)

## 泄漏检测/探针（证据单位 7）

- **条件**：相对位置编码参数多、训练与推理开销大  
- **动作**：用 Llama rotary embedding 替换相对位置编码；旋转嵌入缓存一次并在各层共享  
- **机制**：减少每层重复参数与计算，为更深模型腾出空间  
- **结果**：训练约 2X 加速、tf-lite 推理约 3X 加速；参数量减少 20%  
- **证据**：[asl-fingerspelling#434485-02](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)（@christofhenkel｜A）
- 其他案例：[@christofhenkel](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)、[@harshitsheoran](https://www.kaggle.com/competitions/waveform-inversion/discussion/587388)、[@cdeotte](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301015)、[@brendanartley](https://www.kaggle.com/competitions/byu-locating-bacterial-flagellar-motors-2025/discussion/583143)

## 学习率调度（证据单位 7）

- **条件**：需要 tf-lite fp16 推理，且模型文件受 40MB 限制  
- **动作**：用 mixed precision 训练（cosine 400 epochs、peak LR 0.0045、weight decay 0.08、10 epochs warmup、effective batch 512），并以 fp16 导出 tf-lite  
- **机制**：训练与推理精度一致，避免 fp32 训练到 fp16 推理的性能掉点  
- **结果**：fp32 训练 + fp16 推理会掉约 0.01 CV vs LB；最终两个 seed 的 tf-lite 文件 39988kb（限额 40MB）  
- **证据**：[asl-fingerspelling#434485-05](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)（@christofhenkel｜A）
- 其他案例：[@yiheng](https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/325646)、[@christofhenkel](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561510)、[@cnumber](https://www.kaggle.com/competitions/drawing-with-llms/discussion/581024)、[@tascj0](https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/429060)

## 检索/RAG（证据单位 7）

- **条件**：需要 tf-lite fp16 推理，且模型文件受 40MB 限制  
- **动作**：用 mixed precision 训练（cosine 400 epochs、peak LR 0.0045、weight decay 0.08、10 epochs warmup、effective batch 512），并以 fp16 导出 tf-lite  
- **机制**：训练与推理精度一致，避免 fp32 训练到 fp16 推理的性能掉点  
- **结果**：fp32 训练 + fp16 推理会掉约 0.01 CV vs LB；最终两个 seed 的 tf-lite 文件 39988kb（限额 40MB）  
- **证据**：[asl-fingerspelling#434485-05](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)（@christofhenkel｜A）
- 其他案例：[@christofhenkel](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561510)、[@cnumber](https://www.kaggle.com/competitions/drawing-with-llms/discussion/581024)、[@tatamikenn](https://www.kaggle.com/competitions/drawing-with-llms/discussion/565396)、[@tatamikenn](https://www.kaggle.com/competitions/drawing-with-llms/discussion/565396)

## 合成/生成数据（证据单位 6）

- **条件**：文本生成受约束的 SVG（大小与内容限制）  
- **动作**：FLUX.1-schnell 按 4 个 prompt 模板各生成 2 张位图（共 8 候选）→ vtracer 转 SVG（二分搜索 PNG 分辨率满足大小限制）→ SigLIP 选 top2 → pydiffvg 短优化 10 次选优 → 主优化 200 次  
- **机制**：先用生成模型拿高质量位图，再把问题转成可微矢量参数优化  
- **结果**：8 候选位图；短优化 10 次；主优化 200 次  
- **证据**：[drawing-with-llms#581024-01](https://www.kaggle.com/competitions/drawing-with-llms/discussion/581024)（@cnumber｜A）
- 其他案例：[@ren4yu](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744484)、[@christofhenkel](https://www.kaggle.com/competitions/rsna-breast-cancer-detection/discussion/391208)、[@conjuring92](https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418430)、[@conjuring92](https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418430)

## 伪标签/自训练（证据单位 6）

- **条件**：真实速度模型数量有限  
- **动作**：用 FiveCrop/5xRandomAffine 在已有速度模型上生成 10 倍数据（4.7M seismic 样本）做预训练；迭代伪标签：每 epoch 预测验证与测试约 95k 样本，forward modeling 后加入下一轮训练，共 570 epochs  
- **机制**：增广扩充上游数据；迭代伪标签把测试分布逐步注入训练  
- **结果**：10x 数据、4.7M 样本；每轮约 95k 伪标签；共 570 epochs  
- **证据**：[waveform-inversion#587388-03](https://www.kaggle.com/competitions/waveform-inversion/discussion/587388)（@harshitsheoran｜A）
- 其他案例：[@tascj0](https://www.kaggle.com/competitions/google-research-identify-contrails-reduce-global-warming/discussion/430479)、[@sersasj](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744801)、[@cdeotte](https://www.kaggle.com/competitions/happy-whale-and-dolphin/discussion/320298)、[@conjuring92](https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418430)

## 分组聚合特征（证据单位 6）

- **条件**：完整滑窗太慢，限制 TTA 次数与 overlap  
- **动作**：匹配 patch 高宽、只沿深度滑窗：快 4 倍；用高 overlap 0.875 与更多 TTA；边缘预测用 roi_weight_map 降权（中间 40% 权重 1.0，其余 0.001）  
- **机制**：减少重复计算换取更多 TTA 与更平滑的窗口聚合  
- **结果**：快 4 倍；overlap 0.875；权重 1.0 与 0.001；中间 40%  
- **证据**：[byu-locating-bacterial-flagellar-motors-2025#583143-04](https://www.kaggle.com/competitions/byu-locating-bacterial-flagellar-motors-2025/discussion/583143)（@brendanartley｜A）
- 其他案例：[@philippsinger](https://www.kaggle.com/competitions/dfl-bundesliga-data-shootout/discussion/359932)、[@ren4yu](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744484)、[@ren4yu](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561401)、[@darraghdog](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/362643)

## TTA（证据单位 5）

- **条件**：训练签名者有限，需要泛化到新签名者并支撑深层模型  
- **动作**：组合增广：时间缩放/平移、左右翻转、同签名者内 CutMix、手指/面部/姿态 dropout、时间与空间 masking；多数增广作用 50% 样本，resize/affine 约 80%  
- **机制**：增广抑制过拟合并创造容纳深层模型的训练空间  
- **结果**：粗消融增益：CutMix +0.005、FingerDropout +0.005、Face/PoseDropout +0.005、decoder input masking +0.003  
- **证据**：[asl-fingerspelling#434485-03](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)（@christofhenkel｜A）
- 其他案例：[@harshitsheoran](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/340612)、[@harshitsheoran](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/340612)、[@christofhenkel](https://www.kaggle.com/competitions/rsna-breast-cancer-detection/discussion/391208)、[@tascj0](https://www.kaggle.com/competitions/google-research-identify-contrails-reduce-global-warming/discussion/430479)

## Transformer/注意力（证据单位 5）

- **条件**：相对位置编码参数多、训练与推理开销大  
- **动作**：用 Llama rotary embedding 替换相对位置编码；旋转嵌入缓存一次并在各层共享  
- **机制**：减少每层重复参数与计算，为更深模型腾出空间  
- **结果**：训练约 2X 加速、tf-lite 推理约 3X 加速；参数量减少 20%  
- **证据**：[asl-fingerspelling#434485-02](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)（@christofhenkel｜A）
- 其他案例：[@christofhenkel](https://www.kaggle.com/competitions/rsna-breast-cancer-detection/discussion/391208)、[@sersasj](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744801)、[@sersasj](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744801)、[@ren4yu](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561401)

## 数据清洗/去噪（证据单位 5）

- **条件**：公开榜与私有榜不一致（小数据、榜单噪声）  
- **动作**：最终两个提交分别选 best LB（CV 17.15 / LB 17.64）与 best CV（CV 16.98 / LB 17.78）；best CV 提交的 public rank 只有 120，但 private 第 6  
- **机制**：当 CV 可靠时以 CV 选模，敢于放弃公开榜更好看的提交  
- **结果**：CV 16.98 / public 17.78 / private 16.90（第 6）  
- **证据**：[petfinder-pawpularity-score#301015-01](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301015)（@cdeotte｜A）
- 其他案例：[@ren4yu](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561401)、[@conjuring92](https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418430)、[@conjuring92](https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418430)、[@tascj0](https://www.kaggle.com/competitions/waveform-inversion/discussion/587419)

## 度量学习/ArcFace（证据单位 5）

- **条件**：图像回归、训练集小（9912 张）；可用大量 ImageNet-1k 预训练模型；提交时限 9 小时  
- **动作**：用预训练模型做特征提取把图像回归转成表格回归：取 ImageNet-1k 线性头输出（优于内部 embedding 层）；cuML SVR 加前向爬山多起点选特征集合；最终三组 SVR 特征集合与 5 个图像模型加权融合  
- **机制**：1k 类含猫狗品种故线性头特征更贴合；RAPIDS SVR 让数千次 SVR 折可行；多特征集合提供多样性  
- **结果**：单组 SVR 的 CV 16.997 到 17.148；最终 CV 16.81、public LB 17.72、private LB 16.82（private top10，金区）  
- **证据**：[petfinder-pawpularity-score#301686-01](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301686)（@titericz｜A）
- 其他案例：[@christofhenkel](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)、[@cdeotte](https://www.kaggle.com/competitions/happy-whale-and-dolphin/discussion/320298)、[@tascj0](https://www.kaggle.com/competitions/waveform-inversion/discussion/587419)

## 多种子平均（证据单位 4）

- **条件**：需要 tf-lite fp16 推理，且模型文件受 40MB 限制  
- **动作**：用 mixed precision 训练（cosine 400 epochs、peak LR 0.0045、weight decay 0.08、10 epochs warmup、effective batch 512），并以 fp16 导出 tf-lite  
- **机制**：训练与推理精度一致，避免 fp32 训练到 fp16 推理的性能掉点  
- **结果**：fp32 训练 + fp16 推理会掉约 0.01 CV vs LB；最终两个 seed 的 tf-lite 文件 39988kb（限额 40MB）  
- **证据**：[asl-fingerspelling#434485-05](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)（@christofhenkel｜A）
- 其他案例：[@cnumber](https://www.kaggle.com/competitions/drawing-with-llms/discussion/581024)、[@christofhenkel](https://www.kaggle.com/competitions/rsna-breast-cancer-detection/discussion/391208)、[@tascj0](https://www.kaggle.com/competitions/waveform-inversion/discussion/587419)

## 缺失值/NAN（证据单位 4）

- **条件**：dataset2 标注带噪（膨胀）、dataset3 无标注  
- **动作**：dataset1 5 折训 Mask R-CNN（Swin Transformer backbone 加 HTC RoI head）；用其给 dataset2、3 生成伪标签（每折）；再用 dataset1 加 2 加 3 训 5 折；dataset2 同时用原始（膨胀）标注与伪标签  
- **机制**：伪标签补足缺失标注，并让带噪数据两种口径并存  
- **结果**：5 折；3 个数据集  
- **证据**：[hubmap-hacking-the-human-vasculature#428295-01](https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/428295)（@ren4yu｜A）
- 其他案例：[@christofhenkel](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)、[@tascj0](https://www.kaggle.com/competitions/waveform-inversion/discussion/587419)

## Agent/LLM 工具（证据单位 3）

- **条件**：文本生成受约束的 SVG（大小与内容限制）  
- **动作**：FLUX.1-schnell 按 4 个 prompt 模板各生成 2 张位图（共 8 候选）→ vtracer 转 SVG（二分搜索 PNG 分辨率满足大小限制）→ SigLIP 选 top2 → pydiffvg 短优化 10 次选优 → 主优化 200 次  
- **机制**：先用生成模型拿高质量位图，再把问题转成可微矢量参数优化  
- **结果**：8 候选位图；短优化 10 次；主优化 200 次  
- **证据**：[drawing-with-llms#581024-01](https://www.kaggle.com/competitions/drawing-with-llms/discussion/581024)（@cnumber｜A）
- 其他案例：[@cnumber](https://www.kaggle.com/competitions/drawing-with-llms/discussion/581024)、[@conjuring92](https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418430)、[@darraghdog](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/362643)、[@darraghdog](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/362643)

## 外部数据（证据单位 3）

- **条件**：尝试用去年比赛数据提升  
- **动作**：自己用去年数据预训练或推理都无收益；但 top 方案用去年重复图（约 33% 图像）拼接去年 meta 特征有效  
- **机制**：去年 meta 比今年 meta 更强；需要先找重复图再拼特征，直接预训练无效  
- **结果**：去年重复图约占 33%  
- **证据**：[petfinder-pawpularity-score#301015-05](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301015)（@cdeotte｜A）
- 其他案例：[@christofhenkel](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485)、[@cdeotte](https://www.kaggle.com/competitions/asl-signs/discussion/406302)、[@ren4yu](https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/428295)

## 特征选择（证据单位 2）

- **条件**：图像回归、训练集小（9912 张）；可用大量 ImageNet-1k 预训练模型；提交时限 9 小时  
- **动作**：用预训练模型做特征提取把图像回归转成表格回归：取 ImageNet-1k 线性头输出（优于内部 embedding 层）；cuML SVR 加前向爬山多起点选特征集合；最终三组 SVR 特征集合与 5 个图像模型加权融合  
- **机制**：1k 类含猫狗品种故线性头特征更贴合；RAPIDS SVR 让数千次 SVR 折可行；多特征集合提供多样性  
- **结果**：单组 SVR 的 CV 16.997 到 17.148；最终 CV 16.81、public LB 17.72、private LB 16.82（private top10，金区）  
- **证据**：[petfinder-pawpularity-score#301686-01](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301686)（@titericz｜A）
- 其他案例：[@tascj0](https://www.kaggle.com/competitions/waveform-inversion/discussion/587419)

## 公开榜策略（证据单位 2）

- **条件**：公开榜与私有榜不一致（小数据、榜单噪声）  
- **动作**：最终两个提交分别选 best LB（CV 17.15 / LB 17.64）与 best CV（CV 16.98 / LB 17.78）；best CV 提交的 public rank 只有 120，但 private 第 6  
- **机制**：当 CV 可靠时以 CV 选模，敢于放弃公开榜更好看的提交  
- **结果**：CV 16.98 / public 17.78 / private 16.90（第 6）  
- **证据**：[petfinder-pawpularity-score#301015-01](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301015)（@cdeotte｜A）
- 其他案例：[@philippsinger](https://www.kaggle.com/competitions/dfl-bundesliga-data-shootout/discussion/359932)

## 时间/分组切分（证据单位 2）

- **条件**：完整滑窗太慢，限制 TTA 次数与 overlap  
- **动作**：匹配 patch 高宽、只沿深度滑窗：快 4 倍；用高 overlap 0.875 与更多 TTA；边缘预测用 roi_weight_map 降权（中间 40% 权重 1.0，其余 0.001）  
- **机制**：减少重复计算换取更多 TTA 与更平滑的窗口聚合  
- **结果**：快 4 倍；overlap 0.875；权重 1.0 与 0.001；中间 40%  
- **证据**：[byu-locating-bacterial-flagellar-motors-2025#583143-04](https://www.kaggle.com/competitions/byu-locating-bacterial-flagellar-motors-2025/discussion/583143)（@brendanartley｜A）
- 其他案例：[@christofhenkel](https://www.kaggle.com/competitions/waveform-inversion/discussion/587498)

## 长序列/上下文（证据单位 2）

- **条件**：需要复用尽量多模型  
- **动作**：统一预处理与缩放：DICOM windowing、线性 window 加速、min-filter CNN 粗裁乳房区域、PIL lanczos 缩放优于 cv2、统一缩到 1152、保留比例 padding 成方形  
- **机制**：统一输入尺寸与预处理让不同 backbone 的权重与代码可复用  
- **结果**：缩放目标 1152  
- **证据**：[rsna-breast-cancer-detection#391208-01](https://www.kaggle.com/competitions/rsna-breast-cancer-detection/discussion/391208)（@christofhenkel｜A）
- 其他案例：[@conjuring92](https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418430)

## 贝叶斯/概率模型（证据单位 2）

- **条件**：小图增广会丢信息  
- **动作**：增广在缩放前做：vflip、hflip、transpose、shift、scale、rotate、grid distortion、affine；缩放后只做 grid shuffle 或 coarse dropout；训练随机裁 1024、验证中心裁  
- **机制**：在原始分辨率上做几何增广避免插值损失  
- **结果**：训练裁 1024  
- **证据**：[rsna-breast-cancer-detection#391208-02](https://www.kaggle.com/competitions/rsna-breast-cancer-detection/discussion/391208)（@christofhenkel｜A）
- 其他案例：[@cdeotte](https://www.kaggle.com/competitions/happy-whale-and-dolphin/discussion/320298)

