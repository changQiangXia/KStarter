# lux-ai-season-2-neurips-stage-2

- 类别：Featured ｜ 主题：sim-agent ｜ 子类：— ｜ 领域：游戏
- 截止：2023-11-28 ｜ 队伍数：64 ｜ 机制：标准赛
- 评估指标：lux_ai_s2
- 讨论区：14 条主题

## 讨论区索引（按票数排序）

- 16 票 / 0 评论 | Onboarding materials and references 
  https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/442050
- 5 票 / 1 评论 | Website for submission statistics 
  https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/442372
- 4 票 / 4 评论 | PPO using Jux - Lux AI Season 2 - NeurIPS Stage 2 Competition Solution 「write-up」
  https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/459891
- 3 票 / 3 评论 | Baselines, Dataset, Useful Competition Resources, and Public Code/Bots 
  https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/438939
- 2 票 / 0 评论 | Deadline extended to Monday 
  https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/456054
- 2 票 / 0 评论 | This Competition has an Official Discord Channel 
  https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/442221
- 2 票 / 0 评论 | Welcome to the NeurIPS Edition of Lux AI Season 2! (Stage 2) 
  https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/438940
- 2 票 / 0 评论 | 🔮❓ Who will emerge winners of Lux AI Season 2 - NeurIPS Stage 2?🥇💥 
  https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/457871
- 2 票 / 0 评论 | potential bug with the visualizer 
  https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/449072
- 2 票 / 2 评论 | Is the baseline compatible with State 2 ? 
  https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/445773
- 2 票 / 8 评论 | Does submission working with JUX? 
  https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/444491
- 1 票 / 0 评论 | Tutorial on GPU/Jax environment engine for massive parallelization 
  https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/442048
- 1 票 / 1 评论 | issue with baseline4gym 
  https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/452265
- 1 票 / 0 评论 | Jux (Jax for Lux),  Bidding and Lichens. 
  https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/442242

## write-up 正文（6 篇）

### PPO using Jux - Lux AI Season 2 - NeurIPS Stage 2 Competition Solution

来源：https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/459891

Kaggle competition: Lux AI Season 2 - NeurIPS Stage 2

Kaggle code submission: https://www.kaggle.com/sgoodfriend/lux2-neurips2-ppo-using-jux

Training repo: https://github.com/sgoodfriend/rl-algo-impls. Best submission is from 28e662d.

JUX fork: https://github.com/sgoodfriend/jux. Biggest changes are to support environments not being in lockstep, stats collection, and allowing for adjacent factories (for 16x16 map training).

Weights & Biases report: Lux S2 NeurIPS Training Report

Environment

Jux allows training with vectorized environments using Jax. I used 1024 environments for training on 16x16 and 32x32 maps and 512 environments for training on 64x64 maps. I’m using a fork of Jux for training. The fork has the following changes and extensions:

Fix incorrectly computing valid_spawns_mask. This was broken on 16x16 maps. I'm not certain if it was wrong on competition-size maps.

EnvConfig option to support adjacent factory spawns (default off). I use this for 16x16 map training because the default requirement of 6 spaces away could push factories too far away from resources on such small maps.

Reward -1000 if player lost game for no factories (mimics Lux)

step_unified combines step_factory_placement and step_late_game

Environments don’t need to run in lockstep and can have different numbers of factories to place (externally replace individual envs with new ones when they finish)

Stats collection (generation [resources, bots, kills], resources [lichen, bots, factories], actions)

I convert the Jux observation to a GridNet observation with the following observation features for every position:

[图 1: inbox%2F1298%2F3f878f9ba51a34d536107f98e3d40001%2FScreenshot%202023-12-06%20at%2015.21.57.png]

I take care of computing amounts of resources in my action handling logic. The model only handles position for factory placement while I assign the initial water per factory (150) and enough metal for 1 or 2 heavy units (100 or 200) or 150 if not possible. For example, for 1 to 4 factories to place:

[图 2: inbox%2F1298%2F460d5be764d8e1b750f131673e199c60%2FScreenshot%202023-12-06%20at%2015.22.30.png]

I only allow factories to be placed on tiles that would be adjacent to ice OR ore. I allow factories to be placed adjacent to ore but not ice to help the model learn to mine ore and build robots.

