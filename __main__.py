from espn_api.football import League
import asyncio
import os
import hikari
import lightbulb
import requests
import pprint
import json
import re
from ESPN import *

espn_cookies = {"swid": SWID, "espn_s2": S2}

with open("./secrets/token") as f:
    _token = f.read().strip()

league = League(league_id=LEAGUE_ID, year=YEAR, espn_s2=S2, swid=SWID)
bot = lightbulb.BotApp(
    token=_token,
    intents=hikari.Intents.ALL_UNPRIVILEGED,
    default_enabled_guilds=GUILD_ID,
)

@bot.command()
@lightbulb.option("player", "Enter first name of player(Leave empty for all matchups)", default='all')
@lightbulb.option("week", "Enter week(optional)", required=False)
@lightbulb.command("matchup", "get matchup(s) for current week")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_matchup(ctx: lightbulb.SlashCommand) -> None:
    name = ctx.options.player
    week = ctx.options.week

    response = ""
    if(name == 'all'):
        box_scores = league.box_scores(int(week)) if week else league.box_scores()
        for matchup in box_scores:
            response += "**" + str(matchup.home_score) + "** " + matchup.home_team.team_abbrev + " vs. " + matchup.away_team.team_abbrev + " **" + str(matchup.away_score) + "**\n"
        embed = hikari.Embed(title="List of matchups", description=response)
        embed.set_thumbnail(THUMBNAIL)
    else:
        embed = hikari.Embed(title="Matchup Info")
        embed.set_thumbnail(THUMBNAIL)
        team_name = TEAMS[name]
        team_list = league.teams
        home_team = None
        away_team = None
        home_roster = None
        away_roster = None

        for team in team_list:
            if(team.team_name.lower() == team_name.lower()):
                home_team = team

        box_scores = league.box_scores(int(week)) if week else league.box_scores()

        for matchup in box_scores:
            if(matchup.home_team.team_name == home_team.team_name):
                home_roster = matchup.home_lineup
                away_roster = matchup.away_lineup
                away_team = matchup.away_team
            elif(matchup.away_team.team_name == home_team.team_name):
                home_roster = matchup.away_lineup
                away_roster = matchup.home_lineup
                away_team = matchup.home_team

        home_response = ""
        home_total_points = 0
        home_total_projected = 0
        for player in home_roster:
            if(player.slot_position.lower() != "be"):
                home_response += "**" + player.name + "**, points: **" + str(player.points) + "**, projected: **" + str(player.projected_points) + "**\n"
                home_total_points += player.points
                home_total_projected += player.projected_points
        home_response += "Total Points: **" + str(round(home_total_points,1)) + "**, Projected Points: **" + str(round(home_total_projected,1)) + "**"
        embed.add_field(home_team.team_name, home_response)

        away_response = ""
        away_total_points = 0
        away_total_projected = 0
        for player in away_roster:
            if(player.slot_position.lower() != "be"):
                away_response += "**" + player.name + "**, points: **" + str(player.points) + "**, projected: **" + str(player.projected_points) + "**\n"
                away_total_points += player.points
                away_total_projected += player.projected_points
        away_response += "Total Points: **" + str(round(away_total_points,1)) + "**, Projected Points: **" + str(round(away_total_projected,1)) + "**"
        embed.add_field(away_team.team_name, away_response)
        
        if(home_total_points > away_total_points):
            embed.set_footer("Winner: " + home_team.team_name)
        elif(home_total_points < away_total_points):
            embed.set_footer("Winner: " + away_team.team_name)
        else: 
            embed.set_footer("Matchup Tied")
    await ctx.respond(embed)

@bot.command()
@lightbulb.command("ranks", "get current power rankings")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_ranks(ctx: lightbulb.SlashCommand) -> None:
    response = ""
    power_rankings = league.power_rankings()
    counter = 1
    for team in power_rankings:
        response += "**" + str(counter) + "**" + ". \t\t\t" + "(" + str(team[1].wins) + "-" + str(team[1].losses) + ") " + team[1].team_name + "\n"
        counter += 1
    embed = hikari.Embed(title="Current Power Rankings", description=response)
    embed.set_thumbnail(THUMBNAIL)
    await ctx.respond(embed)

@bot.command()
@lightbulb.option("name", "Enter first and last name of player ex: 'Justin Jefferson'")
@lightbulb.command("player", "return information of a given player")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_ranks(ctx: lightbulb.SlashCommand) -> None:
    name = ctx.options.name
    league_teams = league.teams
    free_agents = league.free_agents()

    nfl_player = None
    regex = re.compile('[^a-zA-Z]')
    p_name = ""

    for team in league_teams:
        for player in team.roster:
            curr_name = regex.sub('', player.name.lower())
            player_name = regex.sub('', name.lower())
            if(curr_name == player_name):
                nfl_player = player
    
    if not nfl_player:
        for player in free_agents:
            curr_name = regex.sub('', player.name.lower())
            player_name = regex.sub('', name.lower())
            if(curr_name == player_name):
                nfl_player = player

    if not nfl_player:
        await ctx.respond("Player could not be found")
    else:
        player_info = league.player_info(playerId=nfl_player.playerId).stats
        week_scores = []
        for i in player_info:
            if(i != 0):
                week_scores.append(player_info[i]['points'])
        week_scores.reverse()

        result = ""
        for i in range(len(week_scores)):
            result += "Week " + str(i+1) + ": **" + str(week_scores[i]) + "** FPTS\n"
    
        url = 'https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/{}.png&w=350&h=254'.format(nfl_player.playerId)
        embed = hikari.Embed(title=nfl_player.name, description=(nfl_player.position + " | " + PRO_TEAM_MAP[nfl_player.proTeam]))
        embed.add_field("Position Rank: ", str(nfl_player.posRank), inline=True)
        embed.add_field("Percent Owned: ", str(nfl_player.percent_owned) + "%", inline=True)
        embed.add_field("Injury Status: ", str(nfl_player.injuryStatus), inline=True)
        embed.add_field("Fantasy Points: ", result, inline=True)
        embed.set_thumbnail(THUMBNAIL)
        embed.set_image(url)
        await ctx.respond(embed)

if __name__ == "__main__":
    if os.name != "nt":
        import uvloop
        uvloop.install()
    bot.run()
