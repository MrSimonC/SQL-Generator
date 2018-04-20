# SQL Generator

When a client asks to find duplicates in the same table, across 7 different fields, scoring how many fields are duplicates between different rows, it sounds easy... but it's not. Soon you'll find there's over 100 combinations...

This code produces all _combinations_ of those 7 fields and output efficient SQL code to run on a large dataset.

Example output:

```sql
DECLARE @resultants TABLE
(
    [Duplicate Count] NVARCHAR(64)
    , ID bigint
    , DupID bigint
    , DOB date
    , SiteID bigint
    , PostCode NVARCHAR(8)
    , FirstName NVARCHAR(128)
    , LastName NVARCHAR(64)
    , Female bit
    , PinNumber NVARCHAR(8)
)
INSERT INTO @resultants ([Duplicate Count], ID, DupID, DOB, SiteID, PostCode, FirstName, LastName, Female, PinNumber)
SELECT '7' 'Duplicate Count', first.ID, second.ID 'DupID', first.DOB, first.SiteID, first.PostCode, first.FirstName, first.LastName, first.Female, first.PinNumber
FROM tblAccount first, tblAccount second
WHERE first.ID < second.ID AND first.Deleted IS NULL AND second.Deleted IS NULL AND NOT EXISTS (select * from @resultants r WHERE r.ID = first.ID and r.DupID = second.ID) AND first.DOB = second.DOB AND first.SiteID = second.SiteID AND first.PostCode = second.PostCode AND first.FirstName = second.FirstName AND first.LastName = second.LastName AND first.Female = second.Female AND first.PinNumber = second.PinNumber

INSERT INTO @resultants ([Duplicate Count], ID, DupID, DOB, SiteID, PostCode, FirstName, LastName, Female, PinNumber)
SELECT '6' 'Duplicate Count', first.ID, second.ID 'DupID', first.DOB, first.SiteID, first.PostCode, first.FirstName, first.LastName, first.Female, '' 'PinNumber'
FROM tblAccount first, tblAccount second
WHERE first.ID < second.ID AND first.Deleted IS NULL AND second.Deleted IS NULL AND NOT EXISTS (select * from @resultants r WHERE r.ID = first.ID and r.DupID = second.ID) AND first.DOB = second.DOB AND first.SiteID = second.SiteID AND first.PostCode = second.PostCode AND first.FirstName = second.FirstName AND first.LastName = second.LastName AND first.Female = second.Female

```