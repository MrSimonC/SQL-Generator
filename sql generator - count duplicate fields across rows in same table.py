import itertools

print_this = '''DECLARE @resultants TABLE
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
SELECT '''
initial_list = ['DOB', 'SiteID', 'PostCode', 'FirstName', 'LastName', 'Female', 'PinNumber']
for length in range(len(initial_list), 2, -1):
    for subset in itertools.combinations(initial_list, length):
        print_this += f"'{len(subset)}' 'Duplicate Count', first.ID, second.ID 'DupID', "
        
        # SELECT fields
        for item in initial_list:
            written = False
            for item_sub in subset:
                if item == item_sub: # entering if it exists
                    written = True
                    print_this +=  f'first.{item_sub}, '
                    break
            if not written:
                print_this += f"'' '{item}', " # or '' 'field' if not
        
        # FROM & WHERE
        print_this += '\nFROM tblAccount first, tblAccount second\nWHERE first.ID < second.ID AND first.Deleted IS NULL AND second.Deleted IS NULL AND NOT EXISTS (select * from @resultants r WHERE r.ID = first.ID and r.DupID = second.ID) AND '
        
        # WHERE continued: first.field = second.field
        for item in initial_list: 
            written = False
            for item_sub in subset:
                if item == item_sub:
                    written = True
                    print_this +=  f'first.{item_sub} = second.{item_sub} AND '
                    break
        # clean up the bottom section (bit hacky!)
        print_this = print_this.replace(' AND \n', '\n')
        print_this += '\n\nINSERT INTO @resultants ([Duplicate Count], ID, DupID, DOB, SiteID, PostCode, FirstName, LastName, Female, PinNumber)\nSELECT '
        print_this = print_this.replace(', \n', '\n')
print_this = print_this.replace('AND \n\nUNION ALL\n\nSELECT ', '')

print(print_this)