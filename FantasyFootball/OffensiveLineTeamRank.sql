select
	LTRIM(RTRIM(o.team)) as Team,
	tt.TeamID,
	tt.Code,
	o.[ranking]
from [dbo].[offensive-line-rankings] o
left join dbo.Team tt on LTRIM(RTRIM(o.team)) = tt.code

insert into dbo.OffensiveLineTeamRank (Date, TeamID, [RankNumber])
select CONVERT(date, getdate()),
	tt.TeamID,
	o.[ranking]
from [dbo].[offensive-line-rankings] o
left join dbo.Team tt on LTRIM(RTRIM(o.team)) = tt.code

select * from  dbo.OffensiveLineTeamRank
