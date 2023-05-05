# =~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~= #
#        _____ _     _      _____    ____  ____  ____  _____ _____ ____    _____ ____  _  _____  ____  ____         #
#       /  __// \ /|/ \  /|/__ __\  /   _\/  _ \/  __\/  __//  __//  __\  /  __//  _ \/ \/__ __\/  _ \/  __\        #
#       | |  _| |_||| |  ||  / \    |  /  | / \||  \/||  \  |  \  |  \/|  |  \  | | \|| |  / \  | / \||  \/|        #
#       | |_//| | ||| |/\||  | |    |  \__| |-|||    /|  /_ |  /_ |    /  |  /_ | |_/|| |  | |  | \_/||    /        #
#       \____\\_/ \|\_/  \|  \_/    \____/\_/ \|\_/\_\\____\\____\\_/\_\  \____\\____/\_/  \_/  \____/\_/\_\        #
#                                                                                                                   #
#           Made by IMF24                       Guitar Hero SDK by Zedek the Plague Doctor, IMF24, et al.           #
# =~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~= #
# Import required modules.
from tkinter import *
from tkinter import ttk as TTK, messagebox as MSG, filedialog as FD
from tktooltip import ToolTip
from PIL import Image, ImageTk
from editor_functions import *
from editor_constants import *
import os as OS
import sys as SYS
import shutil as SHUT
import subprocess as SUB
import configparser as CF

# Set up root window.
root = Tk()
root.geometry(f"1020x719+{int(get_screen_resolution()[0] // 3.25)}+{int(get_screen_resolution()[1] // 6)}")
root.iconbitmap(resource_path('res/icon.ico'))
root.title(f"GHWT Career Editor - V{VERSION}")
root.resizable(False, False)

# Image constants.
class ImageConst():
    """ Image constants used by the GHWT Career Editor. """
    logoIMG = Image.open(resource_path('res/logo.png'))
    resizedLogoImage = logoIMG.resize((128, 128), Image.ADAPTIVE)
    LOGO_IMAGE = ImageTk.PhotoImage(resizedLogoImage)

    TIER_EDITOR_IMAGE = ImageTk.PhotoImage(Image.open(resource_path('res/icons/tier_editor.png')))

    QB_EDITOR_IMAGE = ImageTk.PhotoImage(Image.open(resource_path('res/icons/qb_editor.png')))

    # Icons for the top menus.
    class MenuIcons():
        """ Icons for the top menus. """
        NEW_CAREER_IMAGE = ImageTk.PhotoImage(Image.open(resource_path('res/menuicons/new_file.ico')))
        EXPORT_MOD_IMAGE = ImageTk.PhotoImage(Image.open(resource_path('res/menuicons/save_file.ico')))
        EXIT_EDITOR_IMAGE = ImageTk.PhotoImage(Image.open(resource_path('res/menuicons/exit_program.ico')))

        ADD_TIER_IMAGE = ImageTk.PhotoImage(Image.open(resource_path('res/menuicons/add.ico')))

        HELP_IMAGE = ImageTk.PhotoImage(Image.open(resource_path('res/menuicons/help.ico')))
        ABOUT_IMAGE = ImageTk.PhotoImage(Image.open(resource_path('res/menuicons/about.ico')))

        COMMAND_PLACEHOLDER_IMAGE = ImageTk.PhotoImage(Image.open(resource_path('res/menuicons/song_complete_star_perfect.png')))

# Add the logo on the top left.
logoImageLabel = Label(root, image = ImageConst.LOGO_IMAGE)
logoImageLabel.grid(row = 0, column = 0, padx = 5, sticky = 'nw')

# Editor tabs via the Notebook widget.
notebookFrame = Frame(root)
notebookFrame.grid(row = 0, column = 1, padx = 10)

editorTabs = TTK.Notebook(notebookFrame)
editorTabs.pack(fill = 'both', expand = 1, padx = 10)

