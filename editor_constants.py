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

FONT_INFO_HEADER = ('Segoe UI', 10)

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

#

"""
Script CE_AdjustTier [
    :s{ $params$=:s{:s} :s}

    :i $printf$ %s("Adjusting tier %g in structure %h...") $g$=%GLOBAL%$tier$ $h$=%GLOBAL%$structure$
    
    // Is this even a valid structure?
    :i if NOT $GlobalExists$ $name$=%GLOBAL%$structure$
        :i $printf$ %s("  Global struct did not exist.")
        :i return
    :i endif
    
    // Get the structure, this dereferences it for easy access.
    // Makes the code more readable, really.
    :i $progression_struct$ = (~%GLOBAL%$structure$)
    
    // Does this even contain the tier?
    :i if NOT $StructureContains$ $structure$=%GLOBAL%$progression_struct$ %GLOBAL%$tier$
        :i $printf$ %s("  Tier was not a part of the structure.")
        :i return
    :i endif
    
    // Now get the tier, we'll append things to it.
    :i $tier_struct$ = (%GLOBAL%$progression_struct$ -> %GLOBAL%$tier$)
    
    // Append our parameters to it.
    :i $tier_struct$ = :s{
        :i %GLOBAL%$tier_struct$
        :i %GLOBAL%$params$
    :i :s}
    
    // Now we need to throw our NEW tier into our progression struct.
    // AddToGlobalStruct is part of WTDE's modding API.
    
    :i $printf$ %s("  Patching globalmap progression structure...")
    :i $AddToGlobalStruct$ $id$=%GLOBAL%$structure$ $field$=%GLOBAL%$tier$ $element$=%GLOBAL%$tier_struct$

    :i endfunction
]
"""