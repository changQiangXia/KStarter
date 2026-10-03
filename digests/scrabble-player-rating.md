# scrabble-player-rating

- 类别：Playground ｜ 主题：tabular ｜ 子类：— ｜ 领域：—
- 截止：2022-12-15 ｜ 队伍数：301 ｜ 机制：标准赛
- 评估指标：Root Mean Squared Error
- 讨论区：12 条主题

## 讨论区索引（按票数排序）

- 16 票 / 3 评论 | Welcome to the Scrabble Player Rating competition! 
  https://www.kaggle.com/competitions/scrabble-player-rating/discussion/362735
- 10 票 / 3 评论 |  📌 Advanced Dataset, FE+AGG 🏆🏆🏆 
  https://www.kaggle.com/competitions/scrabble-player-rating/discussion/363143
- 9 票 / 1 评论 | Public kernels on scrabble- ready reference and starter 
  https://www.kaggle.com/competitions/scrabble-player-rating/discussion/362744
- 6 票 / 2 评论 | Competition evaluation metric RMSE -- adjutant resources for ready reference 
  https://www.kaggle.com/competitions/scrabble-player-rating/discussion/362749
- 5 票 / 3 评论 | Please tell me to create a win/loss prediction model using a rating system 
  https://www.kaggle.com/competitions/scrabble-player-rating/discussion/363404
- 3 票 / 2 评论 | Now that it's over... 
  https://www.kaggle.com/competitions/scrabble-player-rating/discussion/372554
- 2 票 / 4 评论 | Anyone making progress? 
  https://www.kaggle.com/competitions/scrabble-player-rating/discussion/363485
- 2 票 / 0 评论 | FE, Public Dataset & Notebook Example 🔥 
  https://www.kaggle.com/competitions/scrabble-player-rating/discussion/365721
- 2 票 / 0 评论 | Scrabble- game introduction and adjutant resources for ready reference 
  https://www.kaggle.com/competitions/scrabble-player-rating/discussion/362747
- 1 票 / 5 评论 | submission error 
  https://www.kaggle.com/competitions/scrabble-player-rating/discussion/364897
- 0 票 / 1 评论 | Scrrable player rating 
  https://www.kaggle.com/competitions/scrabble-player-rating/discussion/371459
- 0 票 / 2 评论 | Can we get the word list? 
  https://www.kaggle.com/competitions/scrabble-player-rating/discussion/363660

## write-up 正文（6 篇）

### Now that it's over...

来源：https://www.kaggle.com/competitions/scrabble-player-rating/discussion/372554

Now that the competition is wrapped up, I was wondering if folks, especially those that did well, might share what they did for the competition for the edification of the community.

For myself, I ended up using a lot of aggregate player features (i.e. min, max, mean of a player's scores for their previous games) over the course of their games up to the current one, along with the turns features from this notebook. I then used LightGBM with Optuna for the final model and to tune the hyperparameters respectively. My notebook is available here.

One thing I never did figure out was the correct cross-validation scheme. I originally started with just KFold, but then went to GroupKFold with the nicknames as the groups when I realized that the data had all of a player's history in either test OR train, but not split across both. Using this CV actually gave me substantially worse scores. Even using 'StratifiedGroupKFold' with stratifying across a combination all of the game types (i.e. time_control_name, rating_mode, and lexicon) did not improve performance much. So, what did other folks do for for cross-validation? Was keeping entire player's games separate between test or train the right strategy?

---

### Public kernels on scrabble- ready reference and starter

来源：https://www.kaggle.com/competitions/scrabble-player-rating/discussion/362744

Hello all, wishing you all the best for the challenge! 

Given below are some kernels on the topic from Kaggle's public code repository for a ready reference- 

https://www.kaggle.com/code/mpwolke/it-s-my-turn-scrabble#Brazilians-will-understand-and-laugh-with-me.

https://www.kaggle.com/code/mrisdal/analyze-basicbot-s-scrabble-game-data-from-woogles

https://www.kaggle.com/code/metlover/cnn-ann-approach-using-flux-jl-17-24339-rmse -- this may be a good starter in my opinion

https://www.kaggle.com/code/mathurinache/scrabble-starter -- another recommended starter in my opinion

https://www.kaggle.com/code/toadofsky/omgwords-starter

I wish to extend thanks and regards to the creators of these kernels. Hope these materials help! Good luck and happy learning!

---

### Welcome to the Scrabble Player Rating competition!

来源：https://www.kaggle.com/competitions/scrabble-player-rating/discussion/362735

Hello Kagglers!

Welcome to the Scrabble Player Rating competition. In this playground competition, you will use data from games played on woogles.io, a competitive Scrabble website, to predict player ratings in matches between humans against 3 bot players. So you can imagine you're a Scrabble scout watching players in matches against the bots in one league … you're familiar with these players, how good they are, and what their ratings are. Then, imagine you take a trip abroad to observe a new league with a totally different set of human players against the same bots. Can you guess what the human players' ratings are based on how they play the game against the bots?

This is the second competition I've launched that uses game play data from matches played on woogles.io. So you may find inspiration from the first competition which focused on predicting the point value of the next play.

Let me know if you have any questions! I'll be here to answer as best as I can. Despite being a Kaggle admin, I'm not a professional data scientist … and I am passionate about Scrabble and data. :)

Cheers & Happy Kaggling!

Meg

PS thank you again to the creators of woogles.io!

---

### Competition evaluation metric RMSE -- adjutant resources for ready reference

来源：https://www.kaggle.com/competitions/scrabble-player-rating/discussion/362749

Hello all, 

Given below are some ready reference materials for the competition evaluation metric- RMSE (Root Mean Square Error). Hope they are useful for one and all. Kindly note that the smaller the value, the better the result!

https://en.wikipedia.org/wiki/Root-mean-square_deviation -- wikipedia article for the metric

https://www.statisticshowto.com/probability-and-statistics/regression-analysis/rmse-root-mean-square-error/ -- very useful introduction to the metric 

https://www.youtube.com/watch?v=N6y5wqdIBas -- short but useful video on the metric

https://towardsdatascience.com/what-does-rmse-really-mean-806b65f2e48e -- provides a brief introduction to the metric with the formulae

All the best and happy learning!

---

### Please tell me to create a win/loss prediction model using a rating system

来源：https://www.kaggle.com/competitions/scrabble-player-rating/discussion/363404

Sorry for the topic, which has nothing to do with this competition.

The rating system is a very useful indicator in predicting the winners and losers of a match.

I expect that by using rating points as one of the features, machine learning models will predict the winners and losers of matches with high accuracy.

In particular, I would like to predict the outcome of a professional Shogi (Japanese chess) tournament, one of the traditional tabletop games in Japan.

For this purpose, I am looking for an example of a model that can predict the winners using features such as rating points and the compatibility of each player in a tabletop game such as chess.

I thought that some of the participants in this competition might be familiar with machine learning to predict winners and losers.

If you know something about it, please let me know!

---

###  📌 Advanced Dataset, FE+AGG 🏆🏆🏆

来源：https://www.kaggle.com/competitions/scrabble-player-rating/discussion/363143

Hi all,

I created new features and aggregated them for faster modeling in this notebook. You can find new features like difficult_word in the dataset.

You can find the dataset here.

Kindly upvote if you find the dataset useful 😊

---
