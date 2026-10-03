# geolifeclef-2022-lifeclef-2022-fgvc9

- 类别：Research ｜ 主题：cv ｜ 子类：— ｜ 领域：—
- 截止：2022-05-24 ｜ 队伍数：52 ｜ 机制：标准赛
- 评估指标：MeanBestErrorAtK
- 讨论区：23 条主题

## 讨论区索引（按票数排序）

- 11 票 / 5 评论 | 🥇 1st place solution description 「write-up」
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/327055
- 11 票 / 3 评论 | .tif files - how to deal with it? 
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/311983
- 10 票 / 1 评论 | Previous Year GeoLifeCLEF Challenge, Notebook and Paper 
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/312112
- 8 票 / 2 评论 | 🔥🌞💢 Resources for this contest - From ImageCLEF website and Kaggle ❄🎯🔥 
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/312283
- 6 票 / 3 评论 | Welcome to GeoLifeCLEF 2022! 
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/312093
- 6 票 / 5 评论 | Looking for a teammate 
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/312788
- 5 票 / 0 评论 | Meaning of some filename codes. Environmental_vectors.csv file 
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/313558
- 5 票 / 4 评论 | Sharing baselines ? 
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/312696
- 4 票 / 5 评论 | What about SnakeCLEF 2022? 
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/315024
- 4 票 / 0 评论 | 2nd place solution description 「write-up」
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/328637
- 3 票 / 0 评论 | Final week and CLEF working notes submission information 「write-up」
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/325984
- 3 票 / 6 评论 | Sharing thoughts: Single class labeling is probably misleading models 
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/325767
- 3 票 / 1 评论 | Time feature ?  
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/318426
- 3 票 / 1 评论 | Research papers on deep learning for image segmentation! 
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/321452
- 3 票 / 1 评论 | Why these competitions don't have medals? 
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/313714
- 3 票 / 0 评论 | GDAL-Geospatial Data Abstraction Library 
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/312250
- 2 票 / 3 评论 | Cannot have my efficientnet to decrease top30 error rate 
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/325902
- 2 票 / 0 评论 | Notebooks To Start From! 
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/323140
- 2 票 / 1 评论 | Looking for team mates! 
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/313968
- 2 票 / 0 评论 | The right Raster in the the right Lat/Long. Geotiff (.tif) Raster File Format.  
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/313562
- 1 票 / 6 评论 | Competition wrap-up 
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/327037
- 1 票 / 0 评论 | Open Source Segmentation Projects 
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/325095
- 0 票 / 4 评论 | Looking for teammate 
  https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/315063

## write-up 正文（6 篇）

### 2nd place solution description

来源：https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/328637

Well, I guess it's my time to explain the solution that clocked in second on the private leaderboard.

Similar to the post by the winners (congratulations!) I will not go into every single detail; this will be made available through the technical report.

General overview

My solution is based around deep convolutional neural networks (CNNs) that process the satellite remote sensing (RS) products only. In detail, the base model consists of two CNN feature extractors (standard image classiﬁcation architectures that had their ﬁnal, fully-connected classiﬁcation layer dropped). They run in parallel and ingest different parts of the RS imagery: the ﬁrst receives the RGB portion of the dataset, the second a stack of altitude, near-infrared (NIR) and NDVI (normalised difference vegetation index: (NIR-red)/(NIR+red)). I previously used the land cover map as input instead of the NDVI, but providing continuous models like CNNs with a discrete map of ordinal class indices is non-straightforward and not imminently sensible, hence the NDVI.

The two feature extractors process their assigned three-channel imagery in parallel, but do not share parameters. They each output a latent feature vector of the same size, which gets concatenated, subjected to heavy dropout (probability of 0.45 worked best), and converted into per-class activations by a single fully-connected layer that maps to the 17,034 species. A standard softmax-cross-entropy loss is used to train the model (more on that below).

What helped improve accuracy

I ran extensive experiments and tried many different ideas; many without success (as is usually the case). However, the following four provided sufﬁcient individual boosts in accuracy:

Correct model architectures: I commenced with a ResNet-50 for each of the two feature extractor branches. This worked reasonably well, but I got an improvement of almost 2% simply by switching to Inception-v4. I also tried DenseNet-201, which performed similarly to ResNet-50. More complex and recent architectures were on the list as well, including ConvNext and a Vision Transformer (ViT B/16). Those two took forever to train, despite decently powerful hardware (see below), and just resulted in massive overﬁtting (35% top-30 on train, 5% on val).

