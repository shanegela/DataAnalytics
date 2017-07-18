/*select 
	d.Name as DataSource,
	t.Name as Team,
	p.Name as Player,
	r.[Rank] 
from dbo.playerranking r
left join dbo.DataSource d on r.datasourceid = d.DataSourceID
left join dbo.team t on r.teamid = t.teamid
left join dbo.player p on r.playerid = p.playerid
order by t.Name, p.Name, r.[Rank]
*/

declare @rankDate date = '07/17/2017'

SELECT 
	t.Name as Team,
	p.Name as Player,
	pos.Name as Position,
	pos.Side,
	r.AvgRank,
	r.NumSources
FROM (select 
		r.TeamID,
		r.PlayerID,
		AVG(r.[Rank]) as 'AvgRank',
		COUNT(d.DataSourceID) as 'NumSources'
	from dbo.playerranking r
	left join dbo.DataSource d on r.datasourceid = d.DataSourceID
	where r.Date = @rankDate
	group by r.TeamId, r.PlayerID
	--order by 'NumSources' DESC, 'AvgRank' ASC
) r
left join dbo.team t on r.teamid = t.teamid
left join dbo.player p on r.playerid = p.playerid and p.teamid = r.teamid
left join dbo.position pos on p.positionid = pos.positionid
where NumSources > 3 and pos.Code = 'QB'
order by NumSources DESC, AvgRank ASC

SELECT 
	t.Name as Team,
	p.Name as Player,
	pos.Name as Position,
	pos.Side,
	r.AvgRank,
	r.NumSources
FROM (select 
		r.TeamID,
		r.PlayerID,
		AVG(r.[Rank]) as 'AvgRank',
		COUNT(d.DataSourceID) as 'NumSources'
	from dbo.playerranking r
	left join dbo.DataSource d on r.datasourceid = d.DataSourceID
	where r.Date = @rankDate
	group by r.TeamId, r.PlayerID
	--order by 'NumSources' DESC, 'AvgRank' ASC
) r
left join dbo.team t on r.teamid = t.teamid
left join dbo.player p on r.playerid = p.playerid and p.teamid = r.teamid
left join dbo.position pos on p.positionid = pos.positionid
where NumSources > 3 and pos.Code = 'RB'
order by NumSources DESC, AvgRank ASC

SELECT 
	t.Name as Team,
	p.Name as Player,
	pos.Name as Position,
	pos.Side,
	r.AvgRank,
	r.NumSources
FROM (select 
		r.TeamID,
		r.PlayerID,
		AVG(r.[Rank]) as 'AvgRank',
		COUNT(d.DataSourceID) as 'NumSources'
	from dbo.playerranking r
	left join dbo.DataSource d on r.datasourceid = d.DataSourceID
	where r.Date = @rankDate
	group by r.TeamId, r.PlayerID
	--order by 'NumSources' DESC, 'AvgRank' ASC
) r
left join dbo.team t on r.teamid = t.teamid
left join dbo.player p on r.playerid = p.playerid and p.teamid = r.teamid
left join dbo.position pos on p.positionid = pos.positionid
where NumSources > 2 and pos.Code = 'WR'
order by NumSources DESC, AvgRank ASC

SELECT 
	t.Name as Team,
	p.Name as Player,
	pos.Name as Position,
	pos.Side,
	r.AvgRank,
	r.NumSources
FROM (select 
		r.TeamID,
		r.PlayerID,
		AVG(r.[Rank]) as 'AvgRank',
		COUNT(d.DataSourceID) as 'NumSources'
	from dbo.playerranking r
	left join dbo.DataSource d on r.datasourceid = d.DataSourceID
	where r.Date = @rankDate
	group by r.TeamId, r.PlayerID
	--order by 'NumSources' DESC, 'AvgRank' ASC
) r
left join dbo.team t on r.teamid = t.teamid
left join dbo.player p on r.playerid = p.playerid and p.teamid = r.teamid
left join dbo.position pos on p.positionid = pos.positionid
where NumSources > 3 and pos.Code = 'TE'
order by NumSources DESC, AvgRank ASC

