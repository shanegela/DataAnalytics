-- Running Back
SELECT  r.Team, p.name as Player, p.position, r.RB_Rank, CONVERT(INT,p.[rank]) as PlayerRank, TotalRank = (r.RB_Rank*.60) + (CONVERT(INT,p.[rank]) *.40)
FROM 
(	SELECT SUM(RB_Rank) as RB_Rank, Team
	From (
		(select RB_AwayRank as RB_Rank, AwayTeam as Team from vRankSummary)
		union all
		(select RB_HomeRank as RB_Rank, HomeTeam as Team from vRankSummary)
	) t
	group by Team
) r
LEFT JOIN vPlayerAvgRank p on p.Team = r.Team
WHERE p.position  = 'RB'
order by TotalRank

-- Wide Receiver
SELECT  r.Team, p.name as Player, p.position, r.WR_Rank, CONVERT(INT,p.[rank]) as PlayerRank, TotalRank = (r.WR_Rank*.60) + (CONVERT(INT,p.[rank]) *.40)
FROM 
(	SELECT SUM(WR_Rank) as WR_Rank, Team
	From (
		(select WR_AwayRank as WR_Rank, AwayTeam as Team from vRankSummary)
		union all
		(select WR_HomeRank as WR_Rank, HomeTeam as Team from vRankSummary)
	) t
	group by Team
) r
LEFT JOIN vPlayerAvgRank p on p.Team = r.Team
WHERE p.position  = 'WR'
order by TotalRank

-- Kicker
SELECT  r.Team, p.name as Player, p.position, r.K_Rank, CONVERT(INT,p.[rank]) as PlayerRank, TotalRank = (r.K_Rank*.60) + (CONVERT(INT,p.[rank]) *.40)
FROM 
(	SELECT SUM(K_Rank) as K_Rank, Team
	From (
		(select K_AwayRank as K_Rank, AwayTeam as Team from vRankSummary)
		union all
		(select K_HomeRank as K_Rank, HomeTeam as Team from vRankSummary)
	) t
	group by Team
) r
LEFT JOIN vPlayerAvgRank p on p.Team = r.Team
WHERE p.position  = 'K'
order by TotalRank

-- DEF
SELECT  r.Team, r.DEF_Rank
FROM 
(	SELECT SUM(DEF_Rank) as DEF_Rank, Team
	From (
		(select DEF_AwayRank as DEF_Rank, AwayTeam as Team from vRankSummary)
		union all
		(select DEF_HomeRank as DEF_Rank, HomeTeam as Team from vRankSummary)
	) t
	group by Team
) r
order by DEF_Rank

-- Quarter Back
SELECT  r.Team, p.name as Player, p.position, r.OFF_Rank, CONVERT(INT,p.[rank]) as PlayerRank, TotalRank = (r.OFF_Rank*.60) + (CONVERT(INT,p.[rank]) *.40)
FROM 
(	SELECT SUM(OFF_Rank) as OFF_Rank, Team
	From (
		(select OFF_AwayRank as OFF_Rank, AwayTeam as Team from vRankSummary)
		union all
		(select OFF_HomeRank as OFF_Rank, HomeTeam as Team from vRankSummary)
	) t
	group by Team
) r
LEFT JOIN vPlayerAvgRank p on p.Team = r.Team
WHERE p.position  = 'QB'
order by TotalRank

-- Tight End
SELECT  r.Team, p.name as Player, p.position, r.TE_Rank, CONVERT(INT,p.[rank]) as PlayerRank, TotalRank = (r.TE_Rank*.60) + (CONVERT(INT,p.[rank]) *.40)
FROM 
(	SELECT SUM(TE_Rank) as TE_Rank, Team
	From (
		(select TE_AwayRank as TE_Rank, AwayTeam as Team from vRankSummary)
		union all
		(select TE_HomeRank as TE_Rank, HomeTeam as Team from vRankSummary)
	) t
	group by Team
) r
LEFT JOIN vPlayerAvgRank p on p.Team = r.Team
WHERE p.position  = 'TE'
order by TotalRank