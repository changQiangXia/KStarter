# kore-2022-beta

- 类别：Playground ｜ 主题：sim-agent ｜ 子类：agent-game ｜ 领域：—
- 截止：2022-04-07 ｜ 队伍数：58 ｜ 机制：标准赛
- 评估指标：kore_fleets
- 讨论区：35 条主题

## 讨论区索引（按票数排序）

- 58 票 / 24 评论 | 1st Place Solution 「write-up」
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/317737
- 16 票 / 2 评论 | Sharing my experience and strategies in building agents in TS/JS 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/315970
- 14 票 / 1 评论 | Sharing my DQN baseline setup using tf.js 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/317289
- 12 票 / 29 评论 | Welcome to Kore - Beta! 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/313582
- 11 票 / 0 评论 | My Reflections 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/317955
- 10 票 / 29 评论 | Switching to 2p for the remainder of the competition 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/316993
- 10 票 / 27 评论 | Beta extended for a week! 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/315572
- 7 票 / 3 评论 | New missile defense 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/316848
- 7 票 / 0 评论 | From Connect-X (Halite, Hungry Geese, Santa 2020, Rock Paper Scissor) till Kore Fleets 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/313794
- 5 票 / 4 评论 | New version with bug fixes! 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/314257
- 5 票 / 2 评论 | Fixed: Maximum length of flight plan 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/313989
- 5 票 / 1 评论 | Rule description 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/313751
- 4 票 / 3 评论 | Typescript and Java Sample Agents 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/313787
- 3 票 / 0 评论 | minor visualiser bug in collisions 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/321628
- 3 票 / 15 评论 | 50 teams but only 1 public notebook? 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/315962
- 3 票 / 0 评论 | Make Kore as Gym Environment 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/315350
- 3 票 / 2 评论 | How to record the history? 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/314305
- 3 票 / 0 评论 | Attacking and defending? 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/314061
- 2 票 / 2 评论 | How to make state key in Q-learning 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/316248
- 2 票 / 6 评论 | Unnatural Fleet + fleet + shipyard collision resolution 「write-up」
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/315895
- 2 票 / 1 评论 | Syntax errors on Rules 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/314344
- 2 票 / 0 评论 | Current Leaderboard Top is an... Official Baseline? 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/314671
- 1 票 / 5 评论 | Make some tweaks to the rating system? 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/316935
- 1 票 / 3 评论 | How to submit tf.js models? 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/316688
- 1 票 / 2 评论 | Kore distribution is not random 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/316092
- 1 票 / 2 评论 | Is classification possible? 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/315125
- 1 票 / 2 评论 | Turn formula for max spawn 10 wrong? 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/315271
- 1 票 / 5 评论 | Attacker bot attack target? 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/314979
- 1 票 / 8 评论 | Potential bug in allied fleet merging 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/314177
- 0 票 / 0 评论 | DQN: Unexpected jumps in Q values 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/317696
- 0 票 / 1 评论 | Populate board set the numpoy and random set global variables 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/317033
- 0 票 / 5 评论 | Multifile submissions 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/315223
- 0 票 / 2 评论 | Keep State 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/315461
- 0 票 / 1 评论 | How do I access an array of the board? 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/315341
- 0 票 / 2 评论 | Upload Error 
  https://www.kaggle.com/competitions/kore-2022-beta/discussion/313965

## write-up 正文（6 篇）

### Sharing my DQN baseline setup using tf.js

来源：https://www.kaggle.com/competitions/kore-2022-beta/discussion/317289

Hi everyone, I just want to share with everyone that I was successful in getting a very simple baseline DQN model using tf.js. It is capable of reaching turn 400 consistently against simple bot and sometimes winning the game. 

Here is the gist:

Input

A 2 * 8 matrix. 

2 for [player, enemies]. I group up all enemies together.

8 for numeric/boolean values of basic information about player and enemies

some of these values are log2 values

details as follows:

const tensorIndexMap = {
 kore: 0,
 totalShipCount: 1,
 outsideShipCount: 2,
 insideShipCount: 3,
 shipyardCount: 4,
 earlyGame: 5,
 middleGame: 6,
 lateGame: 7,
};

I tried to encode the traditional way of 31*31*N board but it seems to be slow and I am not sure what's the best way to encode metadata / global data inside (player kore)

Output

A simple scalar of size 4 for the action keys as follows:

export const ALL_MOVES: MOVE_NAME[] = [
 MOVE_NAME.DO_NOTHING, // 0
 MOVE_NAME.MINE, // 1
 MOVE_NAME.BUILD_SHIP, // 2
 MOVE_NAME.BUILD_SHIPYARD, // 3
];

Each of these actions lead to a rule-based strategy that tries best effort execute that action based on current board state (a little bit of decision logic inside). I intend to add more actions in the future.

Model architecture

A standard tf.js DQN baseline setup as follows:

______________________________________________________________
Layer (type) Input Shape Output shape Param # 
==============================================================
flatten_Flatten1 (Flatten) [[null,2,8]] [null,16] 0 
______________________________________________________________
dense_Dense1 (Dense) [[null,16]] [null,100] 1700 
______________________________________________________________
dense_Dense2 (Dense) [[null,100]] [null,100] 10100 
______________________________________________________________
dense_Dense3 (Dense) [[null,100]] [null,4] 404 
==============================================================
Total params: 12204
Trainable params: 12204
Non-trainable params: 0

Hyper parameters

