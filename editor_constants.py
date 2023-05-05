# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#     G H W T     C A R E E R     E D I T O R     C O N S T A N T S
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
import os as OS

OWD = OS.getcwd()

VERSION = "1.0"

TAB_FRAME_WIDTH = 850
TAB_FRAME_HEIGHT = 650

MENU_HOVER_BG = '#FFFF80'
MENU_HOVER_FG = '#000000'

HOVER_DELAY = 0.35
TOOLTIP_WIDTH = 500

FONT_INFO = ('Segoe UI', 9)
FONT_INFO_HEADER = ('Segoe UI', 10)
FONT_INFO_TITLE_BAR = ('Segoe UI', 14)

# List of the venues, their zone PAK names, and their poster IDs.
TIER_VENUE_LIST = [
    ["Phi Psi Kappa", 'z_frathouse', 'Frat_Poster'],
    ["Wilted Orchid", 'z_goth', 'Goth_Poster'],
    ["Bone Church", 'z_cathedral', 'bone_Poster'],
    ["Pang Tang Bay", 'z_harbor', 'Hongkong_Poster'],
    ["Amoeba Records", 'z_recordstore', 'amobea_Poster'],
    ["Tool", 'z_tool', 'Tool_Poster'],
    ["Swamp Shack", 'z_bayou', 'Bayou_Poster'],
    ["Rock Brigade", 'z_military', 'aircraft_Poster'],
    ["Strutter's Farm", 'z_fairgrounds', 'statefair_Poster'],
    ["House of Blues", 'z_hob', 'hob_Poster'],
    ["Ted's Tiki Hut", 'z_hotel', 'Tiki_Poster'],
    ["Will Heilm's Keep", 'z_castle', 'Castle_Poster'],
    ["Recording Studio", 'z_studio2', 'Studio_01_Poster'],
    ["AT&T Park", 'z_ballpark', 'sf_ballpark_Poster'],
    ["Tesla's Coil", 'z_scifi', 'Voltage_Poster'],
    ["Ozzfest", 'z_metalfest', 'Ozzfest_Poster'],
    ["Times Square", 'z_newyork', 'Times_Poster'],
    ["Sunna's Chariot", 'z_credits', 'WOW_Poster']
]
""" A constant of the type `list[list[str]]` that contains 3 things: The venue name, its zone PAK, and its poster ID. """

# Order of the gig posters in WT. This seems very hit-or-miss...
TIER_ID_ORDER = [1, 2, 3, 4, 5, 6, 7, 8, 14, 15, 9, 16, 10, 11, 12, 13, 18, 17]
""" ID list of Tiers in the program's execution. Maybe this works? """

# Help text list.
# finalList = []
# with (open(resource_path('res/help.txt'))) as helpFile:
#     for (line) in (helpFile): finalList.append(line)

# HELP_TEXT = finalList
# """ The list holding all Help text. """