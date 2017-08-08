SELECT DISTINCT team, LEN(team)
FROM (
	SELECT team FROM dbo.FantasyPros --61
	UNION ALL
	SELECT team FROM dbo.FantasyFootballNerd --31
	UNION ALL
	SELECT team FROM dbo.ProFootballFocus --33
	UNION ALL
	SELECT team FROM dbo.ESPN --32
) f 
ORDER BY team

/* Seed unique team code/name
DELETE FROM Team

DBCC CHECKIDENT (Team, RESEED, 0)

INSERT INTO Team ([Name], [Code])
SELECT [Name], [Code] FROM TeamTemp

SELECT * FROM TEAM
*/


/* Get potential team names and the unique teamID 
Update tt
SET tt.TeamID = t.TeamID
From TeamTranslations tt
join team t on tt.Code = t.Code

SELECT * from TeamTranslations
*/

/*
SELECT DISTINCT position, LEN(position)
FROM (
	SELECT pos as position FROM dbo.FantasyPros
	UNION ALL
	SELECT position FROM dbo.FantasyFootballNerd
	UNION ALL
	SELECT position FROM dbo.ProFootballFocus
	UNION ALL
	SELECT position FROM dbo.ESPN
) f 
ORDER BY position

SELECT *
FROM (
	SELECT pos as position, team, name, [rank] FROM dbo.FantasyPros
	UNION ALL
	SELECT position, team, name, [rank]  FROM dbo.FantasyFootballNerd
	UNION ALL
	SELECT position, team, name, [rank]  FROM dbo.ProFootballFocus
	UNION ALL
	SELECT position, team, name, [rank]  FROM dbo.ESPN
) f 
where position in ('SCB','SS','gateway')

DELETE dbo.ProFootballFocus WHERE position = 'gateway'

INSERT INTO dbo.Position (Name, [Code], Side)
SELECT Name, [Code], Side FROM dbo.positions_temp

SELECT * FROM dbo.Position
*/

/* Fantasy Pro - insert player
SELECT fp.team, 
	COALESCE(t.TeamID, tt.TeamID) as TeamID, 
	fp.name, 
	fp.pos as position, 
	COALESCE(pc.PositionID, pn.PositionID) AS PositionID, 
	fp.[rank]
FROM dbo.FantasyPros fp --402 rows
LEFT JOIN dbo.Team t on fp.team = t.code
LEFT JOIN dbo.TeamTranslations tt on fp.team = tt.Translation
LEFT JOIN dbo.Position pn on pn.Name = fp.pos
LEFT JOIN dbo.Position pc on pc.Code = fp.pos 

INSERT INTO dbo.Player (Name, TeamID, PositionID)
SELECT fp.name,
	COALESCE(t.TeamID, tt.TeamID) as TeamID, 
	COALESCE(pc.PositionID, pn.PositionID) AS PositionID
FROM dbo.FantasyPros fp --402 rows
LEFT JOIN dbo.Team t on fp.team = t.code
LEFT JOIN dbo.TeamTranslations tt on fp.team = tt.Translation
LEFT JOIN dbo.Position pn on pn.Name = fp.pos
LEFT JOIN dbo.Position pc on pc.Code = fp.pos

-- make rankings more simple

UPDATE d
SET [rank] = n.[rank]
FROM  [FantasyFootball].[dbo].[FantasyPros] d
LEFT JOIN (
	select 
	team, pos, name,
	[rank] = ROW_NUMBER() OVER(PARTITION BY pos ORDER BY [rank] ASC)
	FROM [FantasyFootball].[dbo].[FantasyPros]
) n ON d.team = n.team and d.pos = n.pos and d.name = n.name

*/

