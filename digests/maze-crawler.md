# maze-crawler

- 类别：Playground ｜ 主题：sim-agent ｜ 子类：— ｜ 领域：游戏
- 截止：2026-06-30 ｜ 队伍数：459 ｜ 机制：标准赛
- 评估指标：crawl
- 讨论区：23 条主题

## 讨论区索引（按票数排序）

- 11 票 / 4 评论 | Maze Crawler - 1st Place Solution Writeup 「write-up」
  https://www.kaggle.com/competitions/maze-crawler/discussion/717120
- 9 票 / 2 评论 | [SOLVED] Great competition, but no medals or points? 
  https://www.kaggle.com/competitions/maze-crawler/discussion/696453
- 5 票 / 0 评论 | How to Get Started + Competition's Official Discord 
  https://www.kaggle.com/competitions/maze-crawler/discussion/696210
- 4 票 / 0 评论 | Daily Episodes Datasets 
  https://www.kaggle.com/competitions/maze-crawler/discussion/701822
- 3 票 / 0 评论 | 7th Place: Global Task Optimization (Hungarian Matcher) + Time-A 「write-up」
  https://www.kaggle.com/competitions/maze-crawler/discussion/717177
- 3 票 / 0 评论 | [Sharing] Jump-Preferred BFS (LB 1223) 
  https://www.kaggle.com/competitions/maze-crawler/discussion/702108
- 2 票 / 4 评论 | 5th (Correction: now 7th) Place: A Rules-Based Bot Without Much Search 
  https://www.kaggle.com/competitions/maze-crawler/discussion/708834
- 1 票 / 0 评论 | Evaluation Period has started 
  https://www.kaggle.com/competitions/maze-crawler/discussion/708878
- 1 票 / 7 评论 | Competition Updates 
  https://www.kaggle.com/competitions/maze-crawler/discussion/701583
- 1 票 / 0 评论 | # Maze Crawler 3rd Place Solution Writeup 「write-up」
  https://www.kaggle.com/competitions/maze-crawler/discussion/718158
- 1 票 / 4 评论 | [SOLVED]Strange tiebreak 
  https://www.kaggle.com/competitions/maze-crawler/discussion/702770
- 1 票 / 0 评论 | Possible improvements for opponent allocation 
  https://www.kaggle.com/competitions/maze-crawler/discussion/696486
- 0 票 / 0 评论 | late submissions possible? 
  https://www.kaggle.com/competitions/maze-crawler/discussion/714492
- 0 票 / 0 评论 | Is random seed guessable? 
  https://www.kaggle.com/competitions/maze-crawler/discussion/709692
- 0 票 / 1 评论 | [BUG] - Cannot replicate kaggle game history 
  https://www.kaggle.com/competitions/maze-crawler/discussion/703207
- 0 票 / 0 评论 | Meta-lessons from two weeks of grinding Maze Crawler (no recipe inside, just stuff I wish I knew earlier) 
  https://www.kaggle.com/competitions/maze-crawler/discussion/704125
- 0 票 / 1 评论 | spawn North 
  https://www.kaggle.com/competitions/maze-crawler/discussion/704068
- 0 票 / 3 评论 | [SOLVED] Currently local environment doesn't match environment on kaggle, so its impossible to test agents 
  https://www.kaggle.com/competitions/maze-crawler/discussion/701737
- 0 票 / 0 评论 | [SOLVED] Scrolling is way to fast[CONCRETE PROOF] 
  https://www.kaggle.com/competitions/maze-crawler/discussion/701748
- 0 票 / 7 评论 | [SOLVED] DONT COMPETE HERE!!! CURENTLY THE GAME IS ULTRA BUGGED!!! 
  https://www.kaggle.com/competitions/maze-crawler/discussion/700980
- 0 票 / 4 评论 | [SOLVED] Factory as fast as scout, also mines dont seem to spawn[ON CALL NEEDED] 
  https://www.kaggle.com/competitions/maze-crawler/discussion/700638
