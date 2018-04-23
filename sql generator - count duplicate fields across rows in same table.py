import itertools

def main():
    """Generates SQL for comparing rows in a table. Takes a list of fields to compare, 
    generates all combinations of those fields, compares each combination and counts amount"""
    sql = '''DECLARE @resultants TABLE
    (
        [Duplicate Count] NVARCHAR(64)
        , [Matched on] NVARCHAR(128)
        , ID bigint
        , DupID bigint
        , DOB date
        , SiteID bigint
        , PostCode NVARCHAR(8)
        , FirstName NVARCHAR(128)
        , LastName NVARCHAR(64)
        , Female bit
        , PinNumber NVARCHAR(8)
    )'''
    fields = ['DOB', 'SiteID', 'PostCode', 'FirstName', 'LastName', 'Female', 'PinNumber']
    for length in range(len(fields), 2, -1): # working backwards from most to least combinations
        for combinations in itertools.combinations(fields, length):
            sql += f"\n\nINSERT INTO @resultants ([Duplicate Count], [Matched on], ID, DupID, DOB, SiteID, PostCode, FirstName, LastName, Female, PinNumber)\nSELECT '{len(combinations)}' 'Duplicate Count', "
            # Matched on
            matched_on = ''
            for i, field in enumerate(fields):
                # written = False
                for combination in combinations:
                    if field == combination: # entering if it exists
                        matched_on += (f'{combination}' if len(matched_on) == 0 else f', {combination}')
                        break
            matched_on = matched_on.strip()
            sql += f"'{matched_on}' 'Matched on', first.ID, second.ID 'DupID', first.DOB, first.SiteID, first.PostCode, first.FirstName, first.LastName, first.Female, first.PinNumber"
            sql += '\nFROM tblAccount first, tblAccount second WITH(NOLOCK)\nWHERE first.ID < second.ID AND first.Deleted IS NULL AND second.Deleted IS NULL AND \n\tNOT EXISTS (select * from @resultants r WHERE r.ID = first.ID and r.DupID = second.ID)'
            # WHERE first.field = second.field
            for field in fields:
                for combination in combinations:
                    if field == combination:
                        sql +=  f" \n\tAND first.{combination} IS NOT NULL AND first.{combination} != '' AND second.{combination} IS NOT NULL AND second.{combination} != ''"
                        sql +=  f" \n\tAND first.{combination} = second.{combination}"
                        break
    sql += '\n\nSELECT * from @resultants'
    return(sql)

print(main())