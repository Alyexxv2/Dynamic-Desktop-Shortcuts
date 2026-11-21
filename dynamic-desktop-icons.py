#!/usr/bin/env python3
import os
import subprocess
import time
import gi
import warnings
import re
gi.require_version("Gtk", "3.0")
from gi.repository import Gio, GLib, Gtk

# please read readme.md as usual. small summary here:
#this is for defualt app desktop icons. if you use or edit my code please credit me. either @alyexxv2 on twitter (github should have up-to-date if this is incorrect) or use my github account.
# avoid editing code if you are unsure of what it does, it may break things!! only create and remove entries in the SHORTCUTS dictionary. instructions below with my entry:
# as it uses MIME types, apps must be compatible with it (e.g., terminals will not work)
#to run, run the command python3 ~/.local/bin/update-desktop-icons.py in the terminal or as a startup command. Replace update-desktop-icons.py with the path to the script you can also use chmod +x to run it as a normal application


SHORTCUTS ={ #all shortcuts you want to change must be in here.

    "browser": { #information about my browser shortcut. PLEASE CHANGE ANYTHING THATS DIFFERENT. 7596_iexplore.0 MIGHT NOT BE AN ICON [made in linux mint]. replace "browser" with the app you want to do

        "PATH": os.path.expanduser("~/Desktop/browser.desktop"), #shortcut path, os.path.expanduser is unneeded if the path is outside user folder (it'll do nothing).
        "MIME_TYPE": "x-scheme-handler/http", #MIME type of app, reference https://www.freedesktop.org/wiki/Specifications/shared-mime-info-spec or /usr/share/mime/packages/freedesktop.org.xml if youre unsure what to use
        "FALLBACK_ICON": "7596_iexplore.0", # whichever icon you want if an icon cant be found for whichever reason.
        "FALLBACK_EXEC": "xdg-open https://" #same thing but for the exec= line. None in either of these will cause the shortcut to be skipped if a default app cant be found, or if either its exec and icon cannot be found.

}
    }


def get_default_app_details(mime_type, fallback_icon, fallback_exec): #grabs the icon and opening command

    default_app = Gio.AppInfo.get_default_for_type(mime_type, False) #finds the app from mime_type

    icon_path = fallback_icon #sets icon_path to the fallback
    cmd = fallback_exec
    if default_app: #if the app exists, it will try to override the fallback unless the icon cannot be found. Will also find exec
        icon = default_app.get_icon()
        cmd = default_app.get_commandline()
        cmd = re.sub(r'\s+%[uUFdDnNickvm]', '',cmd).strip()
        if isinstance(icon, Gio.FileIcon):
            icon_path = icon.get_file().get_path()
        elif isinstance(icon, Gio.ThemedIcon):
            icon_theme = Gtk.IconTheme.get_default()
            for name in icon.get_names():
                icon_info = icon_theme.lookup_icon(name, 128, 0)
                if icon_info:
                    icon_path = icon_info.get_filename()
                    break


    return icon_path, cmd

def update_shortcut_icon(target_app): #updates the shortcut. takes in data from each entry in the SHORTCUTS dictionary
    shortcut_path = target_app["PATH"]
    icon_path, cmd = get_default_app_details(target_app["MIME_TYPE"], target_app["FALLBACK_ICON"], target_app["FALLBACK_EXEC"])
    if not icon_path or not os.path.exists(shortcut_path) or not cmd: #making sure each one exists before running code. comment out/remove not icon_path or not cmd if you intend to leave them as None
        if not icon_path:
            warnings.warn("!!could not find app icon for {shortcut_path} and no fallback was set!! Is there no set default?", UserWarning)
        if not os.path.exists(shortcut_path):
            warnings.warn("!!shortcut {shortcut_path} does not exist. fallbacks will be used instead!!", UserWarning)
        if not cmd:
            warnings.warn("!!app execute command for {shortcut_path} could not be found and no fallback was set!! Is there no set default?", UserWarning)
        if not cmd or not icon_path:
            warnings.warn("!!skipping {shortcut_path}, script will continue!!", UserWarning)
            return

    with open(shortcut_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = [] # changes the icon path in the .desktop file itself

    for line in lines:
        if line.startswith("Icon="):
            new_lines.append(f"Icon={icon_path}\n")
        elif line.startswith("Exec="):
            new_lines.append(f"Exec={cmd}\n")
        else:
            new_lines.append(line)

    with open(shortcut_path, "w", encoding="utf-8") as f: #updates the file
        f.writelines(new_lines)
    print("shortcut {shortcut_path} updated.")

def on_change(*args): #called when a default app or theme is changed
    time.sleep(0.2)
    for i in SHORTCUTS:
        update_shortcut_icon(SHORTCUTS[i])


def on_dir_changed(monitor, file, other_file, event_type):
    if file and "mimeapps" in file.get_basename():
        on_change()

icon_theme = Gtk.IconTheme.get_default()
icon_theme.connect("changed", on_change) #theme change call of on_change

monitors = [] #whenever a default app is changed, call on_change
for folder in ["~/.config", "~/.local/share/applications"]:
    path = os.path.expanduser(folder)
    if os.path.isdir(path):
        d = Gio.File.new_for_path(path)
        m = d.monitor_directory(Gio.FileMonitorFlags.NONE, None)
        m.connect("changed", on_dir_changed)
        monitors.append(m)

on_change()
GLib.MainLoop().run()