/* insert player rankings
SELECT fp.team, 
	COALESCE(t.TeamID, tt.TeamID) as TeamID, 
	fp.name, 
	pl.playerID,
	fp.pos as position, 
	COALESCE(pc.PositionID, pn.PositionID) AS PositionID, 
	fp.[rank]
FROM dbo.FantasyPros fp --402 rows
LEFT JOIN dbo.Team t on fp.team = t.code
LEFT JOIN dbo.TeamTranslations tt on fp.team = tt.Translation
LEFT JOIN dbo.Position pn on pn.Name = fp.pos
LEFT JOIN dbo.Position pc on pc.Code = fp.pos
LEFT JOIN dbo.Player pl on pl.Name = fp.Name and pl.TeamID = COALESCE(t.TeamID, tt.TeamID)
WHERE PlayerID = 201

select p.*, t.*
from dbo.Player p
left join dbo.team t on p.TeamID = t.TeamID
where p.Name = 'New York'

Update p
	Set Name = 'New York Giants'
From dbo.Player p
Where PlayerId = 201

Update p
	Set Name = 'New York Jets'
From dbo.Player p
Where PlayerId = 254

select * 
from dbo.FantasyPros
where name = 'New York'

Update p
	Set name = 'New York Giants'
from dbo.FantasyPros p
where name = 'New York' and rank = 201

Update p
	Set name = 'New York Jets'
from dbo.FantasyPros p
where name = 'New York' and rank = 254

select * from dbo.player where playerid = 202

select * from dbo.fantasypros  where name like 'Los Angeles%'

Update p
	Set name = 'Los Angeles Rams'
from dbo.FantasyPros p
where name like 'Los Angeles%' and rank = 202


Update p
	Set name = name + ' ' + team
from dbo.FantasyPros p
where name like 'Los Angeles%' and rank in (292)

select * from dbo.player where name like 'Los Angeles%'
Update p
	Set name = 'Los Angeles Chargers'
 from dbo.player p
where name like 'Los Angeles%' and PlayerID in (292)

Update p
	Set name = 'Los Angeles Rams'
 from dbo.player p
where name like 'Los Angeles%' and PlayerID in (202)

DECLARE @dataSourceID INT = 2 -- Fantasy Pros
--SELECT * from dbo.DataSource
INSERT INTO dbo.PlayerRanking (DataSourceID, TeamID, PlayerId, Rank, Date)
SELECT @dataSourceID, 
	COALESCE(t.TeamID, tt.TeamID) as TeamID, 
	pl.playerID,
	fp.[rank],
	'07/17/2017'
FROM dbo.FantasyPros fp --402 rows
LEFT JOIN dbo.Team t on fp.team = t.code
LEFT JOIN dbo.TeamTranslations tt on fp.team = tt.Translation
LEFT JOIN dbo.Position pn on pn.Name = fp.pos
LEFT JOIN dbo.Position pc on pc.Code = fp.pos
LEFT JOIN dbo.Player pl on pl.Name = fp.Name and pl.TeamID = COALESCE(t.TeamID, tt.TeamID)
*/

/* Insert players from ESPN
SELECT fp.team, 
	COALESCE(t.TeamID, tt.TeamID) as TeamID, 
	fp.name, 
	pl.PlayerID,
	fp.position, 
	COALESCE(pc.PositionID, pn.PositionID) AS PositionID, 
	fp.[rank]
FROM dbo.ESPN fp --220 rows
LEFT JOIN dbo.Team t on fp.team = t.code
LEFT JOIN dbo.TeamTranslations tt on fp.team = tt.Translation
LEFT JOIN dbo.Position pn on pn.Name = fp.position
LEFT JOIN dbo.Position pc on pc.Code = fp.position
LEFT JOIN dbo.Player pl on pl.Name = fp.Name
WHERE pl.PlayerID is null

INSERT INTO dbo.Player (Name, TeamID, PositionID)
SELECT fp.name,
	COALESCE(t.TeamID, tt.TeamID) as TeamID, 
	COALESCE(pc.PositionID, pn.PositionID) AS PositionID
FROM dbo.ESPN fp --220 rows
LEFT JOIN dbo.Team t on fp.team = t.code
LEFT JOIN dbo.TeamTranslations tt on fp.team = tt.Translation
LEFT JOIN dbo.Position pn on pn.Name = fp.position
LEFT JOIN dbo.Position pc on pc.Code = fp.position
LEFT JOIN dbo.Player pl on pl.Name = fp.Name
WHERE pl.PlayerID is null
*/

/* ESPN - insert player rankings
SELECT fp.team, 
	COALESCE(t.TeamID, tt.TeamID) as TeamID, 
	fp.name, 
	pl.playerID,
	fp.position, 
	COALESCE(pc.PositionID, pn.PositionID) AS PositionID, 
	fp.[rank]
FROM dbo.ESPN fp --402 rows
LEFT JOIN dbo.Team t on fp.team = t.code
LEFT JOIN dbo.TeamTranslations tt on fp.team = tt.Translation
LEFT JOIN dbo.Position pn on pn.Name = fp.position
LEFT JOIN dbo.Position pc on pc.Code = fp.position
LEFT JOIN dbo.Player pl on pl.Name = fp.Name and pl.TeamID = COALESCE(t.TeamID, tt.TeamID)

DECLARE @dataSourceID INT = 4 -- ESPN
--SELECT * from dbo.DataSource
INSERT INTO dbo.PlayerRanking (DataSourceID, TeamID, PlayerId, Rank, Date)
SELECT @dataSourceID, 
	pl.TeamID,
	pl.playerID,
	fp.[rank],
	'07/17/2017'
FROM dbo.ESPN fp --402 rows
LEFT JOIN dbo.Team t on fp.team = t.code
LEFT JOIN dbo.TeamTranslations tt on fp.team = tt.Translation
LEFT JOIN dbo.Position pn on pn.Name = fp.position
LEFT JOIN dbo.Position pc on pc.Code = fp.position
LEFT JOIN dbo.Player pl on pl.Name = fp.Name and pl.TeamID = COALESCE(t.TeamID, tt.TeamID)
*/

