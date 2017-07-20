/* insert team translations
insert into dbo.TeamTranslations (Code, Translation, TeamID)
select code, substring(Translation,0,LEN(Translation) - CHARINDEX(' ',reverse(translation))+1) as Translation, teamid
from dbo.TeamTranslations
where CHARINDEX(' ', Translation) > 1
*/

--select * from dbo.TeamTranslations


select r.[date],
	LTRIM(RTRIM(r.team)) as Team,
	tt.TeamID,
	tt.Code,
	r.[rank]
from dbo.defensive_team_ranks_temp r
left join dbo.TeamTranslations tt on LTRIM(RTRIM(r.team)) = tt.Translation
where tt.Code is not null

insert into dbo.DefensiveTeamRank (Date, TeamID, Rank)
select r.[date],
	tt.TeamID,
	r.[rank]
from dbo.defensive_team_ranks_temp r
left join dbo.TeamTranslations tt on LTRIM(RTRIM(r.team)) = tt.Translation
where tt.Code is not null

select * from  dbo.DefensiveTeamRank