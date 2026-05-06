# ESPN Fantasy Football Discord Bot

A **Discord bot built with Python** that integrates with ESPN Fantasy Football to provide real-time insights into your league.
Get quick access to **player stats, matchups, rosters, and power rankings**—right inside Discord.

---

## Features

*  Player lookups with detailed stats
*  Weekly matchup tracking and breakdowns
*  Full roster views
*  League power rankings
*  Fast, simple slash commands

---

## Tech Stack

* **Python**
* **Discord API** (slash commands)
* ESPN Fantasy Football data integration

---

## Commands

### `/player player:<name>`

Retrieve detailed information about a player.

**Includes:**

* Team & position
* Position rank
* Percent owned
* Injury status
* Weekly fantasy points (up to current week)

![Player Command](https://user-images.githubusercontent.com/100002813/192939160-6d309812-0fe8-47d5-8894-c63a14b3ee52.png)

---

### `/matchup`

View a quick summary of all matchups for the **current week**.

* Displays current scores
* Scores may appear as `0` if games haven’t started yet
* Weeks run from **Thursday Night Football → Monday Night Football**

![Matchups Overview](https://user-images.githubusercontent.com/100002813/193148124-ba669013-cf86-415f-8372-1a7c0dd9cf6d.png)

---

### `/matchup week:<number>`

View matchup scores for a **specific week**.

* Same format as the default matchup command
* Pulls historical data instead of current week

![Matchups by Week](https://user-images.githubusercontent.com/100002813/193147488-164a5d86-a2d2-4e46-8879-47cee6f78524.png)

---

### `/matchup player:<name>`

Get a **detailed breakdown** of a specific team’s matchup.

**Includes:**

* Current starting roster
* Player-by-player points (scored & projected)
* Total team score & projections
* Current or final winner (shown in footer)

![Detailed Matchup](https://user-images.githubusercontent.com/100002813/197590872-2a210e23-70ee-4cdf-b34e-9e78997c7752.png)

---

### `/roster player:<name>`

View a team’s full roster and player details.

**Includes:**

* Position & team
* Injury status
* Roster percentages

![Roster View](https://user-images.githubusercontent.com/100002813/197592502-9525bacd-3d64-47a3-ac77-69034cbe2374.png)

---

### `/ranks`

Displays current **league power rankings** using a **two-step dominance system**.

![Power Rankings](https://user-images.githubusercontent.com/100002813/193149537-4ba4f6c1-e098-4969-aab1-5063faf36760.png)

---

## ⚙️ Setup

```bash
# Clone the repository
git clone https://github.com/your-username/espn-fantasy-football-discord-bot.git

# Navigate into the project
cd espn-fantasy-football-discord-bot

# Install dependencies
pip install -r requirements.txt

# Run the bot
python bot.py
```

---

## Configuration

Before running the bot, make sure to:

* Add your **Discord bot token**
* Configure your **ESPN league settings / credentials** (if required)

---

## Future Improvements

* Trade analysis tools
* Waiver wire suggestions
* Player comparison command
* Advanced analytics & projections

---

## Contributing

Pull requests are welcome! If you have ideas for new features or improvements, feel free to open an issue.

---

## License

This project is licensed under the MIT License.
