# fathomnet-out-of-sample-detection

- 类别：Research ｜ 主题：cv ｜ 子类：— ｜ 领域：—
- 截止：2023-05-23 ｜ 队伍数：69 ｜ 机制：标准赛
- 评估指标：FathomNet 2023
- 讨论区：29 条主题

## 讨论区索引（按票数排序）

- 19 票 / 2 评论 | Similar competitions in the past 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/397024
- 9 票 / 3 评论 | New to Kaggle or Machine Learning? Check this out ~ 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/397069
- 6 票 / 2 评论 | Incorrect labels from the dataset 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/407400
- 5 票 / 4 评论 | Looking for a Team Megathread 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/397070
- 5 票 / 0 评论 | 4th place solution 「write-up」
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/413092
- 3 票 / 0 评论 | Metric Fix and Rescore 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/404769
- 3 票 / 2 评论 | question about Submission 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/400616
- 3 票 / 0 评论 | Semi-supervised Visual Tracking of Marine Animals Using Autonomous Underwater Vehicles 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/397881
- 2 票 / 2 评论 | Inconsistent submission score with MAP@20 and scoring code 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/410140
- 2 票 / 0 评论 | FGVC10 Workshop at CVPR - Other competitions 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/401210
- 2 票 / 1 评论 | 157 out of 290 categories have no corresponding images 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/398752
- 2 票 / 0 评论 | Handling Label Noise  
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/398487
- 2 票 / 10 评论 | Trying download_images.py code returned "unrecognized arguments" 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/397071
- 1 票 / 1 评论 | What is OSD (Out-of-Sample Detection)? 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/411135
- 1 票 / 6 评论 | Downloading images from source is too long 😥 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/410908
- 1 票 / 3 评论 | What is the correct submission format? 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/410430
- 1 票 / 1 评论 | Submission contains null values 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/406510
- 1 票 / 7 评论 | Inconsistent behavior in leaderboard evaluation metric 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/401858
- 1 票 / 2 评论 | Evaluation metric raised an unexpected error 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/398368
- 1 票 / 2 评论 | Annotation issue 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/397530
- 0 票 / 0 评论 | Wondering the rule about dataset has been changed? 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/411911
- 0 票 / 2 评论 | Clarification on rules for using additional dataset 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/407096
- 0 票 / 0 评论 | External Dataset: Okeanos Animal Guide 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/407254
- 0 票 / 2 评论 | Command line hang when running conda activate fgvc_test 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/402836
- 0 票 / 2 评论 | Question about sample_submission.csv 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/403062
- 0 票 / 1 评论 | Conflict between CVPR2023 submission time and competition time 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/400854
- 0 票 / 2 评论 | Error while trying to get start 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/399727
- 0 票 / 1 评论 | My errors -  
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/399632
- 0 票 / 1 评论 | Is there any metal in this competition? like normal competitions? 
  https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/397675

## write-up 正文（6 篇）

### 4th place solution

来源：https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/413092

Thanks organizers of this research competition. Here, I would like to tell about my 4th place solution.

Code on github: https://github.com/artem-istranin/FathomNet23

TLDL

My solution is based on training an ensemble of categories classification models with labels smoothing. Then OSD score for each model in ensemble is obtained as 1 - max(probabilities of all categories) and the final OSD score is estimated as average of these OSD scores + 5 average standard deviations of all category predictions.

Preprocessing

The data is very unbalanced and some categories only have few (often only 1) images. My approach is to consider all categories with less than 10 images as unknowns (zero class) so that at the end there are only the following classes left in training/validation datasets:

[图 1: inbox%2F1728433%2F8a5e41bdd312789f22a6cf019fceab31%2Fcategories_distr_after_preprocessing.png]

Training

I'm using EfficientNetV2B0 architecture pretrained on imagenet accomplished with 128 units Dense layer following by the output layer for category probabilities. Initialization of the output layer is done based on positive/negative class imbalance to make convergence on model faster. I'm fine tuning base model in classical manner by 2 stages: optimization of top layers with frozen base model layers and then training incl. 2 top layers of base model.

Due to known problem of the noisy labels, training with labels smoothing 0.1 was giving the best results.

Submission

My final submission is an ensemble of 6 different models all following the same training strategy. Finally, the logic on top of predictions from models is the following:

To predict categories, I first average scores over all models and consider only the categories with probability higher than threshold 0.4.

To predict OSD score, I first estimate OSD for each single model as 1 - max(probabilities of all categories) and consider average of these OSD scores + 5 average standard deviations of all category predictions for final OSD score.

[图 2: inbox%2F1728433%2Ff6f58bb3d8fd1d2f084797264e22344c%2F20230523_190837_models_ensemble_osd_scores.png]

---

### New to Kaggle or Machine Learning? Check this out ~

来源：https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/397069

New to machine learning and data science? No question is too basic or too simple. Feel free to start your own thread, or use this thread as a place to post any first-timer clarifying questions for the Kaggle community to help you with!

If you would consider yourself a beginner but don't know where to get started, let other Kagglers help you take your first steps here!

New to Kaggle? Take a look at a few videos Dr. Rachael Tatman has put together to learn a bit more about site etiquette, or Kaggle lingo.

Remember: Kaggle is for everyone. Whether you're teaming up or sharing tips in the competition forum, we expect everyone to follow our Kaggle community guidelines.

A tip on sharing content - Kaggle is a collaborative community, whereby sharing techniques, starter notebooks, and ideas in the discussion forums are highly encouraged throughout the competition. However, as the competition draws closer to the final deadline it's customary to keep high-scoring notebooks withheld until after the competition has concluded. This maintains the spirit of the competition, while also allowing individuals to submit their own creative work without jeopardy of a higher-scoring notebook being available for an automatic higher rank (through copy/submit). We disable publishing of public notebooks within the final week of the competition, but encourage you to use your best judgment prior to that deadline.

Happy Modeling!

---

### Incorrect labels from the dataset

来源：https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/407400

Hello everyone,

There are a few misunderstandings regarding the classes of the discovered dataset. The dataset is undoubtedly unbalanced. Therefore, my team attempted to locate additional data for the few-image-classes. There are numerous labels that are orders or families of other ones.

Acanthascinae is also an unacceptable name for the Rossellidae family.

Careproctus is the genus of the following three species.

Lyssacinosida is a superior order of species.

…

In order to add more data for training the models, we proposed a method for locating accurate images in which we first locate its images on the FathomNet API and then compare it to the internet-source images on Marine websites such as marinespecies.org.

In addition, we hope that this method will improve the FathomNet database for correctly relabeling images.

---

### Similar competitions in the past

来源：https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/397024

Hi, below I have collected a list of similar competitions in the past, which may inspire you in the this competition:

iNaturalist Challenge at FGVC 2017

iWildCam2018

iNaturalist 2019 at FGVC6

iNat Challenge 2021 - FGVC8

---

### Metric Fix and Rescore

来源：https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/404769

As noted in other topics, there was a bug in the metric that was causing the AUC portion of the metric to be scored incorrectly. I fixed the bug and rescored the current submissions. Please let me know if you have any concerns or questions.

You can find an implementation of the metric here: FathomNet metric.

---

### Looking for a Team Megathread

来源：https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/397070

Use this thread to find a teammate if you're interested in finding others to work with!

Please note: You must merge within the Kaggle platform before sharing any private competition information to be considered in adherence to competition rules.

---