# Add 2 frames, one for the graphical editor and the other for the QB editor.
editorCareerFrame = Frame(notebookFrame, bg = '#FFFFFF', width = TAB_FRAME_WIDTH, height = TAB_FRAME_HEIGHT)
editorCareerFrame.pack(side = 'right', fill = 'both', expand = 1)
editorQBFrame = Frame(notebookFrame, bg = '#FFFFFF', width = TAB_FRAME_WIDTH, height = TAB_FRAME_HEIGHT)
editorQBFrame.pack(side = 'right', fill = 'both', expand = 1)

# Add the tabs into the Notebook.
editorTabs.add(editorCareerFrame, text = "Tier Progression Editor", image = ImageConst.TIER_EDITOR_IMAGE, compound = 'left')
editorTabs.add(editorQBFrame, text = "QB Script Editor", image = ImageConst.QB_EDITOR_IMAGE, compound = 'left')

# The main class for the Tier Progression Editor.
class CareerEditor():
    """ The main class for the Tier Progression Editor. """
    # Update program styling.
    TTK.Style(root).configure("TButton", background = '#FFFFFF')
    TTK.Style(root).configure("TMenubutton", background = '#FFFFFF')

    editorWidgetPane = PanedWindow(editorCareerFrame, bd = 1, relief = 'sunken', bg = 'white')
    editorWidgetPane.pack(fill = 'both', expand = 1)

    # Total rows of the Career Editor tiers. Increment this each time we add a new gig.
    global totalRows
    totalRows = 0

    # Tier song rows.
    global tierSongNumbers
    tierSongNumbers = []
    """ Amount of songs each tier has. If an index has 0, it is ignored in the export logic. """

    # Tier venue names.
    global tierVenueNames
    tierVenueNames = []
    """ A global list of all venues being used. If an index has an empty string, it is ignored in the export logic. """

    # This pane is for the actual graphical editor.
    global editorBuilderPane
    editorBuilderPane = PanedWindow(editorCareerFrame, bd = 1, relief = 'sunken', bg = 'white', width = 555)
    editorWidgetPane.add(editorBuilderPane, width = 555)

    # This is the preview pane.
    global editorPreviewPane
    editorPreviewPane = PanedWindow(editorCareerFrame, bd = 1, relief = 'sunken', bg = 'white', width = 300)
    editorWidgetPane.add(editorPreviewPane)
    
    # The widgets in the editing pane itself (left pane).
    class EditorWidgets():
        """ The widgets shown in the editor pane. """
        # Add new editing row.
        def add_new_tier() -> None:
            """ Adds a new tier to be edited. """
            CareerEditor.EditorWidgets.reset_scrollregion()

            def add_new_song() -> None:
                """ Adds a new song to the tier. """
                CareerEditor.EditorWidgets.reset_scrollregion()

                # Get song checksum from song.ini file.
                def get_checksum_from_file() -> None:
                    """ Read a song.ini file, and attempt to return a checksum string. """
                    config = CF.ConfigParser(allow_no_value = True, strict = False)
                    config.optionxform = str

                    iniDir = FD.askopenfilename(title = "Select a Song Mod's INI File", filetypes = (("Song Mod INI Files", "*.ini"), ("All Files", "*.*")))

                    if (not iniDir): return

                    print(iniDir)

                    try:
                        config.clear()
                        config.read(iniDir)

                        checksumNameTest = config.get("SongInfo", "Checksum")

                        if (checksumNameTest): newSongBox.insert(0, checksumNameTest)

                    except Exception as excep:
                        MSG.showerror("INI Read Error", f"An error occurred in trying to parse the file.\n\n{excep}")
                        return

                def delete_song_row() -> None:
                    """ Delete a song row. """
                    CareerEditor.EditorWidgets.reset_scrollregion()
                    newSongLabel.destroy()
                    newSongBox.destroy()
                    newSongGetChecksum.destroy()
                    newSongDeleteRow.destroy()

                tierSongNumbers[rowID] += 1
                newSongLabel = Label(baseFrame, text = f"Song Checksum: ", bg = '#FFFFFF')
                newSongLabel.grid(row = tierSongNumbers[rowID], column = 0, padx = 5, pady = 3)
                ToolTip(newSongLabel, msg = "The checksum of the song to use for this song in the gig.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

                newSongBox = TTK.Entry(baseFrame, width = 30)
                newSongBox.grid(row = tierSongNumbers[rowID], column = 1, padx = 5, pady = 3)
                ToolTip(newSongBox, msg = "The checksum of the song to use for this song in the gig.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

                newSongGetChecksum = TTK.Button(baseFrame, width = 3, text = "...", command = get_checksum_from_file)
                newSongGetChecksum.grid(row = tierSongNumbers[rowID], column = 2, padx = 7, pady = 3)
                ToolTip(newSongGetChecksum, msg = "Select a song.ini file and pull its checksum.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

                newSongDeleteRow = TTK.Button(baseFrame, width = 3, text = "X", command = delete_song_row)
                newSongDeleteRow.grid(row = tierSongNumbers[rowID], column = 3, padx = 7, pady = 3)
                ToolTip(newSongDeleteRow, msg = "Delete this song from the gig. This cannot be undone!", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
                
            def delete_tier() -> None:
                """ Delete the current tier. """
                baseFrame.destroy()
                tierSongNumbers[rowID] = 0
                tierVenueNames[rowID] = ""
                print(tierSongNumbers)
                CareerEditor.EditorWidgets.reset_scrollregion()

            def update_venue_list(event) -> None:
                """ Update the global venue list. """
                tierVenueNames[rowID] = tierVenue.get()
                print(tierVenueNames)

            global totalRows
            tierSongNumbers.append(0)
            tierVenueNames.append("")
            totalRows = len(tierSongNumbers) - 1
            rowID = totalRows

            print(tierSongNumbers)
            print(tierVenueNames)

            baseFrame = Frame(editorBuilderWidgetFrame, bg = '#FFFFFF', width = 550)
            baseFrame.grid(row = totalRows, column = 0, columnspan = 999, sticky = 'e')

            # testLabel = Label(baseFrame, text = f"DEBUG: totalRows: {totalRows}")
            # testLabel.grid(row = 0, column = 0)

            tierVenueLabel = Label(baseFrame, text = f"(ID {totalRows + 1}): Gig Venue:   ", bg = '#FFFFFF', relief = 'flat')
            tierVenueLabel.grid(row = 0, column = 0, sticky = 'w')

            tierVenue = StringVar()
            tierVenueSelector = TTK.OptionMenu(baseFrame, tierVenue, *["<SELECT VENUE>"] + [ven[0] for ven in TIER_VENUE_LIST], command = lambda e: update_venue_list(e))
            tierVenueSelector.config(width = 30)
            tierVenueSelector.grid(row = 0, column = 1, columnspan = 2)
            ToolTip(tierVenueSelector, msg = "What venue should this gig use? This will also determine the poster texture.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

            tierAddSong = TTK.Button(baseFrame, text = "Add Song", width = 12, command = add_new_song)
            tierAddSong.grid(row = 0, column = 3, columnspan = 2, padx = 5)
            ToolTip(tierAddSong, msg = "Add a new song to this gig.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

            tierDelete = TTK.Button(baseFrame, text = "Delete Tier", width = 12, command = delete_tier)
            tierDelete.grid(row = 0, column = 5, columnspan = 2, padx = 5)
            ToolTip(tierDelete, msg = "Delete this gig from the list.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

            # Update the info in the Preview Pane.

        # Add new editing row (keyboard shortcut version).
        def add_new_tier_key(event) -> None:
            """ Add new editing row (keyboard shortcut version). """
            CareerEditor.EditorWidgets.add_new_tier()

        # Reset the editing field to allow the user to create a new career progression.
        def reset_editor() -> None:
            """ Reset the editing field to allow the user to create a new career progression. """
            if (len(editorBuilderWidgetFrame.grid_slaves()) > 0):
                if (MSG.askyesno("Reset Editor?", "Are you sure you want to discard all changes and start over? This cannot be undone!")):
                    for (slave) in (editorBuilderWidgetFrame.grid_slaves()): slave.destroy()
                    global totalRows, tierSongNumbers
                    totalRows, tierSongNumbers = 0, [0]

        # Keyboard binding version of the reset_editor() function.
        def reset_editor_key(event) -> None:
            CareerEditor.EditorWidgets.reset_editor()

        # Export the created tier progression as a QB script mod.
        def export_mod() -> None:
            """ Export the created tier progression as a QB script mod. """
            # =~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=
            # MAKE LOCAL METHODS
            # =~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=
            # Main export logic.
            def export_execute() -> None:
                """ Main export logic script. Using `mod_base.txt`, we'll build our script from there. """
                # Filter out all spaces and turn the name into upper camel casing (UpperCamelCase). We'll also use outFile as the function name.
                outFile = exportModName.get().replace(" ", "")

                print(outFile)

                # If outFile is an empty string, let's just use a fallback.
                if (not outFile): outFile = "CustomCareer"

                # We'll start with a TXT file. If we need to build a QB, we'll run this TXT file through it.
                # Import the contents of mod_base.txt into the file.
                with (open(f"{outFile}.txt", 'w')) as qbOut:
                    with (open(resource_path('res/mod_base.txt'))) as base:
                        for (line) in (base): qbOut.write(line)

                outFilePath = resource_path(f"{outFile}.txt")
                
                # Now comes the fun stuff: Read each tier, and get its songs.
                tierSongs = []

                # In the main editor field, we'll iterate through all slave frames.
                for (slave) in (editorBuilderWidgetFrame.grid_slaves()):
                    # Empty the song list.
                    songList = []

                    # Look through all slaves of the slave we're currently iterating on.
                    for (child) in (slave.grid_slaves()):
                        # Is the slave an Entry widget? If so, it's a song, and we'll get its contents.
                        if (isinstance(child, Entry)): songList.append(child.get())

                    # Append the list with its contents reversed (to correct the order).
                    tierSongs.append(reverse_list(songList))

                # Reverse tierSongs to have everything be in order!
                tierSongs = reverse_list(tierSongs)

                print(tierSongs)

                # Open the file for writing, let's get into the meat of it all!
                with (open(f"{outFile}.txt", 'a')) as qbOut:
                    debugMessage = exportDialogDebugEntry.get()

                    if (not debugMessage): debugMessage = "Setting up custom career..."

                    qbOut.write(f"Script {outFile}_Load [\n    :i $printf$ %s(\"{debugMessage}\")\n\n")

                    writeTimes = 0
                    for (i, venue) in (enumerate(tierVenueNames)):
                        if (not venue): continue

                        writeTimes += 1

                        if (writeTimes > 18):
                            MSG.showwarning("Max Tiers Exceeded", "Your setlist progression exceeds 18 tiers; the remaining tiers will be ignored.")
                            break

                        qbOut.write("    :i $CE_AdjustTier$ :s{\n        :i $structure$ = $GH4_Career_Guitar_Songs$\n")

                        qbOut.write(f"        :i $tier$ = $tier{TIER_ID_ORDER[i]}$\n")

                        qbOut.write("        :i $params$ = :s{\n")

                        songListString = ":a{ "
                        for (song) in (tierSongs[i]):
                            finalSong = tierSongs[i][-1]
                            songListString += f"${song}$ "
                        songListString += ":a}"

                        qbOut.write(f"            :i $songs$ = {songListString}\n            :i $encorep1$ = ${finalSong}$\n")

                        qbOut.write(f"            :i $level$ = $load_{venue_get_aspect('zone', venue)}$\n")
                        
                        qbOut.write(f"            :i $poster_texture$ = ${venue_get_aspect('poster', venue)}$\n")

                        qbOut.write("        :i :s}\n    :i :s}\n\n")

                    qbOut.write("    :i endfunction\n]")

                    # NOW, did we want to create a script mod or just leave it as a TXT file?
                    if (modExtension.get() == ".qb.xen"):
                        if (exportDialogSDKEntry.get() == ""):
                            MSG.showerror("No SDK Path Given", "You didn't specify the path to the SDK!")
                            exportDialogRoot.focus_force()
                            return

                        OS.chdir(exportDialogSDKEntry.get())

                        if (not OS.path.exists("sdk.js")):
                            MSG.showerror("Failed to Create Mod", "Failed to create script mod; sdk.js is not present in this folder.")
                            return
                        
                        try:
                            cmd = f"node sdk.js compile \"{outFilePath}\""

                            OS.system(cmd)

                        except Exception as excep:
                            MSG.showerror("Terminal Error", f"An error occurred when trying to parse the command through the terminal.\n\n{excep}")
                            return
                        
                        reset_working_directory()

                        # We also need to make an INI file.
                        with (open("Mod.ini", 'w')) as iniOut:
                            modName = ""
                            modDesc = ""
                            modAuthor = ""
                            modVersion = ""

                            if (not exportModININame.get()): modName = outFile

                            if (not exportModINIDesc.get()): modDesc = f"Created with GHWT Career Editor V{VERSION}"

                            if (not exportModINIAuthor.get()): modAuthor = "GHWT Career Editor"

                            if (not exportModINIVersion.get()): modVersion = "1.0"

                            outText =  "[ModInfo]\n" \
                                      f"Name={modName}\n" \
                                      f"Description={modDesc}\n" \
                                      f"Author={modAuthor}\n" \
                                      f"Version={modVersion}\n"
                            
                            iniOut.write(outText)

                # Move these files to a folder!
                if (not OS.path.exists(outFile)): OS.mkdir(outFile)
                
                filesToMove = ['Mod.ini', f'{outFile}.qb.xen', f'{outFile}.txt']

                for (file) in (filesToMove):
                    if (OS.path.exists(f"{outFile}/{file}")): OS.remove(f"{outFile}/{file}")
                    SHUT.move(file, outFile)

                # Let the user know that we're all done!
                MSG.showinfo("Mod Compiled!", "At long last, all done! Check to make sure everything looks right!")
                OS.startfile(outFile)

            # Get the path to where the user installed the Guitar Hero SDK.
            def export_get_sdk_path() -> None:
                """ Get the path to where the user installed the Guitar Hero SDK. """
                sdkDir = FD.askdirectory(title = 'Select GHSDK Install Location')

                if (not sdkDir):
                    exportDialogRoot.focus_force()
                    return

                exportDialogSDKEntry.delete(0, END)
                exportDialogSDKEntry.insert(END, sdkDir)
                exportDialogRoot.focus_force()

            # =~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=
            # OPEN EXPORT DIALOG
            # =~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=
            exportDialogRoot = Tk()
            exportDialogRoot.title("Export Script Mod")
            exportDialogRoot.config(bg = '#FFFFFF')
            exportDialogRoot.iconbitmap(resource_path('res/menuicons/save_file.ico'))
            exportDialogRoot.geometry(f"640x480+{int(get_screen_resolution()[0] // 3.25)}+{int(get_screen_resolution()[1] // 6)}")
            # exportDialogRoot.resizable(False, False)
            exportDialogRoot.focus_force()

            TTK.Style(exportDialogRoot).configure("TButton", background = '#FFFFFF')
            TTK.Style(exportDialogRoot).configure("TEntry", background = '#FFFFFF')
            TTK.Style(exportDialogRoot).configure("TMenubutton", background = '#FFFFFF')

            exportDialogHeader = Label(exportDialogRoot, text = "Export Script Mod: Export your career progression into a QB script mod.", bg = '#FFFFFF', font = FONT_INFO_HEADER)
            exportDialogHeader.grid(row = 0, column = 0, columnspan = 999, sticky = 'nw')

            exportDialogSDKLabel = Label(exportDialogRoot, text = "SDK Path: ", justify = 'right', bg = '#FFFFFF')
            exportDialogSDKLabel.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'e')
            ToolTip(exportDialogSDKLabel, msg = "Path to the Guitar Hero SDK.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

            exportDialogSDKEntry = TTK.Entry(exportDialogRoot, width = 60)
            exportDialogSDKEntry.grid(row = 1, column = 1, padx = 10, pady = 5, sticky = 'w')
            ToolTip(exportDialogSDKEntry, msg = "Path to the Guitar Hero SDK.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

            exportDialogSDKGetPath = TTK.Button(exportDialogRoot, text = '...', width = 3, command = export_get_sdk_path)
            exportDialogSDKGetPath.grid(row = 1, column = 2, sticky = 'w')
            ToolTip(exportDialogSDKGetPath, msg = "Select the directory where you have the Guitar Hero SDK installed to.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

            exportDialogDebugLabel = Label(exportDialogRoot, text = "Debug Message: ", justify = 'right', bg = '#FFFFFF')
            exportDialogDebugLabel.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = 'e')
            ToolTip(exportDialogDebugLabel, msg = "Message to be written to debug.txt when this mod gets loaded.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

            exportDialogDebugEntry = TTK.Entry(exportDialogRoot, width = 60)
            exportDialogDebugEntry.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = 'w')
            ToolTip(exportDialogDebugEntry, msg = "Message to be written to debug.txt when this mod gets loaded.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

            # =~=~=~=~=~=~=~=~=~=~= MOD.INI SETTINGS =~=~=~=~=~=~=~=~=~=~= #

            exportModINIHeader = Label(exportDialogRoot, text = "Mod.ini Settings:", bg = '#FFFFFF', font = FONT_INFO_HEADER)
            exportModINIHeader.grid(row = 3, column = 0, columnspan = 999, sticky = 'nw')

            exportModININameLabel = Label(exportDialogRoot, text = "Mod Name: ", justify = 'right', bg = '#FFFFFF')
            exportModININameLabel.grid(row = 4, column = 0, padx = 10, pady = 10, sticky = 'e')

            exportModININame = TTK.Entry(exportDialogRoot, width = 35)
            exportModININame.grid(row = 4, column = 1, padx = 10, pady = 10, sticky = 'w')

            exportModINIAuthorLabel = Label(exportDialogRoot, text = "Mod Author: ", justify = 'right', bg = '#FFFFFF')
            exportModINIAuthorLabel.grid(row = 5, column = 0, padx = 10, pady = 10, sticky = 'e')

            exportModINIAuthor = TTK.Entry(exportDialogRoot, width = 35)
            exportModINIAuthor.grid(row = 5, column = 1, padx = 10, pady = 10, sticky = 'w')

            exportModINIDescLabel = Label(exportDialogRoot, text = "Mod Description: ", justify = 'right', bg = '#FFFFFF')
            exportModINIDescLabel.grid(row = 6, column = 0, padx = 10, pady = 10, sticky = 'e')

            exportModINIDesc = TTK.Entry(exportDialogRoot, width = 60)
            exportModINIDesc.grid(row = 6, column = 1, padx = 10, pady = 10, sticky = 'w')

            exportModINIVersionLabel = Label(exportDialogRoot, text = "Mod Version: ", justify = 'right', bg = '#FFFFFF')
            exportModINIVersionLabel.grid(row = 7, column = 0, padx = 10, pady = 10, sticky = 'e')

            exportModINIVersion = TTK.Entry(exportDialogRoot, width = 15)
            exportModINIVersion.grid(row = 7, column = 1, padx = 10, pady = 10, sticky = 'w')

            # =~=~=~=~=~=~=~=~=~=~= EXPORTED MOD NAME =~=~=~=~=~=~=~=~=~=~= #

            exportModNameLabel = Label(exportDialogRoot, text = "File Name: ", justify = 'right', bg = '#FFFFFF')
            exportModNameLabel.grid(row = 8, column = 0, padx = 10, pady = 72, sticky = 'e')
            
            exportModName = TTK.Entry(exportDialogRoot, width = 60)
            exportModName.grid(row = 8, column = 1, padx = 10, pady = 72, sticky = 'w')

            global modExtension
            modExtension = StringVar()
            exportModExtension = TTK.OptionMenu(exportDialogRoot, modExtension, *[".qb.xen", ".qb.xen", ".txt"])
            exportModExtension.config(width = 15)
            exportModExtension.grid(row = 8, column = 2)
            modExtension.set(".qb.xen")

            # =~=~=~=~=~=~=~=~=~=~= EXPORT COMMANDS =~=~=~=~=~=~=~=~=~=~= #

            exportModExecute = TTK.Button(exportDialogRoot, text = "Export Script Mod", width = 25, command = export_execute)
            exportModExecute.grid(row = 9, column = 1, sticky = 'e')
            
            exportModCancel = TTK.Button(exportDialogRoot, text = "Cancel", width = 15, command = exportDialogRoot.destroy)
            exportModCancel.grid(row = 9, column = 2, padx = 3)

            exportDialogRoot.mainloop()

        # Export the mod (keyboard shortcut).
        def export_mod_key(event) -> None:
            CareerEditor.EditorWidgets.export_mod()

        # Update the Canvas scrollregion.
        def reset_scrollregion():
            """ Update the Canvas scrollregion. """
            CareerEditor.EditorWidgets.editorWidgetCanvas.configure(scrollregion = CareerEditor.EditorWidgets.editorWidgetCanvas.bbox("all"))

        # Update status bar.
        def update_status(value: str) -> None:
            editorStatusBar.config(text = value)

        editorTitleLabel = Label(editorBuilderPane, text = 'Tier Editor Pane: Build the progression for the Guitar Career.', bg = '#FFFFFF', justify = 'left', anchor = 'nw')
        editorTitleLabel.pack(anchor = 'nw')

        editorAddTier = TTK.Button(editorBuilderPane, text = "Add New Tier", width = 15, command = add_new_tier)
        editorAddTier.pack(anchor = 'nw', padx = 10, pady = 3)
        ToolTip(editorAddTier, msg = "Add a new tier to the Career progression. (CTRL + T)", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        editorCanvasFrame = Frame(editorBuilderPane, bg = '#FFFFFF', relief = 'flat')
        editorCanvasFrame.pack(fill = 'both', expand = 1, anchor = 'n')

        editorWidgetCanvas = Canvas(editorCanvasFrame, bg = '#FFFFFF', relief = 'flat')
        editorWidgetCanvas.pack(side = 'left', fill = 'both', expand = 1)

        editorCanvasScrollbar = TTK.Scrollbar(editorCanvasFrame, orient = 'vertical', command = editorWidgetCanvas.yview)
        editorCanvasScrollbar.pack(side = 'right', fill = 'y')
        editorWidgetCanvas.config(yscrollcommand = editorCanvasScrollbar.set)
        editorWidgetCanvas.bind('<Configure>', lambda e: CareerEditor.EditorWidgets.editorWidgetCanvas.config(scrollregion = CareerEditor.EditorWidgets.editorWidgetCanvas.bbox('all')))

        global editorBuilderWidgetFrame
        editorBuilderWidgetFrame = Frame(editorWidgetCanvas, bg = '#FFFFFF', width = 550)
        editorWidgetCanvas.create_window((0, 0), window = editorBuilderWidgetFrame, anchor = 'nw')

        global editorStatusBar
        editorStatusBar = Label(root, text = "", anchor = 'w', justify = 'left', relief = 'sunken', bg = '#FFFFFF', width = 145)
        editorStatusBar.grid(row = 2, column = 0, columnspan = 999, sticky = 'sw')

    # The widgets in the preview pane (right pane).
    class PreviewWidgets():
        """ The widgets shown in the preview pane. """
        previewTitleLabel = Label(editorPreviewPane, text = 'Preview Pane', bg = '#FFFFFF', justify = 'left', anchor = 'nw')
        previewTitleLabel.pack(anchor = 'nw')

        previewMasterFrame = Frame(editorPreviewPane, bg = '#FFFFFF')
        previewMasterFrame.pack(pady = 10, fill = 'both', expand = 1)

# Add top menu stuff.
class TopMenu():
    """ Add the top menus. """
    # Help text window.
    def help_window() -> None:
        pass

    # Make the base menu.
    topMenu = Menu(root)
    root.config(menu = topMenu)

    # File Menu
    fileMenu = Menu(topMenu, tearoff = False, activebackground = MENU_HOVER_BG, activeforeground = MENU_HOVER_FG)
    topMenu.add_cascade(label = "File", menu = fileMenu)
    fileMenu.add_command(label = " New Career", accelerator = "(CTRL + N)", command = CareerEditor.EditorWidgets.reset_editor, image = ImageConst.MenuIcons.NEW_CAREER_IMAGE, compound = 'left')
    fileMenu.add_command(label = " Export Script Mod...", accelerator = "(CTRL + E)", image = ImageConst.MenuIcons.EXPORT_MOD_IMAGE, compound = 'left', command = CareerEditor.EditorWidgets.export_mod)
    fileMenu.add_separator()
    fileMenu.add_command(label = " Exit", accelerator = "(SHIFT + ESC)", command = root.destroy, image = ImageConst.MenuIcons.EXIT_EDITOR_IMAGE, compound = 'left')

    # Add Menu
    addMenu = Menu(topMenu, tearoff = False, activebackground = MENU_HOVER_BG, activeforeground = MENU_HOVER_FG)
    topMenu.add_cascade(label = "Add", menu = addMenu)
    addMenu.add_command(label = " New Tier", accelerator = "(CTRL + T)", command = CareerEditor.EditorWidgets.add_new_tier, image = ImageConst.MenuIcons.ADD_TIER_IMAGE, compound = 'left')

    # Help Menu
    helpMenu = Menu(topMenu, tearoff = False, activebackground = MENU_HOVER_BG, activeforeground = MENU_HOVER_FG)
    topMenu.add_cascade(label = 'Help', menu = helpMenu)
    helpMenu.add_command(label = " About GHWT Career Editor", image = ImageConst.MenuIcons.ABOUT_IMAGE, compound = 'left')
    helpMenu.add_separator()
    helpMenu.add_command(label = " Help Pages", accelerator = "(F1)", image = ImageConst.MenuIcons.HELP_IMAGE, compound = 'left')

# Add global keybinds.
class KeyBindPresses():
    """ All global keybinds for the program. """
    # New Career
    root.bind_all('<Control-n>', lambda e: CareerEditor.EditorWidgets.reset_editor_key(e))

    # Export Script Mod...
    root.bind_all('<Control-e>', lambda e: CareerEditor.EditorWidgets.export_mod_key(e))

    # Exit
    root.bind_all('<Shift-Escape>', lambda e: root.destroy())

    # Add New Tier
    root.bind_all('<Control-t>', lambda e: CareerEditor.EditorWidgets.add_new_tier_key(e))

# Enter main loop.
root.mainloop()