Pretraining: deep learning models oftentimes require some form of pre-training to be able to adapt well, due to the enormous search space with millions of free parameters. Different means of pre-training were on my list, but what eventually worked best was to simply use the weights from ImageNet pre-training. See below for other ideas.

Spatial block-label swap: while the two points above are important to make the model work in the ﬁrst place, this here is the most relevant for the performance of my model by a long shot. This is a training concept that boils down to the presence-only label problem we are facing: a non-observation of a species at a particular location does not imply that the species is not there. This circumstance, together with the fact that each data point is assigned just one single species, technically violates the assumption made with by-the-book heuristics like cross-entropy loss: this one assumes that each data point has exactly one correct label and that all other classes are to be zero (it minimises the entropy in the predicted probability space). While the GeoLifeCLEF dataset is set up this way, this causes the prediction problem to be ill-posed. It is thus prudent to ﬁnd a training strategy that takes this into account. A popular idea is to use a temperature softmax, but this only softens the blows for the model to a certain extent. My solution, the spatial block-label swap, attempts to relax the strict one-class requirement as follows: it ﬁrst creates a spatial grid of square cells (0.01x0.01° lat/lon) and assigns each training point to its encompassing cell. During training, it then performs a look-up for each data point and randomly replaces its label with one of the neighbours in the same grid cell with a probability of 10%. This is a simple but sort of intuitive means of regularisation, and it helped the model gain another 2% of accuracy. I tried different replacement chance probabilities, as well as more sophisticated strategies (e.g., swapping according to encounter probabilities of a species within the grid cell), but the most simple method worked best.

Ensembling: as with many contests (I believe), an ensemble of different models worked best. For the submission I ensembled ten different models trained; some ResNet-50, some Inception-v4, one DenseNet-201. Each was trained with different slight alterations (e.g., different learning rates, different random seeds), but the general concept always stayed the same. I ensembled the output probabilities, but in a pseudo-conﬁdence-based manner: I performed test-time augmentation (also important) and recorded the variance of conﬁdence across the augmentations for each test sample and each model. I then normalised and inverted the variances per model, so that they were bound to [0,1], and applied a softmax across all ten model runs. This provided me with a crude notion of model conﬁdence. Multiplying the softmax scores with the mean model conﬁdences across augmentations and summing them together gave the ﬁnal prediction score, from which I drew the top-30 species. Ensembling gave yet another ~2% boost over the single models.

What I tried without success

A setup and challenge like GeoLifeCLEF absolutely invites to try out many different ideas. Providing an exhaustive list of tricks I attempted is beyond the scope of this thread, but here's some of the more relevant ones that simply did not want to work:

Other covariates: I tried plugging in the environmental rasters (one value extracted per data point), as well as the GPS coordinates, into the model. None of this worked well. I attribute reasons to the difﬁculty of normalising features against the RS-emerging ones and the difﬁculty in extracting features in the ﬁrst place (going from environmental covariates to latent features requires usage of an MLP, which is always a bit messy). The winners have done the better move here by using a non-DL model for the covariates, such as a Random Forest. It shows that DL isn't always the answer (which sounds ironic, given that this is only what I used). Otherwise, encoding geospatial coordinates is not straightforward either. Since we only have the contiguous U.S. and France as study areas, we don't have the periodicity problem, but it still is nontrivial to use those. An MLP trained on the coordinates only, sometimes raw, sometimes sine-cosine-encoded, and once with a more advanced encoding (Theory-guided spatial encoding), just led to severe underﬁtting. I believe more research on this multimodal covariate integration would be an interesting avenue to explore further.

Auxiliary prediction tasks: at some point I tried predicting not just the species class, but the other layers of the taxonomy tree (genus, family, kingdom) with individual fully-connected layers on top. That worked ok, but did not improve species classiﬁcation.

Predicting histogram densities: with the spatial block-label swap strategy explained above, I tried predicting the occurrence histogram per grid cell per species. This provided too faint a learning signal, though.

