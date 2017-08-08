Drop View PlayerRankings
GO

Create View PlayerRankings AS
SELECT 
	t.Code as Team,
	p.Name as Player,
	pos.Code as Position,
	r.AvgRank as PlayerAvgRank
FROM (select 
		r.TeamID,
		r.PlayerID,
		AVG(r.[Rank]) as 'AvgRank',
		COUNT(d.DataSourceID) as 'NumSources'
	from dbo.playerranking r
	left join dbo.DataSource d on r.datasourceid = d.DataSourceID
	where r.Date = '07/17/2017'
	group by r.TeamId, r.PlayerID
	--order by 'NumSources' DESC, 'AvgRank' ASC
) r
left join dbo.team t on r.teamid = t.teamid
left join dbo.OffensiveLineTeamRank otr on otr.teamid = t.teamid and otr.Date = '2017-08-06'
left join dbo.DefensiveTeamRank dtr on dtr.teamid = t.teamid and dtr.Date = '2017-07-20'
left join dbo.player p on r.playerid = p.playerid and p.teamid = r.teamid
left join dbo.position pos on p.positionid = pos.positionid
--where NumSources > 1
GO
