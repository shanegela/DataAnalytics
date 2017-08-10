-- Game Schedule
select g.GameWeek, g.GameDate, g.AwayTeam, at.Name, g.HomeTeam, ht.Name
from GameSchedule g
left join Team at on g.AwayTeam = at.Code
left join Team ht on g.HomeTeam = ht.Code
--where at.Code is null or ht.Code is null

-- Defensive Team Ranks
select d.Team, d.Rank, t.Name
from DefensiveTeamRank d
left join Team t on d.Team = t.Code
--where t.Code is null

-- Offensive Team Ranks
select o.Team, o.[Rank], t.Name
from OffensiveTeamRank o
left join Team t on o.Team = t.Code
--where t.Code is null

-- Offensive Line Ranks
-- Hand Generated From Fantasy Alarm
-- http://www.fantasyalarm.com/articles/Daniel%20Malin/42185/2017-nfl-fantasy-football-offensive-lines/
select o.Team, o.[Rank], t.Name
from OffensiveLineRank o
left join Team t on o.Team = t.Code
--where t.Code is null

-- Football DB Player Rankings
select f.Team, f.Position, f.Name, f.Rank, t.Name
from FootballDB f
left join Team t on f.Team = t.Code
where t.Code is null

-- NFL Player Rankings
select f.Team, f.Position, f.Name, f.Rank, t.Name
from NFL f
left join Team t on f.Team = t.Code
where t.Code is null