/* Insert players from Fantasy Football Nerd
SELECT fp.team, 
	COALESCE(t.TeamID, tt.TeamID) as TeamID, 
	fp.name, 
	pl.PlayerID,
	fp.position, 
	COALESCE(pc.PositionID, pn.PositionID) AS PositionID, 
	fp.[rank]
FROM dbo.FantasyFootballNerd fp
LEFT JOIN dbo.Team t on fp.team = t.code
LEFT JOIN dbo.TeamTranslations tt on fp.team = tt.Translation
LEFT JOIN dbo.Position pn on pn.Name = fp.position
LEFT JOIN dbo.Position pc on pc.Code = fp.position
LEFT JOIN dbo.Player pl on pl.Name = fp.Name and pl.TeamID = COALESCE(t.TeamID, tt.TeamID)
WHERE pl.PlayerID is null

INSERT INTO dbo.Player (Name, TeamID, PositionID)
SELECT fp.name,
	COALESCE(t.TeamID, tt.TeamID) as TeamID, 
	COALESCE(pc.PositionID, pn.PositionID) AS PositionID
FROM dbo.FantasyFootballNerd fp
LEFT JOIN dbo.Team t on fp.team = t.code
LEFT JOIN dbo.TeamTranslations tt on fp.team = tt.Translation
LEFT JOIN dbo.Position pn on pn.Name = fp.position
LEFT JOIN dbo.Position pc on pc.Code = fp.position
LEFT JOIN dbo.Player pl on pl.Name = fp.Name and pl.TeamID = COALESCE(t.TeamID, tt.TeamID)
WHERE pl.PlayerID is null
*/

/* Fantasy Football Nerd - insert player rankings
SELECT fp.team, 
	COALESCE(t.TeamID, tt.TeamID) as TeamID, 
	fp.name, 
	pl.playerID,
	fp.position, 
	COALESCE(pc.PositionID, pn.PositionID) AS PositionID, 
	fp.[rank]
FROM dbo.FantasyFootballNerd fp
LEFT JOIN dbo.Team t on fp.team = t.code
LEFT JOIN dbo.TeamTranslations tt on fp.team = tt.Translation
LEFT JOIN dbo.Position pn on pn.Name = fp.position
LEFT JOIN dbo.Position pc on pc.Code = fp.position
LEFT JOIN dbo.Player pl on pl.Name = fp.Name and pl.TeamID = COALESCE(t.TeamID, tt.TeamID)

DECLARE @dataSourceID INT = 3 -- Fantasy Football Nerd
--SELECT * from dbo.DataSource
INSERT INTO dbo.PlayerRanking (DataSourceID, TeamID, PlayerId, Rank, Date)
SELECT @dataSourceID, 
	pl.TeamID,
	pl.playerID,
	fp.[rank],
	'07/17/2017'
FROM dbo.FantasyFootballNerd fp
LEFT JOIN dbo.Team t on fp.team = t.code
LEFT JOIN dbo.TeamTranslations tt on fp.team = tt.Translation
LEFT JOIN dbo.Position pn on pn.Name = fp.position
LEFT JOIN dbo.Position pc on pc.Code = fp.position
LEFT JOIN dbo.Player pl on pl.Name = fp.Name and pl.TeamID = COALESCE(t.TeamID, tt.TeamID)
*/


