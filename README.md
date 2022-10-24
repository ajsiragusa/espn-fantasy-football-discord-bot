# espn-fantasy-football-discord-bot
Discord bot that gives information about players, matchups, and power rankings.

# player command (/player player:cooper kupp)
Pulls team info, position rank, percent owned, injury Status, and weekly fantasy points up to the current week.

![espn1](https://user-images.githubusercontent.com/100002813/192939160-6d309812-0fe8-47d5-8894-c63a14b3ee52.png)

# matchup command with no parameters (/matchup)
Gives a vague list of matchups for the current week and their scores thus far. This could be 0 for all teams if nobody in the week has played yet. Each week starts at the thursday night game and ends after the monday night game.

![espn3](https://user-images.githubusercontent.com/100002813/193148124-ba669013-cf86-415f-8372-1a7c0dd9cf6d.png)

# matchup command with week parameter (/matchup week:2)
Looks the same as the vague matchup command with no params but pulls the scores from the specified week

![espn2](https://user-images.githubusercontent.com/100002813/193147488-164a5d86-a2d2-4e46-8879-47cee6f78524.png)

# matchup command with player parameter (/matchup player: anthony)
When given a player, the matchup command will give a in depth look at their matchup for the current week, or the week provided.
This will include the current starting roster, each players total and projected points this week, and the total overall projected and scored points.
Finally, the footer will show the winner of the week, or if the week's not over, it will show the current winner.

![espn6](https://user-images.githubusercontent.com/100002813/197590872-2a210e23-70ee-4cdf-b34e-9e78997c7752.png)

# ranks command (/ranks)
Lists the current power rankings for the league teams using two step dominance.

![espn5](https://user-images.githubusercontent.com/100002813/193149537-4ba4f6c1-e098-4969-aab1-5063faf36760.png)

