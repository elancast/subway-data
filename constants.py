
def enum(**enums):
    return type('Enum', (), enums)

Direction = enum(UPTOWN=1, DOWNTOWN=2)
DirectionNames = {
    1: 'Uptown',
    2: 'Dwntwn',
    }

Station = enum(
    S86 = 626,
    S77 = 627,
    S68 = 628,
    S59 = 629,
    S51 = 630,
    GRAND_CENTRAL = 631,
    S33 = 632,
    S28 = 633,
    S23 = 634,
    UNION_SQUARE = 635,
    ASTOR_PLACE = 636,
    )
StationNames = {
    626: '86th',
    627: '77th',
    628: '68th',
    629: '59th',
    630: '51st',
    631: '42nd',
    632: '33rd',
    633: '28th',
    634: '23rd',
    635: '14th',
    636: 'Astr',
    }

Subway = enum(
    L6 = '6',
    L5 = '5',
    L4 = '4',
    )

Line = {}
Line[Direction.UPTOWN] = {}
Line[Direction.DOWNTOWN] = {}

""" 4 SUBWAY LINE """
Line[Direction.UPTOWN][Subway.L4] = [
    Station.UNION_SQUARE,
    Station.GRAND_CENTRAL,
    Station.S59,
    Station.S86,
    ]
Line[Direction.DOWNTOWN][Subway.L4] = [
    Station.S86,
    Station.S59,
    Station.GRAND_CENTRAL,
    Station.UNION_SQUARE,
    ]

""" 5 SUBWAY LINE (yes it's the same as the 4) """
Line[Direction.UPTOWN][Subway.L5] = [
    Station.UNION_SQUARE,
    Station.GRAND_CENTRAL,
    Station.S59,
    Station.S86,
    ]
Line[Direction.DOWNTOWN][Subway.L5] = [
    Station.S86,
    Station.S59,
    Station.GRAND_CENTRAL,
    Station.UNION_SQUARE,
    ]

""" 6 SUBWAY LINE """
Line[Direction.UPTOWN][Subway.L6] = [
    Station.ASTOR_PLACE,
    Station.UNION_SQUARE,
    Station.S23,
    Station.S28,
    Station.S33,
    Station.GRAND_CENTRAL,
    Station.S51,
    Station.S59,
    Station.S68,
    Station.S77,
    Station.S86,
    ]
Line[Direction.DOWNTOWN][Subway.L6] = [
    Station.S86,
    Station.S77,
    Station.S68,
    Station.S59,
    Station.S51,
    Station.GRAND_CENTRAL,
    Station.S33,
    Station.S28,
    Station.S23,
    Station.UNION_SQUARE,
    Station.ASTOR_PLACE,
    ]