/* Insert players from Pro Football Focus
-- Reverse rank - high is good, low is bad

DELETE dbo.ProFootballFocus
where rank = 99999999999999

SELECT team, position, name, rank,
	row_number() OVER(ORDER BY rank DESC) as newRank
FROM dbo.ProFootballFocus

SELECT fp.team, 
	COALESCE(t.TeamID, tt.TeamID) as TeamID, 
	fp.name, 
	pl.PlayerID,
	fp.position, 
	COALESCE(pc.PositionID, pn.PositionID) AS PositionID, 
	fp.[newRank]
FROM (
	SELECT team, position, name, rank,
		row_number() OVER(ORDER BY rank DESC) as newRank
	FROM dbo.ProFootballFocus) fp
LEFT JOIN dbo.Team t on fp.team = t.code
LEFT JOIN dbo.TeamTranslations tt on fp.team = tt.Translation
LEFT JOIN dbo.Position pn on pn.Name = fp.position
LEFT JOIN dbo.Position pc on pc.Code = fp.position
LEFT JOIN dbo.Player pl on pl.Name = fp.Name and pl.TeamID = COALESCE(t.TeamID, tt.TeamID)
WHERE pl.PlayerID is null

select p.*, t.* 
from dbo.player p
join dbo.team t on t.teamid = p.teamid
where p.name = 'J.J. Wilcox'

select *
from dbo.ProFootballFocus
where position = ''

Update f
	SET position = 'LP'
FROM dbo.ProFootballFocus f
WHERE position = '' and name = 'David Harris'

Update f
	SET position = 'OT'
FROM dbo.ProFootballFocus f
WHERE position = '' and name = 'Tom Compton'

Update f
	SET position = 'S'
FROM dbo.ProFootballFocus f
WHERE position = '' and name = 'Steven Terrell'


Update f
	SET position = 'TE'
FROM dbo.ProFootballFocus f
WHERE position = '' and name = 'Logan Paulsen'

INSERT INTO dbo.Player (Name, TeamID, PositionID)
SELECT fp.name,
	COALESCE(t.TeamID, tt.TeamID) as TeamID, 
	COALESCE(pc.PositionID, pn.PositionID) AS PositionID
FROM (
	SELECT team, position, name, rank,
		row_number() OVER(ORDER BY rank DESC) as newRank
	FROM dbo.ProFootballFocus) fp
LEFT JOIN dbo.Team t on fp.team = t.code
LEFT JOIN dbo.TeamTranslations tt on fp.team = tt.Translation
LEFT JOIN dbo.Position pn on pn.Name = fp.position
LEFT JOIN dbo.Position pc on pc.Code = fp.position
LEFT JOIN dbo.Player pl on pl.Name = fp.Name and pl.TeamID = COALESCE(t.TeamID, tt.TeamID)
WHERE pl.PlayerID is null
*/

/* Pro Football Focus - insert player rankings
Delete dbo.ProFootballFocus
Where name = 'Charles Johnson' and position!='DE'

SELECT fp.team, 
	COALESCE(t.TeamID, tt.TeamID) as TeamID, 
	fp.name, 
	pl.TeamID,
	pl.playerID,
	fp.position, 
	COALESCE(pc.PositionID, pn.PositionID) AS PositionID, 
	fp.[newRank]
FROM (
	SELECT team, position, name, rank,
		row_number() OVER(ORDER BY rank DESC) as newRank
	FROM dbo.ProFootballFocus) fp
LEFT JOIN dbo.Team t on fp.team = t.code
LEFT JOIN dbo.TeamTranslations tt on fp.team = tt.Translation
LEFT JOIN dbo.Position pn on pn.Name = fp.position
LEFT JOIN dbo.Position pc on pc.Code = fp.position
LEFT JOIN dbo.Player pl on pl.Name = fp.Name and pl.TeamID = COALESCE(t.TeamID, tt.TeamID)

DECLARE @dataSourceID INT = 1 -- Pro Football Focus
--SELECT * from dbo.DataSource
INSERT INTO dbo.PlayerRanking (DataSourceID, TeamID, PlayerId, Rank, Date)
SELECT @dataSourceID, 
	pl.TeamID,
	pl.playerID,
	fp.[newRank],
	'07/17/2017'
FROM (
	SELECT team, position, name, rank,
		row_number() OVER(ORDER BY rank DESC) as newRank
	FROM dbo.ProFootballFocus) fp
LEFT JOIN dbo.Team t on fp.team = t.code
LEFT JOIN dbo.TeamTranslations tt on fp.team = tt.Translation
LEFT JOIN dbo.Position pn on pn.Name = fp.position
LEFT JOIN dbo.Position pc on pc.Code = fp.position
LEFT JOIN dbo.Player pl on pl.Name = fp.Name  and pl.TeamID = COALESCE(t.TeamID, tt.TeamID)
*/


/* Set up game schedule

/****** Script for SelectTopNRows command from SSMS  ******/
/*
Update dbo.game_sched_temp
set team1_abbr = 'WAS'
where team1_abbr = 'WSH'

Update dbo.game_sched_temp
set team1_abbr = 'JAC'
where team1_abbr = 'JAX'

Update dbo.game_sched_temp
set team2_abbr = 'WAS'
where team2_abbr = 'WSH'

Update dbo.game_sched_temp
set team2_abbr = 'JAC'
where team2_abbr = 'JAX'
*/
INSERT INTO GameSchedule (GameWeekID, GameDate, TeamID1, TeamID2)
SELECT gw.GameWeekID
      ,CONVERT(date, day, 101) as GameDate
      ,t1.TeamID as TeamID1
      ,t2.TeamID as TeamID2
  FROM [FantasyFootball].[dbo].[game_sched_temp] g
  left join dbo.team t1 on t1.code = g.team1_abbr
  left join dbo.team t2 on t2.code = g.team2_abbr
  left join GameWeek gw on g.Week = gw.Description

  -- team1 is away 
  -- team2 is home team
*/