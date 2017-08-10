DROP VIEW vPlayerAvgRank
GO

CREATE VIEW vPlayerAvgRank AS
select Team, Position, Name, avg(CONVERT(INT,[Rank])) as [Rank], COUNT([Rank]) as counter
from  (
	select Team, Position, Name, [Rank] from NFL
	union all
	select Team, Position, Name, [Rank] from FootballDB
) t
group by Team, Position, Name
having COUNT([Rank]) >= 2
--order by team, position, name

Go

select * from vPlayerAvgRank