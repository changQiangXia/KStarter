# iwildcam2022-fgvc9

- 类别：Research ｜ 主题：cv ｜ 子类：— ｜ 领域：—
- 截止：2022-05-30 ｜ 队伍数：24 ｜ 机制：标准赛
- 评估指标：Mean Absolute Error
- 讨论区：16 条主题

## 讨论区索引（按票数排序）

- 16 票 / 0 评论 | 🔥🔥 Useful References Notebooks - from the past Wildcam Competitions 🔥🔥 
  https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/314736
- 5 票 / 3 评论 |  Notebooks To Get You Started! 
  https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/323139
- 5 票 / 1 评论 | Announcement: DeepMAC segmentation masks are now available! 
  https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/316483
- 4 票 / 0 评论 | 1st Place Solution 「write-up」
  https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/328965
- 4 票 / 3 评论 | DeepMAC Class-agnostic Segmentation Model data 
  https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/315980
- 3 票 / 1 评论 | Welcome to iWildCam 2022 
  https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/314608
- 3 票 / 0 评论 | 9th place solution 「write-up」
  https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/328526
- 3 票 / 0 评论 | Other Fine-Grained Competitions on Kaggle from the FGVC9 Workshop at CVPR 
  https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/317727
- 3 票 / 4 评论 | Doubts regarding the sample submission format 
  https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/317140
- 3 票 / 1 评论 | New to Kaggle or Machine Learning? Check this out ~ 
  https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/314432
- 3 票 / 1 评论 | How to pass an index while we're passing scalar values? 
  https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/315064
- 2 票 / 0 评论 |  Read Papers About Machine Learning And Object Counting! 
  https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/323876
- 2 票 / 7 评论 | Looking for a Team Megathread 
  https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/314430
- 0 票 / 2 评论 | Competition Wrap Up [DUE BY JUNE 10TH] 
  https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/328927
- 0 票 / 3 评论 | Duplicates in the data 
  https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/324436
- 0 票 / 4 评论 | Data sequence out of order 
  https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/324425

## write-up 正文（6 篇）

### 9th place solution

来源：https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/328526

Congratulations to the winners and thank you to the competition hosts, current and past, for continuing to sponsor this important, enjoyable competition. I confess that it still challenges me even in its reduced animal-only, counting form. Goats! How can anyone count goats, wandering here and there, staring into the camera? I would love to hear how the top teams - anybody for that matter - approached this counting problem.

Outline of my approach

Use MegaDetector v4 detections to train a 2nd animal detector based on Yolov5.

Merge MegaDetector and Yolov5 detections using weighted boxes fusion WBF.

Apply a custom frame-to-frame object tracking algorithm focused on individuals within herds/packs. 

The herd/pack species that I focused on:

Category Id
Common Name

2
white-lipped peccary

8
collared peccary

70
wild goat

71
domesticated cattle

72
domestic sheep

90
african bush elephant

96
impala

256
dromedary camel

Observations

I first learned about WBF in the Kaggle COTS starfish competition where it was used by many teams to post process detections. I used it successfully to merge the sponsor-provided MedaDetector detections with my Yolov5 detections and it gave me a public/private LB score of 0.275/0.265 (above Benchmark: iWildCam 2021 winner). I spent some time tuning the algorithm's hyperparameters but I'm not sure it provided any significant benefit beyond my initial success.

I found plenty of anecdotal evidence that an inter-frame counting approach could improve on the standard max approach of the benchmarks, but I was never able to get my solution to provide any benefit once I scaled up to the whole dataset. Since the approach works well in video, I hoped it would work with some of our sequences. The first step in my process was to try to estimate the overall direction a herd was moving so that I could eliminate many candidates from the inter-frame matching process. Again, this was easy to do in many cases, but unreliable overall, leading to weaker matching in most cases. I'm still looking into the details of exactly what happened.