I split direction and resources between the action subtypes, resulting in the following action space per position:

[图 3: inbox%2F1298%2F6d62f2cd4d73d74f74d63e35014268ff%2FScreenshot%202023-12-06%20at%2015.24.01.png]

I heavily used invalid action masking to both eliminate no-op actions (e.g. actions on non-own unit or factory positions, moves or transfers off map or onto opponent factory, or invalid actions because insufficient power or resources) and ill-advised actions:

Don’t water lichen if it would result in water being less than the number of game steps remaining.

Don’t transfer resources off factory tiles.

Exception: Allow transferring power to a unit from a factory tile if the destination unit has been digging.

Cannot pickup resources other than power

Exception: Light robots can pickup water if the factory has sufficient water.

Only allow digging on resources, opponent lichen, and rubble that is adjacent to a factory’s lichen grow area (prevents digging on distant rubble).

Only allow moving in a rectangle containing all resources, diggable areas (see above), own units, and opponent lichen.

Only lights can self-destruct and only if they are on opponent lichen that isn’t eliminable by a single dig action.

The action handling logic will also cancel conflicting actions (instead of attempting to resolve them):

Cancel moves if they are to a stationary own unit, unit to be spawned, or into the destination of another moving own unit. This is done iteratively until no more collisions occur.

Cancel transfers if they aren’t going to a valid target (no unit or factory or unit or factory is at capacity)

Cancel pickups if multiple units are picking up from the same factory and they’d cause the factory to go below 150 water or 0 power.

Neural Architecture

I started with a similar neural architecture to FLG’s DoubleCone, but added an additional 4x-downsampling layer within the original 4x-downsampling layer to get the receptive field to 64x64:

[图 4: inbox%2F1298%2Fd9adf36a478568489a4415f6ddc20e94%2FScreenshot%202023-12-06%20at%2015.24.38.png]

The policy output consists of 24 logits for unit actions, 4 logits for factory actions, and 1 logit for factory placement. Each unit’s action type and subactions are assumed independent and identically distributed, as are the factory actions. The factory placement logit undergoes a softmax transformation across all valid factory spawn positions (all factory spawn positions are masked out if it’s not the agent’s turn to place factories).

PPO Training

Similar to FLG’s Lux AI Season 2 Approach and my 2023 microRTS competition solution, I progressively trained the model on larger maps, starting with 16x16, then 32x32, and finally 64x64. The best performing agent had the following training runs:

Name
Map Size

ppo-LuxAI_S2-v0-j1024env16-80m-lr30-opp-resources-S1-2023-11-16T23:18:33.978764
16x16

ppo-LuxAI_S2-v0-j1024env32-80m-lr20-2building-S1-2023-11-18T09:16:46.921499
32x32

ppo-LuxAI_S2-v0-j512env64-80m-lr5-ft32-2building-S1-2023-11-19T09:30:01.096368
64x64

Each larger map training run was initialized with the weights from the best performing checkpoint of the previous map size. The 16x16 map training run’s weights were initialized randomly.