- 0 票 / 1 评论 | How does the competition related to machine learning 
  https://www.kaggle.com/competitions/maze-crawler/discussion/696838
- -5 票 / 3 评论 | AI might take our jobs[discussion] 
  https://www.kaggle.com/competitions/maze-crawler/discussion/701887

## write-up 正文（6 篇）

### Maze Crawler - 1st Place Solution Writeup

来源：https://www.kaggle.com/competitions/maze-crawler/discussion/717120

First, thanks to the organizers for a genuinely fun environment, and to everyone who competed. Below is the full breakdown of how the agent thinks, in the order the pieces build on each other.

Main keys of the solution

Three layers, each on top of the previous:

Movement - a first-move BFS that scores every reachable cell and takes the best. Behavior is steered entirely through the score formula.

Economy (the "standard" top approach) - head to mining nodes (node > bfs), and switch to a worker for survival when sbd gets low.

Combat win condition (the reason it won) - win the factory-collision energy tiebreak. This is the part that beats the many top solutions that just farm energy and wait to win the tiebreak after step 500.

1. The Movement Module

The core is a breadth-first search from the factory that expands over the known map and records, for every reachable cell, the first move needed to start heading there.

Two things make it more than a plain BFS:

(a) Jump-aware expansion. The BFS explores both walking edges and jump edges. When two paths reach the same cell - one with a jump and one without - I keep whichever has the better score, not blindly the shorter one. Each cell_best entry is (arrival_ticks, jump_cd_at_arrival, first_move, jumped_flag), so later logic knows whether a route needed a jump.

(b) Score-driven selection. After the BFS fills cell_best, I score every candidate cell and take the max. The dominant term is sbd (steps-before-death - how many ticks until the scroll boundary reaches that row), evaluated at the arrival tick, not the current one:

def _pick_action(cell_best, tbl, wm, fc, fr, width, south, north, spawn_col=None, crossed=False, enemy_col=None):
 best_score = None; best_action = None
 for (c, r), (ticks, jcd, first, jumped) in cell_best.items():
 if r < fr: # only consider cells at or above the factory
 continue
 sc = _score_cell(tbl, wm, c, r, ticks, jcd, width, south, north, spawn_col if not crossed else None)
 if enemy_col is not None:
 sc += max(0, 3 - abs(c - enemy_col)) * ENEMY_COL_BONUS
 if best_score is None or sc > best_score:
 best_score = sc; best_action = first
 return best_action, ...

The key idea: movement is entirely a function of the score formula, so I can shape behavior just by adding terms. The very same BFS is reused for exploration, for approaching a node, and for closing on the enemy - only the scoring changes. That reuse is what lets the combat and economy layers plug in cleanly later.

Basic movement terms:

Edge penalty (EDGE_PENALTY, EDGE_COLS) - the outer columns are traps; you get pinned against the wall as the map scrolls. Penalizing them keeps the factory in the safer central corridor.

One-time crossing bonus (CROSS_BONUS) - the map is left/right symmetric and both players start on opposite halves, so the enemy is obviously on their side. A one-shot bonus pushes the factory to cross into the opposite half, then switches off once crossed.

2. The Economy - the "standard" top approach (node mine + worker)

The second ingredient is the one most strong solutions share: energy economy, with a strict priority - node > bfs.

When a reachable mining node is visible and still safe on arrival (sbd above a threshold), the factory drops exploration and goes to it. It builds a miner, the miner TRANSFORMs into a mine, and the factory sits on the mine to farm energy - energy that later wins tiebreaks.

As the scroll catches up and sbd gets small, the agent switches to worker mode for survival: the worker clears walls to the north so the factory can keep escaping the scroll where plain BFS would be stuck.

Gated by a few tunables so it's easy to rebalance:

MINER_PHASE_END = 350 # after this step, stop starting new mining
MIN_NODE_SBD = 30 # only commit to a node if it's this safe on arrival
ENERGY_CAP = 3000 # once banked, permanently stop farming and hunt instead
WORKER_PHASE_START = 400 # only build the survival worker this late

