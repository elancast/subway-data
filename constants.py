def enum(**enums):
    return type('Enum', (), enums)

Direction = enum(UPTOWN=1, DOWNTOWN=2)
