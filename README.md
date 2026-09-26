# Worldtick

[![check](https://github.com/shaneraphel/aletheia-worldtick/actions/workflows/check.yml/badge.svg)](https://github.com/shaneraphel/aletheia-worldtick/actions/workflows/check.yml)

世界模型要交回下一帧，脑电解码要交回“动了还是没动”，灵巧手的画面要交回一只已经摆好的手。有一块没测到的时候，常见做法是先填一个能接着用的值，后面的程序就把它当成测到的。这个仓库挡在那一步前面：只按已经到的信息继续；什么都没送来，就停住，不交回一个看起来像测量结果的零。

A world model is asked for the next frame, a brain decoder is asked whether the person moved, and a picture of a dexterous hand is asked for a pose that has already happened. When part of the input never arrived, the usual next step writes in a usable value, and the program after that treats the value as a measurement. This repository sits in front of that step. It continues only from what arrived. When nothing arrived, it stops, and it does not hand back a zero that looks like a measurement.

可以打开的页面：[shaneraphel.github.io/aletheia-worldtick](https://shaneraphel.github.io/aletheia-worldtick/)。

## 怎么读

按这个顺序。页面是可以交给别人试的东西。这份说明讲它为什么长这样。证明、和每篇论文的对照、全部计数，都在 [`paper/paper.md`](paper/paper.md)，这里不把那些数再念一遍。

1. 打开页面，先按按钮。走廊上的三种走法，一段脑电，奖励表上的下一步，左右声，再看一根手指。先看见它做什么。
2. 回来读：这幅画面给谁，市面上的产品卡在哪，常用的库在信号没来时会交回什么，为什么挡在模型前面就够，交出去的是哪一次调用。
3. 下面的说法表只收这份说明里会反复用到的几个词。同一个词在页面上是同一个意思。

Read in that order. The page is the thing you can hand someone. This file is why it is shaped this way. The proofs, the comparison with each paper, and the full counts are in [`paper/paper.md`](paper/paper.md). They are not repeated here.

1. Open the page and press the buttons first: the three ways to walk the corridor, the brain recording, the next action on the reward table, the left-right sound, then one finger.
2. Then read who the picture is for, where shipped products get stuck, what common libraries return when a signal never arrived, why a check in front of the model is enough, and which call is actually shipped.
3. The short list below is only the words this file keeps using. The same word means the same thing on the page.

拿融资去做视频世界模型的团队，时间花在数据、训练和机器人测试上。那是生成画面的那一层。这里交付的是它前面的检查：一个页面，一次调用。它不训练，也不把别人论文里的机器人分数说成自己跑出来的。

A team funded to ship a video world model spends the work on data, training, and a robot test. That is the layer that generates the picture. What this repository ships is the check in front of that layer: a page, and one call. It does not train, and it does not present robot scores from other papers as its own runs.

别的项目的 issue 是留给那个项目自己的缺陷的。这里不把这个页面贴到别人的 issue 下面。某个库在“什么都没送来”时确有缺陷，而且能用测试修好，贡献的形式是一个 pull request。

Issues on another project are for defects in that project. This page is not posted there. When a library really does the wrong thing on a missing recording, and a test can fix it, the contribution is a pull request.

## 说法

| 说法 | 人话 | In plain words |
|---|---|---|
| 缺口 | 这一段没测到。它和“测到了零”不是一回事。 | A part that was not measured. That is different from measuring a zero. |
| 填上 | 给缺口写一个能接着用的值。后面的程序就会把它当成测到的。 | Write a usable value into the gap. The next program treats it as measured. |
| 只按测到的走 | 下一步只用已经到的信息。没到的地方先停住。 | The next step uses only what arrived. Where nothing arrived, it waits. |
| 平手 | 两条路一样长。交出去的是只走已经看见的地面的那条。 | Two routes of the same length. The one that stays on ground already seen is the one that ships. |
| 左右声 | 左耳和右耳交替。这里不声称它在治疗。规则只规定这段声音什么时候可以变。 | Sound that alternates left and right. No treatment is claimed. The rule is when that sound may change. |
| 画面先停 | 这一小段脑电不完整时，音乐和画面保持原样。 | When this stretch of the brain recording is incomplete, the music and the picture stay as they are. |
| 手指没到 | 关节角度没传来。画面不把这根手指画成已经握上。 | A joint angle did not arrive. The picture does not draw that finger closed. |

## 两个人，一幅画面

页面面对两种人。伤到他们的是同一种写法：把没测到的地方填上，再当成已经发生。

The page is for two people. What injures both is the same write: fill in what was not measured, then treat it as something that happened.

**正在适应一只灵巧手的人。** 世界模型把这只手画进场景里，让人在动作还没做完时看见这一下，用来练。画面只能画到摄像机已经看见的地方。没看见的地面如果被画成已经走过去，人就会去练一个场景里没有的动作。房间里可以有别人，他们站着，画面不把人派过去，也不把没看见的人画进来充数。

**Someone learning a dexterous hand.** The world model draws the hand into the scene so the person can see a motion before it is finished, and practice it. The picture stops where the camera stopped. If unseen ground is drawn as already crossed, the person practices a motion the place does not contain. Other people may stand in the room. The picture does not send the hand to them, and it does not add people the camera never saw.

**想把左右声听下去的人。** 左右交替的声音很难一直听。游戏是一个可以待着的开阔地方：声音继续，别人在场，不要求完成任务，也不要求高消耗的社交。若要在脑电看起来紧张时改音乐、改画面，这一小段必须是完整的。不完整就先保持。把没到的采样填成零再去改，改的就不是这个人当时的状态。这里不检测惊恐，也不声称在治疗谁。数据也不是从人身上采来的。

**Someone trying to stay with the left-right sound.** That sound is hard to keep listening to. The game is an open place where it can continue, with other people present, without a task and without demanding social effort. If the music or the picture is to change because the brain recording looks tense, that stretch has to be complete. An incomplete stretch stays as it is. Filling missing samples with zeros and then changing the scene is not a reading of the person. Nothing here detects fright, and nothing here claims to treat anyone. The numbers in the note are not taken from a person.

**你打开页面能做的。** 按播放，点击在左耳和右耳之间交替。这一小段信号完整时，休息是慢的，动作是快的。按“这一段丢了”，速度留在正在响的那一档。画面里的手只走到已经看见、可以走的地面。你按“我动了，下一格没看见”，声音可以变快，手留在原地。再看一根手指：张开的角度到了，两边都是张开；角度丢了，填上的那一版会画成握上，给用户看的那一版保持上次真正到过的角度；一次都没到过，就不画成握上。

**What the page lets you do.** Press play, and clicks alternate left and right. On a complete stretch, rest is slow and a movement is fast. Press “this stretch dropped,” and the speed stays where it is. The hand in the picture walks only on ground the camera has seen and found clear. Press “I moved; the next place was not seen,” and the sound may speed up while the hand stays. Then one finger: an open angle arrives and both views stay open; if the angle drops, the filled view draws the finger closed, and the view for the user keeps the last angle that actually arrived; if none has ever arrived, that finger is not drawn closed.

![给用户看的画面停在摄像机看见的地方。把缺口填上之后，手会走进没看见的障碍。](docs/figures/session.png)

![左右声。灰色是丢掉的那段。红线是填成零以后会改成的速度。蓝线是真正在响的速度。](docs/figures/pace.png)

![画面只画到摄像机看见的地方。没画出来的那一截里还有真实的障碍。](docs/figures/room.png)

![没有新的观测，再画一次，像素不变。把没看见的地方也涂上，这一帧就变了。](docs/figures/frames.png)

![关节角度没到。填成零的那一版把手指画成握上。给用户看的那一版不这么画。](docs/figures/aperture.png)

## 市面上的产品卡在哪

三个产品卡在同一步。模型或地图被要求交回一幅完整场景，下一家把这幅场景当成测到的。

Three products get stuck at the same step. The model or the map is asked for a finished scene, and the next module treats that scene as measured.

**世界模型。** [Cosmos](https://github.com/nvidia-cosmos/cosmos-predict1) 和 [V-JEPA 2.1](https://arxiv.org/abs/2603.14482) 的用法是先想象下一帧，再按那一帧行动。交出去的画面上看不见缺口。[Nilaksh 等人](https://arxiv.org/abs/2605.06388) 说明，一个模型可以在画面上更好，拿去规划却更差。[Yuan 等人](https://arxiv.org/abs/2609.24745) 说明，如果有一个已经知道每个想象结果的对照，成功率从 68.9% 到 79.2%；只给画面打分，收不回这个差距。难点是把未来画出来以后，看不出哪一块是猜的。[Zhang 等人](https://arxiv.org/abs/2609.02159) 从另一侧说了同一件事：留下哪一个未来，下一步动作就变了。68.9% 和 79.2% 是他们论文里的数，这里没有重跑。

**World models.** [Cosmos](https://github.com/nvidia-cosmos/cosmos-predict1) and [V-JEPA 2.1](https://arxiv.org/abs/2603.14482) are used as “imagine the next frame, then act.” The frame that leaves the model shows no gap. [Nilaksh et al.](https://arxiv.org/abs/2605.06388) showed that a model can look better and plan worse. [Yuan et al.](https://arxiv.org/abs/2609.24745) showed that a reference which already knows how each imagined future turns out lifts success from 68.9% to 79.2%, while scores of the picture alone recover little of that gap. The hard part is that a finished drawing no longer says which part was guessed. [Zhang et al.](https://arxiv.org/abs/2609.02159) say the same thing from the other side: which future you keep changes the next action. Those two percentages are theirs. They are not re-run here.

**脑机。** [LaBraM](https://arxiv.org/abs/2405.18765) 会把遮住的脑电补出来。[InterpolatedLaBraM](https://braindecode.org/dev/generated/braindecode.models.InterpolatedLaBraM.html) 让一个已经训练好的模型始终看到它训练时的电极布局。包没到、被写成零，会和“人没动”得到同一个类别。产品于是把“信号没到”做成“用户在休息”。信号如果有正有负，同一种填法还可以把休息读成动作。方向取决于被删掉的那段是正还是负。

**Brain–computer interfaces.** [LaBraM](https://arxiv.org/abs/2405.18765) fills in masked brain recordings, and [InterpolatedLaBraM](https://braindecode.org/dev/generated/braindecode.models.InterpolatedLaBraM.html) makes a trained model always see the electrode layout it was trained on. A dropped packet written as zeros gets the same class as a person who did not move. A product then treats “the packet did not arrive” as “the user is at rest.” When the voltage can be negative, the same fill can also read rest as a movement. The direction follows the sign of the samples that were deleted.

**机器人和车。** 传感器没返回时，地图、激光滤波、行车日志仍被期望交出一幅能规划的场景。车就会开过一块其实没测过的地方，因为那里现在看起来能走。

**Robots and vehicles.** When the sensor returns nothing, the map, the lidar filter, and the log player are still expected to hand back a scene a planner can drive. The vehicle then crosses a place the sensor never measured, because that place now looks clear.

![同一处分歧，出现在手上、脑电、移动机器人和车上。](docs/figures/hand-delta.png)

## 常用的库在信号没来时会交回什么

下面这些库，机器人软件和脑电软件真的会调用。在它们被设计来接受的输入上，它们是对的。信号没来的时候，它们仍交回一个下一层程序愿意接着用的结果。这个结果随后就成了一次决策。

These are libraries a robotics stack or a biosignal stack actually calls. On the input they were built for, they are right. When the signal never arrived, they still return something the next function will accept. That return then becomes a decision.

| Library | When nothing arrived | What the next program hears |
|---|---|---|
| [MuJoCo 3.13.0](https://github.com/google-deepmind/mujoco) | 没有物体的模型也能载入。A model with no bodies still loads. | 没有身体，仍是一场场景。A scene with no bodies is still a scene. |
| [munkres 1.1.4](https://github.com/bmc/munkres) | `compute([[]])` 得到 `[]`（[issue 54](https://github.com/bmc/munkres/issues/54)） | 没有指派问题，看起来像指派已经做完。No assignment problem looks like a finished assignment. |
| [NumPy 2.4.6](https://github.com/numpy/numpy) | 范数 `0.0`，均值 `NaN`。Norm `0.0`, mean `NaN`. | 缺了一条向量，看起来像零向量，或像一个会悄悄传下去的数。A missing vector looks like a zero vector, or like a number that propagates quietly. |
| [MNE-Python 1.9.0](https://github.com/mne-tools/mne-python) | 时长为 0，标注也是零。Duration 0, zero annotations. | 没录上的脑电，看起来像一段安静的录音。A missing recording looks like a quiet one. |
| [NetworkX 3.6.1](https://github.com/networkx/networkx) | 一张没有节点的图。A graph with no nodes. | 地图没载入，看起来像图上没有路、人已经到了。A map that never loaded looks like a graph with nowhere left to go. |
| [FilterPy 1.4.5](https://github.com/rlabbe/filterpy) | 没有测量的更新被接受，状态留在 `0.0`。An update with no measurement is accepted and the state stays `0.0`. | 激光没返回，看起来像状态就是零。No lidar return looks like a state of zero. |
| [Foxglove MCAP](https://github.com/foxglove/mcap) | 一条没有消息的日志。A log with no messages. | 回放在沉默上继续。Playback continues through silence. |
| [ROS 2 rosbag2](https://github.com/ros2/rosbag2) | 一个没有消息的包。A bag with no messages. | 机器人录下来的包也一样。Same for the bag a robot records. |
| [pybloom-live 4.0.0](https://github.com/joseph-fox/python-bloomfilter) | 没给键，也报告不在里面。A missing key is reported absent. | 没给键，看起来像这个键不存在。No key was given, and it looks as if that key is absent. |
| Python `wave` | 零帧的文件仍是合法声音。A file with no frames is still a legal sound. | 有采样率、没有波形，播放器仍会打开。A sample rate and no waveform is a file the next player opens. |
| [SciPy 1.17.1](https://github.com/scipy/scipy) | 写成 WAV 再读回来，长度为零，采样率 8,000 Hz。A WAV round-trip comes back with length 0 at 8,000 Hz. | 丢掉的左右声仍是一个能读的文件。A dropped left-right tone is still a readable file. |
| [soundfile 0.14.0](https://github.com/bastibe/python-soundfile) | 同一个文件读出来长度为零。The same file reads back with length 0. | 游戏用来播放的库也一样。Same for the library a game uses to play it. |
| [Pillow 11.3.0](https://github.com/python-pillow/Pillow) | 可以造出一张 0×0 的图。`Image.new` accepts a 0×0 RGB image. | 一帧可以存在，里面却没有像素。A frame can exist with no pixels. |
| [OpenCV 5.0.0](https://github.com/opencv/opencv) | 没有像素的图，非零像素数是 0。An image with no pixels has 0 nonzero pixels. | 什么都没看见，看起来像数到了零。Seeing nothing looks like a counted zero. |
| [Open3D 0.20.0](https://github.com/isl-org/Open3D) | 点云零个点，网格零个顶点。A cloud with no points, a mesh with no vertices. | 没到的手部扫描仍是一个几何对象。A hand scan that did not arrive is still a geometry object. |

每一行是同一件事。缺失被存成一个数。后面的程序分不出“什么都没测到”和“测到的是零”。

Each row is the same fact. A gap is stored as a number. The next program cannot tell “nothing was measured” from “the measurement was zero.”

这段脑电如果真有采样，类别跟着这些采样走，文件里也真有波形。什么都没送来时，上面那些调用仍然成功，于是下一层可以播放、显示、渲染。这里在同样的情况下停住。有内容的输入，数值和原来一样。

A brain stretch that really has samples keeps the class of those samples, and the file really has a waveform. When nothing arrived, the calls above still succeed, so the next layer can play, show, or render the result. On that same input, this repository stops. When the input has content, the values stay what they were.

![合法的无声文件、没有像素的图、没有点的扫描。调用都成功。](docs/figures/media.png)

## 为什么挡在模型前面就够

不另做一个世界模型。规划、解码、地图都留着。换掉的是“把缺口填上，再交给下一家”。这一步错在哪里，可以写下来核对，不靠训练。证明在 [`paper/paper.md`](paper/paper.md)。

We do not ship another world model. The planner, the decoder, and the map stay. What changes is the step that fills the gap and passes it on. How that step fails can be written down and checked. It is not trained. The proofs are in [`paper/paper.md`](paper/paper.md).

**填上的那一版已经做了决定。** 同一条最短路，在填完的地图上走一遍，再只在看见的地面上走一遍，得到的不是同一步。页面上那条走廊就是这个形状：中间没看见，填上以后会走进障碍；只按看见的走，会在那里停住。八段脑电被写成零，会把动作读成休息。奖励表只看眼前，和往前多看一步，选出的动作不同。三个产品是同一件事。

**The filled version has already decided.** The same shortest path, walked on the filled map and walked again only on ground that was seen, does not take the same step. The corridor on the page has that shape: the middle was not seen, the filled walk enters an obstacle, and the walk that stays with what was seen stops there. Eight brain samples written as zeros are read as rest instead of a movement. On the reward table, the action you pick from the row in front of you and the action you pick after looking one step ahead are different. Three products, one fact.

**更短，加上平手时偏向填上的那条，每次都会交回填上的方案。** 只走看见的地面，是填上之后仍然合法的一条路，而且不会比填上的那条更长。所以“选更短的，一样长就选填上的”每次都选中填上的方案。一样长的时候，只走看见的地面那条路是存在的，交出去的应该是它。只有填上以后才出现的那些目的地，本来就没有第二条路。剩下真正更短的那些，是靠走进没看见的地方才变短的，其中多数仍然会撞上。更短本身说明不了安全。

**Preferring the shorter route, and on a tie preferring the filled one, returns the filled route every time.** The route that stays on seen ground is still legal after the fill, and it is never strictly longer. So a score that wants the shorter route, and breaks a tie toward the filled route, selects the filled route on every try. When the lengths match, the route on seen ground exists, and that is the one to ship. Destinations that appear only after the fill have no second route. The routes that really are shorter got shorter by crossing ground that was not seen, and most of those still hit something. A shorter length does not show that the path is safe.

**往前多看一步，会在一个分数上改主意。** 表是 `[[10, 1], [-100, −100]]`。眼前选收益更高的那一列，下一步掉下去。用分数精确解，改主意的折扣是 `9/101`。先把这个分数放大再迭代，会改得太早，因为公分母丢了。从眼前那一行算起，真正多看一次，就已经和一直看下去相同。把眼前那一行也算成“已经多看了”，改主意会晚报一步。

**Looking one step ahead changes the choice at one fraction.** The table is `[[10, 1], [-100, −100]]`. The column that pays more now steps into −100. Solved in exact fractions, the discount where the choice flips is `9/101`. Scaling that fraction and iterating flips too early, because the common denominator is lost. Counted from the row in front of you, one real look ahead already matches looking forever on this table. Counting that raw row as a look ahead reports the flip one step late.

**缺口填上以后，再查“这里没测到”，什么也查不到。** 标记已经被擦掉，对象看起来和全程都测到了一样。这就是和上面那张表的差别：那些库交回一个能用的数，这里停住。

**After the gap is filled, a later look for “this was not measured” finds nothing.** The mark is gone, and the object looks like everything was measured. That is the difference from the table above. Those libraries hand back a usable number. Here the call stops.

![三条产品上的同一种分叉。填上以后走得更远。只按测到的走，停得更早。什么都没送来，就停住。](docs/figures/story.png)

![两条路都能到，是一种情况。只有填上以后才能到，是另一种。只有停在看见的地面上才能到，又是一种。一样长时，留下看见的那条。](docs/figures/partition.png)

![信号不能为负时，填零只会把动作读成休息。信号有正有负时，两种读错都会出现。](docs/figures/signfill.png)

页面上还有一个容易误会的按钮：只堵住第一次撞上的地方，再规划。后面没看见的地方还在，路可以再撞一次。一直问到能走通，多数会撞的图要问很多次。所以“问一次”不是这层检查。检查是：没看见，就不走进去。

The page has a button that is easy to misread: block the first collision, then plan again. Unseen ground remains, and the route can hit something again. Asking until the route is clear takes more than one question on most of the maps that hit something. One question is not this check. The check is: if it was not seen, do not walk into it.

## 交出去的是什么

一次调用，三种结果。它坐在产品已经在跑的规划前面。

One call, three outcomes. It sits in front of a planner the product already runs.

| 调用 | 人拿到的 | 它不做的 |
|---|---|---|
| `measure` | 只用已经到的信息。平手时留在看见的地面上。脑电的缺口不填零。 | 不给缺口编一个值，平手时也不改选填上的那条路。 |
| `impute` | 旁边的对照。同一个规划，在缺口被填上之后会怎么走。演示用它给人看两边不一样。 | 这不是交出去的那一版。 |
| 停住 | 什么都没送来时的结果。 | 不交回零，不交回一个里面什么都没有的列表，也不交回一个会悄悄传下去的非数。 |

页面上能对上的三件事：走廊中间没看见，填上以后会走完，只按看见的会提前停下；八段脑电写成零，类别从动作变成休息；奖励表往前看一步，和只看眼前，动作不同。

The page lines up with three cases. On the corridor the middle was not seen: the filled walk finishes, the walk that stays with what was seen stops early. Eight brain samples written as zeros change the class from a movement to rest. On the reward table, looking one step ahead and looking only at the current row pick different actions.

这次没有训练好的视频模型，没有头戴设备的开发包，没有机器人成功率，也没有治疗效果。68.9% 和 79.2% 属于 Yuan 等人。

Not in this delivery: a trained video model, a headset SDK, a robot success rate, or a treatment effect. 68.9% and 79.2% belong to Yuan et al.

## 一个人可以打开的页面

[`site/index.html`](site/index.html) 在浏览器里做完上面三件事，也播放左右声，也演示一根手指。页面上没有训练，也不需要账号。GitHub Pages 用本仓库发布：[shaneraphel.github.io/aletheia-worldtick](https://shaneraphel.github.io/aletheia-worldtick/)。

[`site/index.html`](site/index.html) runs those three cases in the browser, plays the left-right sound, and shows one finger. Nothing on the page is trained, and it asks for no account. GitHub Pages serves it from this repository: [shaneraphel.github.io/aletheia-worldtick](https://shaneraphel.github.io/aletheia-worldtick/).

```bash
make check
python3.12 show_story.py
python3.12 show_policy.py
```

`make check` 把笔记里的计数重新算一遍。计数在 `results/`。和每篇论文的方法对照在 [`paper/paper.md`](paper/paper.md)。要并排调用那些库，用 `requirements-show.txt` 里的版本。

`make check` recomputes the counts cited in the note. The counts live in `results/`. The comparison with each paper’s method is in [`paper/paper.md`](paper/paper.md). Callers that import those libraries side by side need the versions in `requirements-show.txt`.

## 这层检查要坐在谁前面

| 项目 | 它交出来的 | 这层检查做什么 |
|---|---|---|
| [V-JEPA 2.1](https://arxiv.org/abs/2603.14482) | 补出来的画面碎片 | 不把预测出来的一块当成已经看见 |
| [Cosmos](https://github.com/nvidia-cosmos/cosmos-predict1) | 预测的下一帧 | 同一条，用在画出来的未来上 |
| [LaBraM](https://arxiv.org/abs/2405.18765) | 补出来的脑电 | 不把填成零的丢包读成休息 |
| [NetworkX](https://github.com/networkx/networkx) | 整张图上能走到的全部 | 只走已经看见的下一步，不把走完的路当成现在 |
| [MNE-Python](https://github.com/mne-tools/mne-python) | 一段录音 | 一个采样都没有时停住 |
| [MuJoCo](https://github.com/google-deepmind/mujoco) | 一个模型 | 没有物体的模型上停住 |
| [Foxglove MCAP](https://github.com/foxglove/mcap) | 一条日志 | 一条消息都没有时停住 |
| [ROS 2 rosbag2](https://github.com/ros2/rosbag2) | 一个录包 | 一条消息都没有时停住 |
| [ROS map_server](https://wiki.ros.org/map_server) | 一张地图 | 没测到的地方保持没测到 |
| [FilterPy](https://github.com/rlabbe/filterpy) | 一次状态更新 | 没有测量时停住 |

对应各个文件格式的检查在 `locks/`。索引是 [`ATLAS.md`](ATLAS.md)。

## 文件

| 路径 | 它在产品里做什么 |
|---|---|
| `tick.py` | 只按已经到的信息走下一步 |
| `datalog.py` | 把路走完，那是填上缺口之后才会交回的结果 |
| `complete.py` · `decode.py` · `policy.py` | 三种填法：地图、脑电、奖励表 |
| `partition.py` | 两条路的包含关系，以及一样长时留哪一条 |
| `signfill.py` | 不能为负的信号，和有正有负的电压，填零以后各读成什么 |
| `decisive.py` | 只堵住第一次撞上的地方，再规划 |
| `askdepth.py` | 要问多少次，路才清楚 |
| `session.py` | 脑电不完整时声音保持；没看见的地方不画成已经抓完 |
| `fleet.py` | 同一批地图，一个核和多个核，结果相同 |
| `media.py` | 无声文件、没有像素的图、没有点的扫描，旁边是保持原样的会话 |
| `pace.py` | 左右声：信号完整时可以变快变慢，丢了就保持 |
| `room.py` | 画面停在摄像机看见的最后一处 |
| `attempt.py` | 听见动作，并不等于走进还没看见的地方 |
| `ledger.py` | 丢掉的那段不记类别；手停在已经看见的地方 |
| `company.py` | 一个人只有被看见才画出来 |
| `framecheck.py` | 没有新观测，再画一次像素不变；把缺口也涂上，帧就变了 |
| `clock.py` | 丢掉的那段，速度和画面都不动 |
| `near.py` | 离房间里的人有多远：只走看见的地面，和把没看见的当成能走 |
| `reel.py` | 速度可以变，画面仍停在这一帧 |
| `aperture.py` | 关节角度没到，不是这根手指已经握上 |
| `site/index.html` | 浏览器里的页面 |
| `paper/paper.md` | 理论、它是怎么被发现的、和每篇参考文献的方法对照 |
| `tests/test_precision.py` | 这些关系一旦变了，测试就失败 |
| `kits/README.md` | 本机的启动器、自然场景模型和钢琴录音放在哪 |

## 本机的画面和声音

开放世界的画面还不是一个已经发布的虚幻关卡。这台机器上已经装了 Epic 启动器，解压了两套可自由使用的自然场景模型，并放了一份贝多芬第十五钢琴奏鸣曲的公有领域录音。虚幻编辑器本体没有安装：4.27 的 Mac 说明停在 macOS Big Sur，而这台电脑是 Apple Silicon 上的 macOS 26。要拿到引擎，需要登录启动器。这些文件不进 GitHub。路径和许可在 [`kits/README.md`](kits/README.md)。

The open-world picture is not a shipped Unreal level. On this machine the Epic Games Launcher is installed, two freely usable nature model packs are unpacked, and a public-domain recording of Beethoven's Piano Sonata No. 15 is on disk. The Unreal Editor itself is not installed: the Mac notes for 4.27 stop at macOS Big Sur, and this computer is Apple Silicon on macOS 26. An engine build means signing into the launcher. Those files stay off GitHub. Paths and licenses are in [`kits/README.md`](kits/README.md).

## License

MIT