const config = {
 replayBufferSize: 10000,
 epsilonInit: 0.4,
 epsilonFinal: 0.01,
 epsilonDecayFrames: 1000000,
 learningRate: 0.0001,
 batchSize: 64,
 startTrainingSize: 64 * 4,
 gamma: 0.95,
 syncEveryFrames: 1000,
};

Reward function

This one is a little bit complicated. I encoded the following into the reward formula, each with a weight factor as parameter that I can tune:

shipcount

shipcount delta

current kore

special reward for losing/winning

penalty for not enough ship

Let me know if you any comments / suggestions on how to improve it. Or share what you have done if you have a different setup.

I also have a series of livestream documenting how I developed the DQN model towards this baseline on YouTube:

https://www.youtube.com/playlist?list=PLjyg49kS3nt-MbwWyl2sSTKgrGN0LEsEr

---

### My Reflections

来源：https://www.kaggle.com/competitions/kore-2022-beta/discussion/317955

I entered this competition because I really wanted Kaggle-branded merchandise and I wanted to touch reinforcement learning as part of my machine learning studies.

Although the duration was short, I really enjoyed the competition and learned a lot, so I would like to share a brief recap!

First, I start to read the staff's notebooks by @bovard for understanding the game rules. I was amazed at how well thought out the game was, a game that could never be played by humans, and with rules that are likely to make agents who can understand the strategy stronger! For example, I think we had to use the fact that the mining rate and the number of orders were different depending on the number of ships, and that when ships collided, both sides were damaged as well, to win.

Next, I tried q-learning, although it did not work this time. This is the first time I've read and implemented reinforcement learning, so there may be some bugs, but I implemented q-learning, kore2022 Q-learning.

After all, I felt that implementing reinforcement learning is really hard and takes a lot of time.

In the end, the top scores were obtained with a few modifications to the example, and the agent created by q-learning did not score well at all.

I would like to work on the production as a team, so I will summarize some ideas that I could not do this time but would like to try.

In discussion, @paradite gave me his idea of using DQN and strategy based RL.

In my code's comment, @wrinkledtime gives me advice on how to increase learning efficiency and speed.

I tried to strategy based agent, but I think I need to fix updating the q-value part. That reason is after the ship returns, the kore number will finally change, so I have to give a reward for some previous step action.

---

### 1st Place Solution

来源：https://www.kaggle.com/competitions/kore-2022-beta/discussion/317737

Ahoy, there!

My solution is a simple rules-based agent which sequentially performs some basic operations:

shipyard defence - We can find out where and when our shipyard will be attacked, and we have time to form a defense. Knowing how many ships are currently in the shipyard and how many my ships will arrive in the near future, I can say exactly what minimum number of additional ships I need to get for a successful defense. If the shipyard has enough spawning capacity and time, then I just create the necessary number of ships in the shipyard. But if that's not enough, then I will send ships from the nearest shipyards to help.

shipyard attack - The same thing, I know the exact number of ships that need to be sent to capture a shipyard. Unfortunately it doesn't always work.

direct attack - I launch a pirate fleet to intercept an enemy fleet, just as simple as that. And of course I choose a route that will not overlap with the routes of enemy fleets.

adjacent attack- It's looks like this: [图 1: 7v4jOCW]. I sacrifice my fleet, but at the same time I create double or even triple damage to the opponent.

expansion - I create new shipyards if I have an surplus of kore, and my current spawning capacity is much less than I can mine.

mining - I look at the huge number of possible routes that are available to me, and choose the one that will give me the largest number of kores per turn. At the same time, I check that a route does not intersect with routes of opponent's fleets. This was very important in 4p games, but I'm not sure how much it's necessary in 2p games.

spawn - I spawn as much as possible until my fleet outnumbers the opponent's fleet by several times.

I can share the code, but I'm not sure if it would be appropriate. Will it harm the upcoming competition? What do you think?

I hope you enjoyed this little competition as much as I did. See you in the next one!

Edit: you can find my code here

---

### Sharing my experience and strategies in building agents in TS/JS

来源：https://www.kaggle.com/competitions/kore-2022-beta/discussion/315970

I started streaming on YouTube a few days ago on my experience building agents in TS/JS. I thought it would be quite interesting to see what I can achieve with an uncommon language.

Apparently I am supposed to share it on discussion to make others aware. So here it goes:

YouTube channel (livestream and past livestreams):

https://www.youtube.com/channel/UC965IqGwTEYCA0SNM4B1UBQ

Playlist specific to Kore 2022 beta:

https://www.youtube.com/watch?v=8gvNS98FsgU&list=PLjyg49kS3nt_ZtnKfawOd9uDERmN0C04U

---

### Welcome to Kore - Beta!

来源：https://www.kaggle.com/competitions/kore-2022-beta/discussion/313582

Hi All,

We're excited to launch Kore 2022 soon, but before we do, we need your help! We're launching Kore in a preview state early to help with gameplay/rule balancing and establishing a fair and fun competition, soon to be launched. As such, this competition does not have cash prizes, points, or medals - but we hope to gain your feedback for when the featured competition goes live! Feel free to posts any bugs you find, or questions/concerns in this thread.

We hope to have this competition up for just a few short weeks so we can polish our configuration and launch the full, featured competition soon thereafter.

---

### Unnatural Fleet + fleet + shipyard collision resolution

来源：https://www.kaggle.com/competitions/kore-2022-beta/discussion/315895

I know the rule says fleet to fleet damage resolves first. But when multiple fleets are attacking the same shipyard, it doesn't feel right.

Checkout this replay turn 231 / 324 top right:

https://www.kaggle.com/competitions/kore-2022-beta/submissions?dialog=episodes-episode-35943182

---