Advanced pre-training: besides standard ImageNet weights, I tried self-supervised pre-training (in particular MoCo-v2, which is what the winner of last year's challenge used), and an own form of Model-Agnostic Meta-Learning (MAML); resp. the more lightweight alternative Almost No Inner Loop (ANIL). I also tried training models from scratch. In the end, ImageNet is what performed best.

Addressing the long-tail: the species classes are severely long-tailed (i.e., thousands of species have less than ten images and a few make up the vast majority of the dataset). That strongly confuses machine learning models by default, with the result that the rare species never get predicted. I tried many ideas to cope with this, from loss weights over special losses (e.g., Balanced Softmax) to ANIL pre-training (see above). In the end, doing nothing about it worked best—for a very simply reason: the test set could be assumed to be as unbalanced in species classes as the training and validation sets. Hence, giving more weight to the rare species is actually the opposite of what one wants to maximise performance. I could probably even have dropped many of the rare species with possibly performance gains, as the model had a less complicated task to solve (I didn't do that, though).

Setup

I distributed training to three machines: two workstations (16-core CPU, 128 GB RAM, NVIDIA GeForce RTX 3090 each; Ubuntu 20.04 LTS) and an HPC (NVIDIA Tesla V100; RHEL 7). I used Python 3.8.10 and implemented my solution in PyTorch 1.9.0. Models came from either Torchvision (ResNet-50) or the PyTorch Image Models (TIMM) library (Inception-v4, DenseNet-201, Inception-v4, ViT B/16).

Lessons learnt

This would be a big one to cover. It was difﬁcult to get to the grounds of the performance of models, due to the sheer number of species classes. However, gradually getting a feel for how the models perform over different experiments was possible to an extent and certainly helped in settling in on standard parameter sets and avoiding pitfalls. There is a slew of ideas to be tested still, such as advanced data augmentation (I only used random flips, addition of Gaussian noise and normalisation), grid-searching hyperparameters, and other architectures I didn't try (EfﬁcientNet, for example). Otherwise, adequately using all available covariates on the one hand, and further exploring tweaks about the label situation on the other, are probably worth studying.

Apologies for the long post; I hope it was at least somewhat insightful. Full details on the solution will be given in the technical report.

Many thanks for everyone involved: the dataset creators, contest organisers, data collectors, and of course the competitors! It was quite exciting to see developments on the leaderboard, especially towards the end. Huge congratulations to the winners; your solution reads fantastically and that win is more than well-deserved!

Thank you.

---

### 🥇 1st place solution description

来源：https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/327055

I was thinking how to explain it without spending too much hours but as clear as possible, probably later I will make a graphical representation of the entire data pipeline, models and inference and also maybe a notebook with some preprocessing functions and our best part of the entire experimental pytorch lightning pipeline, but for now I will share what I was writing on the Competitiors Feedback form about our best solution and what we tried that didn't work well. Sorry if I'm not accurate or I don't explain it with more details, it is probably a little bit too dense, specially for those who haven't been fully involved on the competition. What's more, for those of you who can speak or understand Spanish, you can take a look at my Team partner @juansensio Youtube channel were he shared a couple of Twitch lives were he was starting to solve this challenge and he defined the pytorch lightning workflow pipeline, updating metrics to Weights and Biases: https://www.youtube.com/c/sensio-ia

Best solution description:

Ensemble of 3 models: 

1- The first one was a bi-modal network with Nir+G+B on a pretrained resnet34 stacking its final layer to a FCN of 3 layers with the inputs of the environmental vectors + lat + lon + country + alt mean + max-min alt + "dothot" encoding (this is how I called the somehow softmax-onehot encoding) of landcovers, these two backbones were connected to the final 17k class layer. 

2- The second model was similar to the previous but the CNN was a mobilenetv3 100 large pretrained model with the input of R+G+B+Nir, the FC network was the same of the previous one and between the two stacked final layers of these two models we added an extra Linear Layer of 2048 with dropout and ReLu and then the final 17k layer for classification. 

3- The third model was a Random Forest with 32 estimators and a depth of 12, using as inputs the same as the previous FC networks: the environmental vectors + lat + lon + country + alt mean + max-min alt + dothot encoding (softmax-onehot encoding) of landcovers, and also in addition the 25, 50 and 75% percentiles of each of the R/G/B/Nir layers, so 81 input features in total, adding also the validation data to the training. 

In addition the first two models had Data Augmentation on the CNN models of random vertical and horizontal flips, rotations and 5-10% of Brightness and Contrast. We also implemented Test Time Augmentation of 5 random image transformations for each sample and then we merged these with the mean probabilities of every prediciton. We applied this same strategy of the mean probablities to merge the 3 models ensemble. Finally we tried to retrain a little further the models adding validation data to train data and it improved a little but probably we could do it better. 

Our setup is a rtx3090 with 24gb of vram, with a 12th gen i7 and 64gb of ram from my side and Juan has also a heavy dutty rig with two rtx3090. It's been so much helpful that amount of VRAM for the CNNs but also I needed so much CPU RAM for the Random Forests with 17k classes.

Things that we also tried but performed worse:

We tried to aggregate close labels to have multi label observations, we tried it in different ways and different loss functions but none resulted better than single labels, but something tells me that there has to be a way to make it work. Regarding to labels aggregation, I noticed that at some spots there were up to some hundreds of different labels together, which means that there is a theoretical minimum top30 error to achieve as at some point, even with an ideally perfect model, you will have to bet on 30 labels among 50, 100 or more which are really correct in that location. 

We also tried other backbones in the CNN models, we tried to train without transfer learning on these, we tried to put three different backbones for 1. RGBNir + 2. Alt tiffs + 3. Landcover tiffs and then adding this to the FC tabular data backbone to name the most relevant. None of these gave us the best results but probably there is room for some of those to make it better. I also tried gradient boosted trees but with 17k classes this would need probably around a terabyte of RAM I guess.

Conclusion:

At the end I value very positvely our experience participating in this competition, I personally learnt and practised some different new techniques and types of data but I would like to highlight two: the use of multi-modal networks were you can mix structured and unstructured data with their own backbones to finally merge them in the same final layers and also to tackle a problem of presence-only data, something that I have never before encountered or thinked of, but it could really be in other areas like medicine, financial and more, where you can have latent or hidden variables.

Thank you very much to the organizers and the Kaggle team. Also a big aplause to all the people who collect this kind of ecological bio data out there, it's incredible to have almost two millions of data points together with this level of diversity. And finally good job to all the other teams and members who have participated and have motivated us to keep pushing until the last day, I wish that our notes give you all more knowledge and I'm curious to see and learn from what else has been tried and done to achieve almost as good results as ours!

Best Regards!

Enric Domingo

---

### 🔥🌞💢 Resources for this contest - From ImageCLEF website and Kaggle ❄🎯🔥

来源：https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/312283

A collation of resources for this contest!

Some Useful Papers

 

 
Overview of LifeCLEF 2020: A System-Oriented Evaluation of Automated Species Identification and Species Distribution Prediction

 
Overview of LifeCLEF 2020: A System-Oriented Evaluation of Automated Species Identification and Species Distribution Prediction

 
LifeCLEF: Species identification and prediction

 
Overview of LifeCLEF location-based species prediction task 2020 (GeoLifeCLEF) 

 
A Kaggle notebook from 2021 - GeoLifeCLEF2021 - Baselines and submission

 

A Curation from the imageclef website detailing all previous contests

 

ImageCLEF 2022

LifeCLEF 2022

ImageCLEF 2021

LifeCLEF 2021

ImageCLEF 2020

LifeCLEF 2020

ImageCLEF 2019

LifeCLEF 2019

GeoLifeCLEF 2019

PlantCLEF 2019

BirdCLEF 2019

ImageCLEF 2018

LifeCLEF 2018

ImageCLEF 2017

LifeCLEF 2017

ImageCLEF 2016

LifeCLEF 2016

ImageCLEF 2015

LifeCLEF 2015

ImageCLEF 2014

LifeCLEF 2014

ImageCLEF 2013

ImageCLEF 2012

ImageCLEF 2011

ImageCLEF 2010

ImageCLEF 2009

ImageCLEF 2008

ImageCLEF 2007

ImageCLEF 2006

ImageCLEF 2005

ImageCLEF 2004

ImageCLEF 2003

Publications

FAQ

Resources

 

[图 1: inbox%2F59561%2Fcc6d9a21f0c3ed71b00113b33efb2b66%2Fkaggle_sweater.png]

Hope you like it. 

Best wishes for the competition

[图 2: 360-F-238882142-RR07-WHn-FIm82-FA6x-Rv-U7-MLos0-Mxrf-Hgw.jpg]

---

### Final week and CLEF working notes submission information

来源：https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/325984

Hi everyone,

First of all, thank you for your participation in GeoLifeCLEF 2022.

There are a few days left before the end of the competition (unfortunately, the deadline is strict, sorry for that).

As you have noticed, GeoLifeCLEF is a difficult challenge that involves large and varied data.

The underlying stakes are however immense for the monitoring and preservation of biodiversity on a global scale.

We therefore congratulate all of you who managed to submit runs and we are very happy to see that several of you beat the baseline models by a large margin.

Note that the public leaderboard only relies on 10% of the test data, it is thus a bit noisy and the private leaderboard (constituting the final results) might change a bit the ranking.

So make sure to select the models that you trust the most based on your validation scores and not solely on the public leaderboard scores!

GeoLifeCLEF being part of the CLEF initiative, the next step for you is to write a so called "working note", i.e., a technical report describing your methods and results.

The deadline to submit it is June 01.

The working note doesn't have to be as detailed as an article, but it should still report the minimum necessary information to enable the reproduction of your method and results.

After a (light) review process, you will have a feedback on June 13 and then you will have more time, until July 1, to finalize the working note.

Submitting a working note is mandatory to get your results published in the scientific articles that we will write afterwards.

Any run that could not be reproduced thanks to its description in the working notes might be removed from the official publication of the results.

Working notes themselves are published within CEUR-WS proceedings, resulting in an assignment of an individual DOI (URN) and an indexing by many bibliography systems including DBLP.

According to the CEUR-WS policies, a light review of the working notes will be conducted by LifeCLEF organizing committee to ensure quality.

As an illustration, LifeCLEF 2021 working notes (task overviews and participant working notes) can be found within CLEF 2021 CEUR-WS proceedings in the "LifeCLEF: Multimedia Life Species Identification" section (see also CLEF 2020 CEUR-WS proceedings for more examples).

Last year's winning solution working notes is available here.

More information about the templates (latex, doc) to use, the mandatory information to report (about the names, affiliations, …), etc. is provided here:

http://clef2022.clef-initiative.eu/index.php?page=Pages/instructions_for_authors.html

The direct link to submit your working note through EasyChair is:

https://easychair.org/my/conference?conf=clef2022

(you first need to create an account, then submit a paper to the LifeCLEF track and choose the "Task 3 - GeoLifeCLEF" topic)

Kind regards,

GeoLifeCLEF 2022 organizers

---

### .tif files - how to deal with it?

来源：https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/311983

Hi, I noticed that a lot of pictures in this contest are in .tif format. I didn't know much about this format before, so I wanted to share my short research.

1. What is TIF?

TIF (or TIFF) is an image format used for containing high quality graphics. It stands for “Tagged Image File Format” or “Tagged Image Format”. The format was created by Aldus Corporation but Adobe acquired the format later and made subsequent update in this format. TIF file is capable of holding both lossy jpeg compression and lossless image data. It can also contain vector based graphics data. TIF file format is widely supported in image editing applications. For that it’s a very popular image format among Graphic artists, Photographers, and Publishing authorities.

2. How to load files in Python?

There are at least several ways to load such files. A lot depends on whether we want to load an image in the form of a numeric array or hold it as a graphical object. Three most populars by StackOverflow are:

By using tifffile package

import tifffile as tiff

image = tiff.imread('abc.tif')

By using PIL and numpy packages

from PIL import Image

import numpy as np

image = Image.open('abc.tif')

image = np.array(image)

By using cv2 and numpy packages

import cv2

import numpy as np

image = cv2.imread('abc.tif')

image = np.asarray(image, dtype = np.float64)

If you have worked with .tif files before, share your thoughts on how to best approach this format.

Sources:

https://www.paintshoppro.com/en/pages/tif-file/

https://stackoverflow.com/questions/18446804/python-read-and-write-tiff-16-bit-three-channel-colour-images

https://stackoverflow.com/questions/7569553/working-with-tiffs-import-export-in-python-using-numpy

https://stackoverflow.com/questions/29049771/working-with-tiff-files-in-python

---

### Previous Year GeoLifeCLEF Challenge, Notebook and Paper

来源：https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/312112

2021: https://www.kaggle.com/c/geolifeclef-2021/overview

2020: https://www.imageclef.org/GeoLifeCLEF2020

2019: https://www.imageclef.org/GeoLifeCLEF2019

2018: https://www.imageclef.org/node/229

2017: https://www.imageclef.org/lifeclef/2017/GeoLifeCLEF

Notebook:

https://www.kaggle.com/tlorieul/geolifeclef2021-baselines-and-submission

Papers:

1) Overview of GeoLifeCLEF 2021 :http://ceur-ws.org/Vol-2936/paper-124.pdf

2) Overview of GeoLifeCLEF 2020: http://ceur-ws.org/Vol-2696/paper_192.pdf

3) Overview of GeoLifeCLEF 2020: http://ceur-ws.org/Vol-2380/paper_71.pdf

4) Overview of GeoLifeCLEF 2019 : https://hal.archives-ouvertes.fr/hal-02190170/file/paper_257.pdf

5) Species Recommendation using Machine Learning - GeoLifeCLEF 2019: http://ceur-ws.org/Vol-2380/paper_71.pdf

Good Luck to the competition :)

---