Additional detail for the inter-frame matching approach: Herd sequences were identified by a 9-class Yolov5 detector. For any sequence with a preponderance of herd detections, detection-level matching was performed using the following method. An autoencoder was trained on small chips from the center of mass of the DeepMac mask for each detection. The autoencoder produced a 512-element latent feature vector for each detection. These latent features (along with X,Y, area, delta-T) where used in detection-to-detection matching within the sequence. Using the DeepMac segmentation masks to select which chips are fed to the autoencoder showed improvement over using the entire detection (scaled) or the center of the detection. Presumably this is due to the elimination of non-individual pixels due to occlusion and/or background between the individual's legs.

My largest counting errors in the validation set usually involved domestic cattle. Consequently, I spent a lot of time looking at sequences of domestic cattle and getting a little discouraged about not being able to spend more time with the more exotic animals. Then I heard a story on public radio about how damaging cows can be in many different situations. This got me thinking about camera traps for habitat destruction monitoring and suddenly counting cattle seemed much more significant.

---

### 🔥🔥 Useful References Notebooks - from the past Wildcam Competitions 🔥🔥

来源：https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/314736

🔥🔥 Useful References Notebooks - from the past Wildcam Competitions 🔥🔥

2021 Contest

 
1st Place Solution by Fagner Cunha

 
Discussion: https://www.kaggle.com/competitions/iwildcam2021-fgvc8/discussion/245460

 
Code: https://github.com/alcunha/iwildcam2021ufam

 
 
2nd place solution by johnbeuving

 
Discussion : https://www.kaggle.com/competitions/iwildcam2021-fgvc8/discussion/245559

 
 
3rd Place Solution by JuanCarlosLópezEnriquez

 
Discussion : https://www.kaggle.com/competitions/iwildcam2021-fgvc8/discussion/244950

 
 
4th Place Solution by Charlie Turner

 
Discussion : https://www.kaggle.com/competitions/iwildcam2021-fgvc8/discussion/243509

 
 
7th Place Solution by Devashish Prasad

 
Discussion : https://www.kaggle.com/competitions/iwildcam2021-fgvc8/discussion/242978

 
Code: https://www.kaggle.com/code/devashishprasad/iwildcam2021-submission/notebook

 
 
2020 Contest

 
 
Code: https://www.kaggle.com/aleksandradeis/iwildcam-eda

 
Code: https://www.kaggle.com/nayuts/iwildcam-2020-overviewing-for-start

 
Code: https://www.kaggle.com/ateplyuk/iwildcam2020-pytorch-start

 
Code: https://www.kaggle.com/manojacharya/fastai-implementation-after-pre-processing-images

 
Code: https://www.kaggle.com/qinhui1999/how-to-use-bbox-for-iwildcam-2020

 
Code: https://www.kaggle.com/bsridatta/eda-and-object-extraction-for-classifier-training

 
 
2019 Contest

 
 
Code: https://www.kaggle.com/artgor/iwildcam-basic-eda

 
Code: https://www.kaggle.com/gpreda/iwildcam-2019-eda-and-prediction

 
Code: https://www.kaggle.com/xhlulu/densenet-transfer-learning-iwildcam-2019

 
Code: https://www.kaggle.com/tanlikesmath/fastai-starter-iwildcam-2019

 
Code: https://www.kaggle.com/rblcoder/cnn-in-tf-coursera-course-iwildcam-2019-mobilenet

 
 
Hope you liked it. All the best!

##### One of the reference - https://www.kaggle.com/competitions/iwildcam2021-fgvc8/discussion/225161

---

###  Notebooks To Get You Started!

来源：https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/323139

'

All right guys! Listen up.

This is what you need to do to get started on your notebooks!

Here is a list of starter notebooks that will help you get started on the competition.

Welcome to the Kaggle competition iwildcam2022-fgvc9!

Good luck and happy coding!

Iwildcam 2022 Cnn by @mpwolke

 
@mpwolke uses a simple CNN, TensorFlow, and GPU machines.

