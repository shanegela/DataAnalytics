UPDATE d
SET RankNumber = drank.RankNumber
FROM [FantasyFootball].[dbo].[DefensiveTeamRank] d
JOIN (
      SELECT 
		[TeamID]
      , RankNumber = ROW_NUMBER() OVER (ORDER BY [Rank] ASC)
  FROM [FantasyFootball].[dbo].[DefensiveTeamRank]
  ) drank on d.TeamID = drank.TeamID -- AND d.Date = '2017-07-20'

SELECT t.Name, d.*
FROM [FantasyFootball].[dbo].[DefensiveTeamRank] d
LEFT JOIN dbo.Team t on d.TeamID = t.TeamID
WHERE d.Date = '2017-07-20'
ORDER BY RankNumber

UPDATE o
SET RankNumber = orank.RankNumber
FROM [FantasyFootball].[dbo].[OffensiveTeamRank] o
JOIN (
      SELECT 
		[TeamID]
      , RankNumber = ROW_NUMBER() OVER (ORDER BY [Rank] DESC)
  FROM [FantasyFootball].[dbo].[OffensiveTeamRank]
  ) orank on o.TeamID = orank.TeamID -- AND d.Date = '2017-07-20'

SELECT t.Name, o.*
FROM [FantasyFootball].[dbo].[OffensiveTeamRank] o
LEFT JOIN dbo.Team t on o.TeamID = t.TeamID
WHERE o.Date = '2017-07-20'
ORDER BY RankNumber