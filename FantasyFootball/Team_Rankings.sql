-- offensive: higher the rank the better
-- defensive: lower the rank the better

select 
	gw.Description as Week,
	g.GameDate,
	t1.Name as Team1,
	o1.[Rank] as Team1_OffensiveRank,
	d1.[Rank] as Team1_DefensiveRank,
	t2.Name as Team2,
	o2.[Rank] as Team2_OffensiveRank,
	d2.[Rank] as Team2_DefensiveRank,
	ABS(o1.[Rank] - o2.[Rank]) as offensive_diff,
	ABS(d1.[Rank] - d2.[Rank]) as defensive_diff
from dbo.GameSchedule g
left join dbo.GameWeek gw on g.GameWeekID = gw.GameWeekID
left join dbo.Team t1 on g.TeamID1 = t1.TeamID
left join dbo.Team t2 on g.TeamID2 = t2.TeamID
left join dbo.OffensiveTeamRank o1 on o1.teamid = t1.TeamID
left join dbo.OffensiveTeamRank o2 on o2.teamid = t2.TeamID
left join dbo.DefensiveTeamRank d1 on d1.teamid = t1.TeamID
left join dbo.DefensiveTeamRank d2 on d2.teamid = t2.TeamID
where gw.Description = 'Week 1'
order by offensive_diff DESC, defensive_diff ASC