ENERGY_CAP is a one-shot latch. Once total energy crosses it, the agent permanently stops caring about nodes and commits to finding the enemy — resources are already sufficient to win the tiebreak, so from that point time is better spent hunting than farming.

[图 1: inbox%2F32104791%2F8a3953a10667d8efde91ce6df727512c%2F2026-07-01_16-58-29.png]

Figure 1 - The factory sits on a mine (a miner transformed into a mine), farming energy that will later decide the tiebreak.

3. Combat - the win condition that actually won

This is the part I believe made the difference. The match ends when the two factories collide (or one is scrolled out), and a factory-vs-factory collision is decided by total energy of surviving robots.

Most strong solutions treat this as: farm as much energy as possible, then win the tiebreak once the game runs long (past step ~500). My agent instead treats combat as an active objective - it seeks the collision on its own terms with an energy edge, rather than passively waiting. That's why it beats pure energy-farmers: it doesn't let the game drift to a neutral late-game tiebreak; it forces a favorable one.

The whole thing reduces to two subgoals: find the enemy, and have more energy at the moment of collision.

3.1 Finding the enemy

(1) Score manipulation. Beyond the edge penalty, an enemy-column bonus biases motion toward where the enemy likely is:

# added in _pick_action when the enemy is known but not directly chaseable:
sc += max(0, 3 - abs(c - enemy_col)) * ENEMY_COL_BONUS

It applies when the enemy is seen but unreachable in BFS, or was last seen and then lost, so the factory drifts toward the enemy's column and closes in as the map opens. The bonus zeroes out once the factory reaches that column, so it never gets glued to a stale column.

(2) Path-capture priority. When the enemy is actually reachable, target selection is strict:

enemy > node > normal BFS

If the enemy appears in the BFS while the factory is en route to a node, it drops the node and switches to the enemy.

(3) Scouts. Cheap eyes (SCOUT_COST = 50). They spawn right after the factory jumps - a jump usually clears a dead end, and the factory pauses on the gap tick, so it's a free moment to spawn a scout that can explore onward. Scouts are tuned to fan out and cross into the half opposite their own spawn, maximizing coverage. Each scout is also a bundle of energy that adds to the tiebreak total.

[图 2: inbox%2F32104791%2Fea5b489753edfccbbd874b83de259bbd%2F2026-07-01_16-58-58.png]

Figure 2 - Scouts fanning out across both halves of the map, maximizing vision coverage while each adds energy to the tiebreak total.

3.2 Winning the tiebreak - the early miner drop

The miner is the biggest energy unit (300 energy), so dropping a miner next to the factory just before a collision is the single strongest tiebreak swing. The whole trick is timing.

TIEBREAK_DIST = 5 # build the tiebreak miner when the enemy is within this manhattan distance
TIEBREAK_ENERGY_MARGIN = 50 # keep this much spare after paying MINER_COST
# fires if: enemy visible, within TIEBREAK_DIST, build cd ready, and no live miner already counts

Two refinements made it reliable:

Placement behind the advance - the miner drops on the cell the factory just left (OPPOSITE[last_move_dir]), so as the factory pushes toward the enemy it never runs over its own miner. If that cell is blocked, fallback directions are sorted away from the enemy.

Lookahead death prediction - a miner that will be scrolled out within the next 1–2 ticks is treated as already dead, so the replacement is built early. This dodges the worst case: the miner dying and the factory colliding on the same tick, which would lose the tiebreak.

TIEBREAK_MINER_LOOKAHEAD = 2 # treat a soon-to-be-scrolled miner as already dead

[图 3: inbox%2F32104791%2Fce302c9691517519d78b474ddef2ca3b%2F2026-07-01_17-02-19.png]

Figure 3 - The factory drops a tiebreak miner on the cell behind it just before closing on the enemy.

[图 4: inbox%2F32104791%2F625da0c91184d6a841b72e8fdf9e8cd0%2F2026-07-01_17-01-55.png]

Figure 4 - The moment of the factory collision, with the freshly dropped miner's 300 energy counted on my side of the tiebreak.

4. Collision avoidance between my own units

