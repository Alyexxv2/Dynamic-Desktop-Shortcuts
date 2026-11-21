# Dynamic-Desktop-Shortcuts
Shortcuts for default apps based on MIME type. Automatically updates when defaults are changed and has scheduled updates to catch app deletions

This is meant for Linux Mint, specifically the cinnamon desktop. Full compatibility is not guarenteed with other desktop enviroments!!! Although it will probably just be delayed icon updating. I will mark my experience (and others' if it comes up) with different DEs.
Cinnamon 6.6 - works flawlessly
KDE Plasma 6.8 - Icons take awhile to update

# Installation
This is a general section on how to install it. The process is very simple (and not super strict)! ! !

1) download dynamic-desktop-icons.py
2) move it into ~/.local/bin (or another folder if you prefer)

two different ways from here

#1 - chmod: 
    i) run chmod +x ~/.local/bin/dynamic-desktop-icons.py (or wherever else you have it)
    ii) add it to startup applications so it starts with your system
    
#2 - python 3:
    i) add as a custom command in startup applications. The command is python3 ~/.local/bin/dynamic-desktop-icons.py (or wherever else you have it)
    

    

# Limitations
The script does have a few limitations, and it depends on how your distro handles default applications and MIME types.

#1: terminals arent compatible
#2: shortcuts can be broad or missing


# How to Customize
It is really simple! 
There is a dictionary at the top of the script containing each shortcut you want. You just input the path to the shortcut, the MIME type, and a fallback icon/exec if the script fails to find a default
MIME types can be found here: https://www.freedesktop.org/wiki/Specifications/shared-mime-info-spec. A link to where MIME types can be referenced is inside the script for quick access aswell.

# Last Comments
Please credit me if you use my code for something. Personal use does not require it. Do not used in closed source projects as per the GNU v2.0 license. Any ideas on how to improve or any bug reports would be appreciated! you can also fix them for yourself if you like.
