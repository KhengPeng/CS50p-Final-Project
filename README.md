# Project Title: NBA Web Scrapping Project

User will be prompted to enter the name(s) of NBA players and the program will scrap data from the official [NBA](https://www.nba.com/stats) website. These data can then be used to create visualisations for further analysis.

## Video Demo

You can watch a video demonstration in the link [here](https://youtu.be/rP-pNSaPR7A).

## API Package: nba_api
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install nba_api. Read the documentation [here](https://github.com/swar/nba_api).

```bash
pip install nba_api
```

## Required Packages:
```python
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from nba_api.stats.static import players
from nba_api.stats.endpoints import playerprofilev2
```
## Input Example:
Once the program is executed, it will ask users for inputs as shown below.
```bash
How many players do you want to analyse? 3
Player name: Stephen Curry
Player data up till which age: 30
Season type: playoffs
```
The program will then display a list of attributes that can be used to plot data. Enter the corresponding index to select. A similar list will be displayed for selection for each axis.
```bash
0           SEASON_TYPE
1                PLAYER
2            PLAYER_AGE
3        YEAR_IN_LEAGUE
4             SEASON_ID
5     TEAM_ABBREVIATION
6                    GP
7                   MIN
8          MIN_PER_GAME
9                   FGM
10         FGM_PER_GAME
11                  FGA
12         FGA_PER_GAME
13               FG_PCT
14                 FG3M
15        FG3M_PER_GAME
16                 FG3A
17        FG3A_PER_GAME
18              FG3_PCT
19                  FTM
20         FTM_PER_GAME
21                  FTA
22         FTA_PER_GAME
23               FT_PCT
24                 OREB
25        OREB_PER_GAME
26                 DREB
27        DREB_PER_GAME
28                  REB
29         REB_PER_GAME
30                  AST
31         AST_PER_GAME
32                  STL
33         STL_PER_GAME
34                  BLK
35         BLK_PER_GAME
36                  TOV
37         TOV_PER_GAME
38                   PF
39          PF_PER_GAME
40                  PTS
41         PTS_PER_GAME
dtype: object
What statistic do you want to analyse for x? Enter the corresponding numerical index: 3
```

## Sample Output:
Output for Stephen Curry, with data up till 30 years old in the playoffs:
![](https://github.com/KhengPeng/CS50p-Final-Project/blob/main/Figure_1.png)

Output for Stephen Curry, Kevin Durant, Lebron James, with data up till 30 years old in the playoffs:
![](https://github.com/KhengPeng/CS50p-Final-Project/blob/main/Figure_2.png)