Small but genuinely valuable: my own units don't crush each other. The factory outranks scouts and miners, so a naive step would delete a friendly unit.

Scouts reserve their next cells (planned_moves) and never walk into each other or the factory's next cell.

When the factory would step onto its own miner, they swap: the miner steps OPPOSITE, the factory takes its place.

Engine subtlety: a freshly built miner has a move cooldown and can't vacate on its first tick - so the factory waits one tick instead of crushing it.

def _swap_with_miner(actions, obs, player, factory_uid, fc, fr):
 a = actions.get(factory_uid)
 if not a or a not in OFFSETS: return
 dc, dr = OFFSETS[a]; tc, tr = fc + dc, fr + dr
 for uid2, d2 in obs.robots.items():
 if d2[4] == player and d2[0] == MINER_TYPE and d2[1] == tc and d2[2] == tr:
 if d2[5] > 0: # miner still on move cooldown -> can't move yet
 actions[factory_uid] = "IDLE" # wait instead of crushing it
 elif uid2 not in actions:
 actions[uid2] = OPPOSITE[a] # swap places
 break

5. The near-mirror match: rival bunterrrr

Here's the honest part of the story. I designed every feature to beat the standard energy-farming solutions as hard as possible — targeting ~95% win rate against them. I did not expect anyone to build essentially the same idea, so I never tuned for a symmetric match, or for evenness against a copy of myself.

Then bunterrrr showed up with a very similar approach - same combat-first, miner-drop core - but without scouts and without node mining. Against a near-mirror, two of my choices actually cost me games:

Their miner drop was later than mine. A mine loses 1 energy per tick, so an early drop bleeds value over the run-up to the collision. Because bunterrrr dropped later, in some head-to-heads their miner simply carried more energy at impact and won the tiebreak.

I had removed "leave the mine when the enemy is visible." I removed it after seeing games where the factory couldn't free up build_cd for a fresh miner in time (it had just placed one), so I disabled leaving the mine to avoid that failure - but I should have kept it. Against bunterrrr that rigidity occasionally handed them the initiative.

So against the standard field my agent dominated as intended, but against its own near-twin the match was close to 50/50 - I'd estimate something like 53/47 in my favor, though I didn't count exact games. It's genuinely hard to be sure, because per-game rating changes never settled to ±1: they were always around ±5, and asymmetric with the rating gap (e.g. when I was rated higher, a loss cost me −5 while costing the lower-rated player only −4). With two nearly equal players, that kind of update is slow to converge. My final rating ended up slightly higher, so on balance I think I won a little more often - but it was close.

[图 5: inbox%2F32104791%2F8a02b864a300547df24f4cd4993d3bbf%2F2026-07-01_16-59-25.png]

Figure 5 - Final ratings: my agent and bunterrrr ended up nearly tied, with my rating slightly ahead.

6. Tunability as a design philosophy

Because every behavior is either a score term or a named threshold, the whole agent is a flat block of tunable constants - rebalancing never meant rewriting logic, just changing numbers:

ENEMY_LOGIC_START = 35 # first ticks: pure exploration, no combat logic yet
TIEBREAK_DIST = 5
CHASE_BUILD_MARGIN = 2 # only pursue if there's time to place the tiebreak miner en route
ENEMY_LOW_SBD_WALK = 12 # enemy too low to chase (safe, if reachable on foot)
ENEMY_LOW_SBD_JUMP = 23 # enemy too low to chase (jumping down is riskier -> higher bar)
CROSS_BONUS = 40.0
ENEMY_COL_BONUS = 15.0

Example of that philosophy: I don't dive after an enemy that's about to be scrolled out anyway - but walking down is safer than jumping down, so the "too low to chase" bar is lower on foot (12) and higher when only a jump reaches it (23).

Other micro-details: the early game (step < ENEMY_LOGIC_START) is pure exploration to build map knowledge first; the map's left/right symmetry is used to predict walls on never-seen cells (prediction only - observed truth is never overwritten, avoiding phantom walls at the door exceptions); and every spawn path has a bounded wait + reset so the factory never idles to death on a failed build.

