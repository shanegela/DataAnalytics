DROP VIEW vPlayerAvgRank
GO

CREATE VIEW vPlayerAvgRank AS
select team, position, name, avg(CONVERT(INT,[rank])) as [rank], COUNT([rank]) as counter
from  (
	select team, position, name, [rank] from nfl
	union all
	select team, position, name, [rank]  from footballdb
) t
group by team, position, name
having COUNT([rank]) >= 2
--order by team, position, name

Go

select * from vPlayerAvgRank