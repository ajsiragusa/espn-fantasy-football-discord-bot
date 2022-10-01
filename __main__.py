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
            if(matchup.home_score > matchup.away_score):
                response += str(matchup.home_score) + " - [**" + matchup.home_team.team_abbrev + "**] vs. " + matchup.away_team.team_abbrev + " - " + str(matchup.away_score) + "\n\n"
            else:
                response += str(matchup.home_score) + " - " + matchup.home_team.team_abbrev + " vs. [**" + matchup.away_team.team_abbrev + "**] - " + str(matchup.away_score) + "\n\n"
        embed = hikari.Embed(title="List of matchups", description=response)
        embed.set_thumbnail(THUMBNAIL)
    else:
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

        embed = hikari.Embed(title=home_team.team_name + " vs. " + away_team.team_name)
        embed.set_thumbnail(THUMBNAIL)

        qb = []
        qb2 = []
        rb = []
        rb2 = []
        wr = []
        wr2 = []
        te = []
        te2 = []
        dst = []
        dst2 = []
        k = []
        k2 = []

        for player in home_roster:
            if(player.slot_position.lower() != "be" or player.slot_position.lower() != "ir"):
                if(player.position.lower() == 'qb'):
                    qb.append(player)
                elif(player.position.lower() == 'rb'):
                    rb.append(player)
                elif(player.position.lower() == 'wr'):
                    wr.append(player)
                elif(player.position.lower() == 'te'):
                    te.append(player)
                elif(player.position.lower() == 'k'):
                    k.append(player)
                else:
                    dst.append(player)

        for player in away_roster:
            if(player.slot_position.lower() != "be" or player.slot_position.lower() != "ir"):
                if(player.position.lower() == 'qb'):
                    qb2.append(player)
                elif(player.position.lower() == 'rb'):
                    rb2.append(player)
                elif(player.position.lower() == 'wr'):
                    wr2.append(player)
                elif(player.position.lower() == 'te'):
                    te2.append(player)
                elif(player.position.lower() == 'k'):
                    k2.append(player)
                else:
                    dst2.append(player)    

        home_roster.clear()
        home_roster = qb + rb + wr + te + dst + k

        away_roster.clear()
        away_roster = qb2 + rb2 + wr2 + te2 + dst2 + k2

        home_response = ""
        home_response_p = ""
        home_response_m = ""
        home_total_points = 0
        home_total_projected = 0
        for player in home_roster:
            if(player.slot_position.lower() != "be"):
                home_response += "**" + player.name + "**\n" 
                home_response_p += "FPTS: **" + str(player.points) + "**, PROJ: **" + str(player.projected_points) + "**\n"
                home_response_m += player.pro_opponent + " | **" + str(player.pro_pos_rank) + "**\n"
                home_total_points += player.points
                home_total_projected += player.projected_points
        home_response += "Total Points: "
        home_response_p += "FPTS: **" + str(round(home_total_points,1)) + "**, PROJ: **" + str(round(home_total_projected,1)) + "**"
        embed.add_field(home_team.team_abbrev, home_response, inline=True)
        embed.add_field("Points", home_response_p, inline=True)
        embed.add_field("Matchup", home_response_m, inline=True)

        embed.add_field("\u200c", "\u200c", inline=False)

        away_response = ""
        away_response_p = ""
        away_response_m = ""
        away_total_points = 0
        away_total_projected = 0
        for player in away_roster:
            if(player.slot_position.lower() != "be"):
                away_response += "**" + player.name + "**\n" 
                away_response_p += "FPTS: **" + str(player.points) + "**, PROJ: **" + str(player.projected_points) + "**\n"
                away_response_m += player.pro_opponent + " | **" + str(player.pro_pos_rank) + "**\n"
                away_total_points += player.points
                away_total_projected += player.projected_points
        away_response += "Total Points: "
        away_response_p += "FPTS: **" + str(round(away_total_points,1)) + "**, PROJ: **" + str(round(away_total_projected,1)) + "**"
        embed.add_field(away_team.team_abbrev, away_response, inline=True)
        embed.add_field("Points", away_response_p, inline=True)
        embed.add_field("Matchup", away_response_m, inline=True)

        
        
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
async def cmd_player(ctx: lightbulb.SlashCommand) -> None:
    name = ctx.options.name
    league_teams = league.teams
    free_agents = league.free_agents()

    nfl_player = None
    regex = re.compile('[^a-zA-Z]')
    p_name = ""

    save_team = None

    for team in league_teams:
        for player in team.roster:
            curr_name = regex.sub('', player.name.lower())
            player_name = regex.sub('', name.lower())
            if(curr_name == player_name):
                nfl_player = player
                save_team = team.team_name
    
    if not nfl_player:
        for player in free_agents:
            curr_name = regex.sub('', player.name.lower())
            player_name = regex.sub('', name.lower())
            if(curr_name == player_name):
                nfl_player = player
                save_team = "Free Agent"

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
        embed.add_field("\u200c", "\u200c", inline=False)
        embed.add_field("Fantasy Points: ", result, inline=True)
        embed.add_field("Current Team: ", save_team, inline=True)
        embed.set_thumbnail(THUMBNAIL)
        embed.set_image(url)
        await ctx.respond(embed)