Closing

The agent is deliberately simple: one scored BFS, a standard node-mine + worker economy, and a combat-first win condition with a well-timed miner drop. No learning - all the strength came from making the score function express the right incentives and from treating the energy tiebreak as something to force, not wait for. The one thing I'd change is tuning for the near-mirror case against bunterrrr rather than only for crushing the standard field.

A personal note: this is easily the most significant thing I've competed for (even without any prizes😭🙏🙏), and being in contention for first - even in a relatively small competition by Kaggle's standards - kept me on edge the whole way through. I literally left Kaggle for eval period to be away from checking leaderboard and be worried. I'm genuinely relieved it's finally over. Thanks for reading, and thanks to everyone who made the run worth it.

---

### # Maze Crawler 3rd Place Solution Writeup

来源：https://www.kaggle.com/competitions/maze-crawler/discussion/718158

This was a really fun competition, and I mostly used it as a chance to try out Genematon's
experimental RL features, which aren't generally available yet. Genematon did the machine
learning: the behavioral-cloning bootstrap, the reward, the PPO training, and the self-play,
all from a problem we set up for it. We supplied the behavioral-cloning data, drawn from the
daily datasets posted to Kaggle, and wrote a fast JAX port of the environment with the help
of LLMs. Large-scale RL needs a quick simulator, and generating that environment isn't
something Genematon does yet (though we expect it to before long). Everything that follows is
my own analysis and summary of what the system did.
The submission is a neural-network policy trained with self-play reinforcement learning.
Rather than hand-coding a strategy, the agent learned one from a very large number of games.

Overview

The pipeline had three broad stages:

A fast simulator. A heavily optimized JAX port of the environment, allowing an
enormous number of games to be run cheaply. Fast simulation is the foundation everything
else rests on; it's what made large-scale RL and thorough evaluation practical.

A learned starting point. An initial policy was bootstrapped by imitating strong
existing play, giving the reinforcement-learning stage a competent place to begin instead
of starting from scratch.

Self-play reinforcement learning. From there the policy was trained with PPO, first to
reliably survive and then to win in head-to-head play, improving across successive
generations of self-play.

Model

The policy is a small neural network that combines a convolutional view of the board with a
separate pathway for non-spatial game state, so both the spatial layout and the scalar
information (things like resources, timers, and counts) are used effectively. The model was
kept deliberately small and fast.

Reward

The reward is intentionally minimal. The objective the agent optimizes is winning; the
main signal is the game outcome. On top of that, a small, dense shaping term tied to in-game
energy is added, purely to make learning tractable: a single win/loss signal per long game
gives very little to learn from, so a light, well-behaved shaping term helps the agent
improve steadily between outcomes without changing what "optimal" means.
The most important lesson here was to keep the reward simple and to make sure it matches the
game's actual win condition exactly. Getting the win logic precisely right mattered more
than adding extra reward terms; several of the reward "improvements" were really just
removals of terms that pulled the agent in the wrong direction.

Self-play

The agent was improved through repeated self-play against past versions of itself, with the
strongest checkpoints kept and used to train the next generation. Careful, large-sample
evaluation was essential. Small evaluations were far too noisy to trust, and an improvement
was only believed once it held up over many games.
The end result was an agent that plays a very strong energy game: it survives almost every
match and banks energy up to the practical ceiling the map allows.

What I believe could be done differently

The agent became excellent at the energy side of the game but comparatively weak at direct
combat. I think that's because the self-play pool was fairly homogeneous, so the training
loop never forced the agent to become a strong fighter; energy play was enough to win
against its own lineage. Against the field, the top solutions exploited exactly that gap. If
I did this again, I'd deliberately train adversarial opponents whose job is to attack the
agent's blind spots, the approach used in AlphaStar, so a single dominant strategy couldn't
quietly take over the whole population.

---

### How to Get Started + Competition's Official Discord

来源：https://www.kaggle.com/competitions/maze-crawler/discussion/696210

Information for First Timers