This notebook will take you through the basics of Neural Networks, how they work and how to implement a simple 3-layer neural network in TensorFlow. Along the way, you will also learn how to load data and train your model on a GPU enabled machine. After completing this notebook, you will know enough to start working on more complicated Neural Networks.

Iwildcam2022 Show And Extract by @stpeteishii

 
The methods used by @stpeteishii are mainly to show how to load, extract and play with the data!

If you are looking for a way to relax and de-stress, I urge you to go through my notebook. The magnificent, colorful, and vibrant images will take your breath away and transport you to another world. Each page will leave you feeling inspired and motivated.

Iwildcam 2022 Visualize Deepmac Instance Masks by @stefanistrate

 
This notebook uses methods such as visualization and deep learning to help the reader understand the instance masks.

This notebook will help you visualize instance masks in action. After going through this notebook, you will be able to see how the training data is built detect some key components that are important for your competitive edge.

Gps Data Visualization by @vickyskarthik

 
@vickyskarthik uses clustering methods to analyze the GPS data.

Take a stroll through the world of GPS data visualization with @vickyskarthik. Using beautiful, colorful markers on an interactive map, you can explore the clustering of GPS coordinates around the world. You can also see how different clusters correspond to different physical locations. This is a great way to see how data is organized and to get a sense of where different areas are located.

Iwild Tf Starter by @thomasdubail

 
@thomasdubail uses Tensorflow to create machine learning models.

This notebook will take you on a beautiful journey into the fascinating world of deep learning, where you will learn how to create state-of-the-art machine learning models. With @thomasdubail's clear and concise instructions, you will be able to easily follow along and build your very own neural networks.

---

### 1st Place Solution

来源：https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/328965

Our method is based on filtering detection results of megadetector. No model training or tracking algorithm is involved. We just return the max number of objects among all images in sequence as our final predict.

By observation, if we set 0.95 as confidence threshold, we found that we will undercount animals in images with high-density objects and overcount animals in images with low-density objects. So we divided all images in to low-object -density images and high-object-density images and then use different filtering methods to solve them separately. The threshold is 8 predictions in a image

high-object-density images

To count more animals, we set the confidence threshold as 0.0. To remove the duplications we applied NMS method and set IoU=0.2. We also make little modifications to suppress smaller boxes. I cannot upload images but the filtering result is pretty good by observation. With the help of our NMS method, the public score can increase to 0.253

low-object-density images

If we don't take confidence score into consideration, We assume that area with many bounding box overlap has higher tp probability than area without overlapping bounding boxes if set the confidence threshold as 0. After few times of fine-tuning, we found that 0.98(confidence threshold) for boxes without overlaps and 0.8 for boxes with overlap can get best public score. Public score can raise up to 0.249 now. We also applied second round of filtering for images with 1 or 2 object left after first round of filtering. The confidence threshold is 0.98 and now we get our best result 0.247

Summary

We don't try any training methods because ground truth is not provided and if we use the detector's result as training data, the error propagation will happen and new model cannot outperform megadetector if we don't manually filter out FP prediction of megadetector. We attend this competition 1 week before deadline so we don't have enough time to focus on tracking algorithm. If time permits, we will continue the study and focus on tracking objects in image sequence.

---

### Announcement: DeepMAC segmentation masks are now available!

来源：https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/316483

We have now published DeepMAC segmentation masks for the bounding boxes identified by MegaDetector V4. Data is available on Kaggle and can also be downloaded directly via the competition's GitHub page. We hope these will help you get more insights into the data and build better models.

We are also providing an updated notebook to visualize the masks: https://www.kaggle.com/stefanistrate/iwildcam-2022-visualize-deepmac-instance-masks

Happy coding!

---

### DeepMAC Class-agnostic Segmentation Model data

来源：https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/315980

The data page indicates that segmentations from DeepMAC are "coming soon". Any news on when that data might be available?

---