@bot.command()
@lightbulb.option("name", "Enter first of player whos roster to display'")
@lightbulb.command("roster", "return information of a players roster")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_roster(ctx: lightbulb.SlashCommand) -> None:
    box_scores = league.box_scores()
    name = TEAMS[ctx.options.name]
    team_list = league.teams

    roster = []
    for matchup in box_scores:
        if(matchup.home_team.team_name == name):
            roster = matchup.home_lineup
        elif(matchup.away_team.team_name == name):
            roster = matchup.away_lineup

    if not roster:
        await ctx.respond("No player found with name " + ctx.options.name)
    else:
        starters = []
        bench = []

        for roster_player in roster:
            if(roster_player.slot_position.lower() == "be" or roster_player.slot_position.lower() == "ir"):
                bench.append(roster_player)
            else:
                starters.append(roster_player)

        qb = []
        rb = []
        wr = []
        te = []
        dst = []
        k = []

        for strter in starters:
            if(strter.position.lower() == 'qb'):
                qb.append(strter)
            elif(strter.position.lower() == 'rb'):
                rb.append(strter)
            elif(strter.position.lower() == 'wr'):
                wr.append(strter)
            elif(strter.position.lower() == 'te'):
                te.append(strter)
            elif(strter.position.lower() == 'k'):
                k.append(strter)
            else:
                dst.append(strter)

        starters.clear()
        starters = qb + rb + wr + te + dst + k

        response_s = ""
        response_s2 = ""
        response_s3 = ""

        response_b = ""
        response_b2 = ""
        response_b3 = ""

        for starter in starters:
            response_s += "**" + starter.name + "**\n"
            response_s2 += starter.position + " - " + starter.proTeam + " | **" + starter.injuryStatus + "**\n" 

        temp_list = []
        for player in starters:
            temp_list.append(league.player_info(playerId=player.playerId))

        for player in temp_list:
            response_s3 += "O: **" + str(round(player.percent_owned,1)) + "**% ST: **" + str(round(player.percent_started,1)) + "**% RNK: **" + str(player.posRank) + "**\n"

        temp_list.clear()
        for player in bench:
            temp_list.append(league.player_info(playerId=player.playerId))

        for bench_player in bench:
            response_b += "**" + bench_player.name + "**\n"
            response_b2 += bench_player.position + " - " + bench_player.proTeam + " | **" + bench_player.injuryStatus + "**\n" 

        for player in temp_list:
            response_b3 += "O: **" + str(round(player.percent_owned,1)) + "**% ST: **" + str(round(player.percent_started,1)) + "**% RNK: **" + str(player.posRank) + "**\n"
        
        embed = hikari.Embed(title=name)
        embed.add_field("Starters", response_s, inline=True)
        embed.add_field("Team + Status", response_s2, inline=True)
        embed.add_field("%'s + Pos Rank", response_s3, inline=True)
        embed.add_field("\u200c", "\u200c", inline=False)
        embed.add_field("Bench", response_b, inline=True)
        embed.add_field("Team + Status", response_b2, inline=True)
        embed.add_field("%'s + Pos Rank", response_b3, inline=True)

        await ctx.respond(embed)

if __name__ == "__main__":
    if os.name != "nt":
        import uvloop
        uvloop.install()
    bot.run()