New to machine learning and data science? No question is too basic or too simple. Feel free to start your own thread, or use this thread as a place to post any first-timer clarifying questions for the Kaggle community to help you with!

New to Kaggle? Take a look at a few videos to learn a bit more about site etiquette, Kaggle lingo, and how to enter a competition using Kaggle Notebooks. Publish and share your models on Kaggle Models!

Looking for a Team? Express your interest in joining a team through our Team Up feature.

Remember: Kaggle is for everyone. Whether you're teaming up or sharing tips in the competition forum, we expect everyone to follow our Kaggle community guidelines.

Competition's Official Discord

In addition to this competition forum, you can continue the discussion in our official Kaggle Discord Server here:

discord.gg/kaggle

The Discord is a great place to ask getting started questions, chat about the nuances of this competition, and connect with potential team mates. Learn more about Discord at our announcement here. Here are a few things to keep in mind though:

1. Discord Competition Channels are 'Public' - Don't Share Private Information

Discord channels for specific competitions are considered 'public' spaces where you are allowed to talk about competition details. Please remember that private sharing of competition code or data outside of your team is, as always, not permitted. Code sharing must always be done publicly through the Kaggle forums/notebooks.

2. Discord Competition Channels are Not Monitored by Staff - Keep Important Information on the Kaggle Forums

Kaggle Staff and Hosts running competitions will not monitor Discord or be available to answer questions in Discord. This is intended to be a more casual space to discuss competitions and help each other. Please keep important questions, insights, writeups, and other valuable conversation on the Kaggle forums. 

Happy modeling!

---

### 7th Place: Global Task Optimization (Hungarian Matcher) + Time-A

来源：https://www.kaggle.com/competitions/maze-crawler/discussion/717177

This approach focuses on coordinating units globally and managing pathfinding efficiently to handle the game's constraints without overcomplicating the logic.

Map Symmetry Exploration

Because the maze is symmetrical from East to West, visibility on one side reveals the layout of the opposite side. When a section is obscured by fog, the known layout from the mirrored side is used to fill in the blanks, reducing the need for physical exploration.

Task Coordination

To prevent units from crowding around the same resources, objectives like crystals, mining nodes, breaches, and trains are evaluated globally. Every unit receives a single, distinct target based on proximity and suitability, ensuring efficient distribution across the map.

Movement and Collision Avoidance

Path planning accounts for both special abilities and timing to ensure smooth navigation:

Jump Mechanics: Navigation planning tracks the cooldown of the Factory's jump ability, charting paths directly over walls whenever the ability is available.

Time-Step Reservations: Units plan their routes sequentially based on priority. When a unit charts a path, it reserves specific tiles for the exact future turns it will occupy them. Lower-priority units then treat those tiles as temporarily blocked on those specific turns, preventing collisions.

Traffic Management and End-Game Adjustment

Corridor Clearance: Units identify narrow pathways. If a low-priority or idle unit is blocking a bottleneck, it shifts into an adjacent row to keep the main path clear for active units.

Forced Progression: When entirely blocked in tight spaces, the Factory utilizes the mechanism that allows larger units to crush smaller teammates, prioritizing forward momentum over saving low-tier units.

Late-Game Retreat: As the match nears its end and the map's upward scroll accelerates, resource collection is abandoned. Remaining units align and move directly North to stay ahead of the elimination wall.

---

### [SOLVED] Great competition, but no medals or points?

来源：https://www.kaggle.com/competitions/maze-crawler/discussion/696453

I took on this competition with huge enthusiasm. I think it's fantastic.

But when I noticed there are no medals or ranking points awarded, my enthusiasm 
dropped significantly. The absence of points and medals though, in my view, will significantly lower the quality of competition.

Is there any chance this could be changed?

---

### Daily Episodes Datasets

来源：https://www.kaggle.com/competitions/maze-crawler/discussion/701822

I've started the export of daily episodes. It'll take a few hours to catch up, but once it is you can find a link to all the days here:

https://www.kaggle.com/datasets/kaggle/maze-crawler-episodes-index

---
