select r.[date],
	LTRIM(RTRIM(r.team)) as Team,
	tt.TeamID,
	tt.Code,
	r.[rank]
from dbo.offensive_team_ranks_temp r
left join dbo.TeamTranslations tt on LTRIM(RTRIM(r.team)) = tt.Translation
where tt.Code is not null


insert into dbo.OffensiveTeamRank (Date, TeamID, Rank)
select r.[date],
	tt.TeamID,
	r.[rank]
from dbo.offensive_team_ranks_temp r
left join dbo.TeamTranslations tt on LTRIM(RTRIM(r.team)) = tt.Translation
where tt.Code is not null

select * from  dbo.OffensiveTeamRank

