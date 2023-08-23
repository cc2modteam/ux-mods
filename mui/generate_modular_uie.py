#!/usr/bin/env python3
"""
Populate "Modular" UI enhancer mod files.
"""
import argparse
from pathlib import Path

HERE = Path(__file__).parents[1].absolute()

UI_ENHANCER_QUANTX = HERE / "CC2-UI-Enhancer" / "ui_enhancer" / "source" / "scripts"
MOD_DEVKIT = Path("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Carrier Command 2\\mod_dev_kit"
                  ) / "source" / "scripts"

LIBRARY_FILES = [
    "library_ui.lua",
    "library_util.lua",
    "library_vehicle.lua",
]

HEADER = "-- Part of UI Enhancer by QuantX"

EXCLUDE = [
    "screen_menu_quit.lua",
    "screen_placeholder.lua",
    "screen_intro_main.lua",
    "screen_intro_shuttle.lua",
]

GROUPED = {
    "screen_propulsion": "helm",
    "screen_navigation": "helm",
    "screen_compass": "helm",

    "screen_damage": "info",
    "screen_ship_log": "info",
    "screen_currency": "info",
    "screen_delivery_log": "info",
    "screen_landing": "info",
    "screen_weapons_anti_air": "info",
    "screen_weapons_anti_missile": "info",
    "screen_weapons_support": "info",
    "screen_cctv": "info",
}

for _lib_file in LIBRARY_FILES:
    GROUPED[Path(_lib_file).stem] = "lib"


parser = argparse.ArgumentParser(description=__doc__)
grp = parser.add_mutually_exclusive_group()
grp.add_argument("--base", default=False, action="store_true",
                 help="Populate mui folders with un-modded files")
grp.add_argument("--write", default=False, action="store_true",
                 help="Create modularised UI Enhancer mods")


def uie_path(basename: str) -> Path:
    return UI_ENHANCER_QUANTX / basename


def devkit_path(basename: str) -> Path:
    return MOD_DEVKIT / basename


def file_changed(basename: str) -> bool:
    """Return True if the file is modified by ui enhancer"""
    uie = uie_path(basename)
    sdk = devkit_path(basename)
    if uie.exists() and sdk.exists():
        sdk_lines = sdk.read_text().splitlines(keepends=False)
        mod_lines = uie.read_text().splitlines(keepends=False)
        return sdk_lines != mod_lines
    return False


def modular_folder(basename: str) -> Path:
    basename = basename.lower()
    basename = GROUPED.get(basename, basename)

    name = basename.replace("screen_", "")

    return HERE / f"uie-{name}" / "content" / "scripts"


def populate(base=True):
    for script in UI_ENHANCER_QUANTX.rglob("*.lua"):
        lower = script.name.lower()
        if lower in EXCLUDE:
            continue
        if file_changed(lower):
            folder = modular_folder(script.stem.lower())
            if base:
                folder.mkdir(parents=True, exist_ok=True)
                basefile = folder / lower
                sdk_file = MOD_DEVKIT / lower
                basefile.write_bytes(sdk_file.read_bytes())
            else:
                # overwrite with ui enhancer versions
                outfile = folder / lower

                with outfile.open("w", encoding="utf-8") as output:
                    print(HEADER, file=output)
                    output.write(script.read_text(encoding="utf-8"))
                    if lower not in LIBRARY_FILES:
                        # append the three libs even if it doesn't need them
                        for lib_filename in LIBRARY_FILES:
                            lib_file = UI_ENHANCER_QUANTX / lib_filename
                            print(f"\n-- include {lib_filename} from UI Enhancer\n", file=output)
                            output.write(lib_file.read_text(encoding="utf-8"))


def run(args=None):
    opts = parser.parse_args(args)
    if opts.base:
        populate(base=True)
    elif opts.write:
        populate(base=False)


if __name__ == "__main__":
    run()