I used my own implementation of PPO (inspired by Costa Huang's implementation) with the following hyperparameters:

[图 5: inbox%2F1298%2F5e27c6ca82f5622963a15a45abd5f9d8%2FScreenshot%202023-12-06%20at%2015.25.15.png]

Each training run was for 80 million steps with the following schedule for learning rate and entropy coefficient (cosine interpolation during transition phases):

[图 6: inbox%2F1298%2F473071dbcba3ef72fc8882ad6f554b0d%2FScreenshot%202023-12-06%20at%2015.25.45.png]

Training was done on Lambda Cloud GPU instances each with 1 Nvidia A10. I also used Nvidia A100 instances for the larger maps (not these specific training runs) where I could double the mini-batch size. I used PyTorch’s autocast to bfloat16 to reduce memory usage and gradient accumulation to take optimizer steps on the full batch.

While training was scheduled to run 80 million steps, I would stop training early if it looked like progress was stuck. This let me schedule different training runs with limited resources.

Reward structure

RL solutions from the prior Lux Season 2 competition had to start training with shaped rewards. Similar to my prior solution, I used generation and resource statistics to generate the reward. However, instead of determining the scaling factors myself, I scaled each statistic by dividing each statistic by its exponential moving standard deviation (window size 5 million steps). The environment would return all of these scaled statistics and a WinLoss reward (+1 win, -1 loss, 0 otherwise), and the rollout computes an advantage for each statistic. The PPO implementation has element-wise scaling factors for each advantage and reward for computing policy and value losses:

[图 7: inbox%2F1298%2F3c651a4b1df678206a17ab30c990e397%2FScreenshot%202023-12-06%20at%2015.26.15.png]

The advantage of the above was that I could keep the same model and simply change the weights in the value and reward coefficients to adjust the strategy. For example, the training runs for 32x32 and 64x64 maps rewarded building robots more by increasing the reward weights for ore, metal, and robot generation.

Training Results

Reaches End of Game

[图 8: inbox%2F1298%2F77e3e145ef3c9ba11df7c25b67abdb6a%2Freach_game_end.png]

The chart above shows the rate of games that reach the step limit. The 16x16 agent (light green) averages about 600 steps/game by the end of training. Even though I require maps to have at least 2 ice and ore each, later agents I’ve trained rarely reach over 900 steps/game, implying the small map with competitive resources is a difficult environment to reliably reach the step limit. The 32x32 (magenta) and 64x64 agents (blue) get to the step limit regularly.

Metal Generation

[图 9: inbox%2F1298%2Fb02290583ed05522c03042211847f189%2Fmetal_generation.png]

The chart above shows average metal generation per game. The dashed lines represents evaluations that on average beat the prior 4 best evaluation checkpoints (cumulative win-rate of at least 57% in 128 games [64 games for 64x64]). Notice that the last dashed line for 64x64 is before 20 million steps. 32x32 does continue to make models that beat prior checkpoints (dashed line continues to 60 million steps), but metal generation falls below 100 (the cost of a heavy robot). All of this implies training stopped being useful before the end.

KL Divergence and Loss

[图 10: inbox%2F1298%2Fc64ab76fd68a7a92d2cc3ab7345c0237%2Flosses.png]

The charts above shows the KL divergence and training loss. 3 things jump out at me:

KL divergence for 32x32 is too high (over 0.02), especially after 30 million steps. This is around when metal generation drops below 100.

Losses are periodically spiky for 64x64 (and to a lesser extent 32x32). This is likely caused by training games ending at the same time every 1000 steps.

The variability of KL divergence means a constant learning rate is not ideal. Training reaches milestones that changes game dynamics. For example, the 16x16 spike at 25 million steps coincides with games beginning to reach the step limit a sizable portion of the time. A constant learning rate means a training agent can easily be training too slowly or too quickly in the same training run depending on how much game dynamics are changing.

Next steps

I spent a lot of time creating a GridNet observation space from Jux using Jax. I believe there are a few things I could do to improve the model:

Fix the periodic spikes in losses by doing a rolling reset of environments at the beginning of training.

Track L2 gradient norm to gauge training stability. Loss, value loss, policy loss, KL divergence, and entropy loss are all important, but I noticed that I could end up in situations where everything would be stable until a sudden spike. Rising gradient norm is one possible indicator that training is becoming unstable even if other metrics show little change.

Use a learning rate schedule that takes into account the changing game dynamics. I’m currently working on raising and lowering learning rate depending on the KL divergence. This is tricky because KL divergence isn’t the only indicator of instability. Currently, if the L2 gradient norm is above a cutoff, learning rate isn’t increased. This has been very finicky so this will either be supplemented with or abandoned for the next item.

Normalization layers. FLG’s solution called out that normalization layers didn’t appear necessary given the use of Squeeze-and-Excitation layers, but did mention LayerNorm could be useful if there wasn’t Squeeze-and-Excitation layers. Given my convergence issues, I’m trying out adding LayerNorm after fully connected layers and a spatial dimension-independent ChannelLayerNorm2d after convolutional layers. So far this has helped with stability at the cost of training memory and performance.

Appendix

Environment hyperparameters:

[图 11: inbox%2F1298%2F227bc5e2f75df25b8cb4ca3de6bc66f4%2FScreenshot%202023-12-06%20at%2015.26.55.png]

---

### Onboarding materials and references

来源：https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/442050

Hello all,

Wishing you all the best for the challenge! Hope the below artefacts help one and all onboard effectively- 

Lux AI Season 2

Kernels

https://www.kaggle.com/code/stonet2000/lux-ai-challenge-season-2-tutorial-python -- tuturial from the host

https://www.kaggle.com/code/stonet2000/rl-with-lux-2-rl-problem-solving -- another good kernel from the host

https://www.kaggle.com/code/stonet2000/rl-with-lux-1-intro-to-rl -- beginner friendly RL kernel from the host

https://www.kaggle.com/code/scakcotf/building-a-basic-rule-based-agent-in-python -- good kernel with a rule based framework

https://www.kaggle.com/code/istinetz/picking-a-good-starting-location -- helps one understand the tenets of picking up a good location to start in the RL process

High scoring approaches

https://www.kaggle.com/competitions/lux-ai-season-2/discussion/407982 -- rank 1 approach

https://www.kaggle.com/competitions/lux-ai-season-2/discussion/405476 -- rank 2 approach

https://www.kaggle.com/competitions/lux-ai-season-2/discussion/404921 -- rank 3 approach

https://www.kaggle.com/competitions/lux-ai-season-2/discussion/406702 -- rank 4 approach

https://www.kaggle.com/competitions/lux-ai-season-2/discussion/405245 -- rank 6 approach

https://www.kaggle.com/competitions/lux-ai-season-2/discussion/411725 -- rank 10 approach

Other popular discussions

https://www.kaggle.com/competitions/lux-ai-season-2/discussion/404921

https://www.kaggle.com/competitions/lux-ai-season-2/discussion/381185 

https://www.kaggle.com/competitions/lux-ai-season-2/discussion/404842 -- highlights notes from the imitation solution approach

Lux AI 2021

Kernels

https://www.kaggle.com/code/huikang/lux-ai-working-title-bot -- most popular kernel in the series

https://www.kaggle.com/code/shoheiazuma/lux-ai-with-imitation-learning -- uses a novel approach of imitation learning to extremely good effect

https://www.kaggle.com/code/stonet2000/lux-ai-season-1-jupyter-notebook-tutorial -- excellent tutorial to use kaggle-environments to excellent effect

https://www.kaggle.com/code/aithammadiabdellatif/lux-ai-reinforcement-learning -- engenders a very effective approach using Q-learning

https://www.kaggle.com/code/glmcdona/reinforcement-learning-openai-ppo-with-python-game -- uses reinforcement learning to excellent effect to engender a great approach to the assignment

High scoring approaches

https://www.kaggle.com/competitions/lux-ai-2021/discussion/300844 -- rank 2 approach

https://www.kaggle.com/competitions/lux-ai-2021/discussion/296938 -- rank 4 approach

https://www.kaggle.com/competitions/lux-ai-2021/discussion/296306 -- rank 11 approach

https://www.kaggle.com/competitions/lux-ai-2021/discussion/296406 -- rank 12 approach

Kore 2022 kernels

https://www.kaggle.com/competitions/kore-2022/discussion/340035 -- winning approach

https://www.kaggle.com/competitions/kore-2022/discussion/340994 -- 2nd place approach

https://www.kaggle.com/competitions/kore-2022/discussion/342296 -- 3rd place approach

https://www.kaggle.com/competitions/kore-2022/discussion/340157 -- 4th place approach

https://www.kaggle.com/code/lesamu/reinforcement-learning-baseline-in-python -- very good usage of reinforcement learning for the assignment

Hungry geese

https://www.kaggle.com/competitions/hungry-geese/discussion/263686 -- 2nd place approach

https://www.kaggle.com/competitions/hungry-geese/discussion/263735 -- 3rd place approach

https://www.kaggle.com/competitions/hungry-geese/discussion/263690 -- 4th place approach

https://www.kaggle.com/competitions/hungry-geese/discussion/263702 -- 5th place approach

https://www.kaggle.com/code/ihelon/hungry-geese-agents-comparison -- most popular kernel of the assignment

All the best and happy learning!!

---

### Baselines, Dataset, Useful Competition Resources, and Public Code/Bots

来源：https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/438939

There's a wealth of knowledge thanks to the previous Season 2 competition in addition to some open-sourced baselines we provide.

To get started with research into multi-agent RL, collaborators at Parametrix.ai have provided a flexible baseline utilizing a popular on-policy algorithm called PPO here: https://github.com/RoboEden/Luxai-s2-Baseline. Check out the code to see how to get started with it and modify it for your needs. Moreover, this repository has instructions for how to download past episodes from the previous season that can be used for kickstarting your agent learning.

This post compiles a list of helpful resources for getting started competing as well as learning how the top reinforcement learning, rule-based, etc. solutions were done, some of which come with code!

Reinforcement Learning

4th Placed Solution: https://www.kaggle.com/competitions/lux-ai-season-2/discussion/406702

10th Placed Solution: https://www.kaggle.com/competitions/lux-ai-season-2/discussion/411725

Imitation Learning

31st Placed Solution (which imitates the 10th placed solution): https://www.kaggle.com/competitions/lux-ai-season-2/discussion/404842

Rule Based

1st Placed Solution: https://www.kaggle.com/competitions/lux-ai-season-2/discussion/407982

2nd Placed Solution: https://www.kaggle.com/competitions/lux-ai-season-2/discussion/405476

3rd Placed Solution: https://www.kaggle.com/competitions/lux-ai-season-2/discussion/404921

5th Placed Solution: https://www.kaggle.com/competitions/lux-ai-season-2/discussion/409394

6th Placed Solution: https://www.kaggle.com/competitions/lux-ai-season-2/discussion/405245

15th Placed Solution (Code Open Sourced): https://www.kaggle.com/competitions/lux-ai-season-2/discussion/407723; Code

Tutorials / Open Source

RL for Lux AI Season 2 Tutorial. Practical approach to simplifying a complex game for RL: https://www.kaggle.com/code/stonet2000/rl-with-lux-2-rl-problem-solving

Open Sourced, simple, self-play RL agent: https://www.kaggle.com/competitions/lux-ai-season-2/discussion/406791

Another Open Sourced RL agent: https://www.kaggle.com/competitions/lux-ai-season-2/discussion/404809

Popular open sourced code/notebooks for season 2, covering tutorials on RL, the game itself, and some neat strategies to boost performance: https://www.kaggle.com/competitions/lux-ai-season-2/code?competitionId=45040&sortBy=voteCount

---

### Website for submission statistics

来源：https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/442372

Hi all

During season 2 some of the participants found useful our statistics site, so I'll try to host it this season too

Check it here

http://luxaistats.crabdance.com/ (more powerful VM now, so I hope it won't crash that often this time 🙂)

https://github.com/nikiandr/lux_ai_stats - DYI edition: code and deployment tutorial

Although it isn't actively developed, I'll try to keep it alive as much as I can.

If you see that something does not work, or any help is needed - feel free to contact me through Kaggle email!

This is a simple app based on submission page scrapping and visualization using plotly & streamlit. As the last time, features include plots of score growth, score change, win rate changes, and a win/loss match count.

All you need to do - is enter a submission id, which can be found in the dialog window. E.g. 33605309 here https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/leaderboard?dialog=episodes-submission-33605309

[图 1: inbox%2F6430020%2F8c0a2dc993a6e6c1d382820b908b5316%2FUnsaved%20Image%201.png]

---

### This Competition has an Official Discord Channel

来源：https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/442221

In addition to this competition forum, you can continue the discussion in our official Kaggle Discord Server here: discord.gg/kaggle

The Discord is a great place to ask getting started questions, chat about the nuances of this competition, and connect with potential team mates. Learn more about Discord at our announcement here. Here are a few things to keep in mind though:

Discord Competition Channels are 'Public'

Discord channels for specific competitions are considered 'public' spaces where you are allowed to talk about competition details (it will not count as private sharing).

Discord Competition Channels are Not Monitored by Staff

Kaggle Staff and Hosts running competitions will not monitor Discord or be available to answer questions in Discord. Always post important questions in the forums.

Keep the Good Stuff on the Forums

Please keep important questions, insights, writeups, and other valuable conversation on the Kaggle forums. Discord is intended to be a more casual space to discuss competitions and help each other, we want to keep all the best information on the forums.

Remember to never privately share competition code or data

Please remember that private sharing of competition code or data is, as always, not permitted. Code sharing must always be done publicly through the Kaggle forums/notebooks.

I hope you’ll join us to chat on Discord soon!

---

### Deadline extended to Monday

来源：https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/456054

Due to some episode failures we are extended the deadline to Monday! Best of luck!

---
