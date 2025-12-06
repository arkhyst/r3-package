#!/usr/bin/env python3
#======================================================================
# Brought to you by ~ arkhyst ⟨●_●⟩
# -------------------------------- R3 ---------------------------------
# r3-lib/Utils [r3]
# v/0.1-alpha
# --------------------------- INSTRUCTIONS ----------------------------
# Utils module. Provides cool functions.
# ------------------------------ NOTES --------------------------------
# My momma once told me, clean yo ass before cleaning somebody else's.
# ---------------------------- DISCLAIMER -----------------------------
# Use only with explicit permission of the system owner.
# Breaking things or getting arrested is on you, I'm just a goblin.
# ----------------------------- LICENSE -------------------------------
# Licensed under the MIT License (see LICENSE file in repo)
#======================================================================

#============================ ALPHA TABLE =============================
#------------------------------- bugs ---------------------------------
# [ ] 
#----------------------------- features -------------------------------
# [ ]
#======================================================================
#----------------------------------------------------------------------
#\ PRE

#/ PRE
#----------------------------------------------------------------------
#\ H - Essentials

#/ H - Essentials
#----------------------------------------------------------------------
#\ SRC - Functions

#/ SRC - Functions
#----------------------------------------------------------------------
#\ SRC - MAIN

def path(p:str="") -> str:
    from pathlib import Path as P
    return str(P(__file__).resolve().parent.parent.parent / p.lstrip("/"))

def goblint(txt:str="", **karg) -> None:
    # I feel this could be WAY more elegant... but meh.
    clr = {
        "@0": "\033[0m", # Reset
        "@b": "\033[1m", # Bold
        "@u": "\033[4m", # Underline
        "@i": "\033[3m", # Italic
        "@c0": "\033[38;5;231m", # White : Text
        "@c1": "\033[38;5;153m", # Cyna : Subtext
        "@c2": "\033[38;5;111m", # Light Blue : Info
        "@c3": "\033[38;5;69m", # Purple : Highlight
        "@c4": "\033[38;5;27m", # Blue : Title
        "@c5": "\033[38;5;21m", # Dark Blue : Accent
        "@r0": "\033[38;5;224m", # Light Red
        "@r1": "\033[38;5;217m", # Pink 
        "@r2": "\033[38;5;210m", # Light Orange
        "@r3": "\033[38;5;203m", # Orange
        "@r4": "\033[38;5;196m", # Red
        "@r5": "\033[38;5;160m", # Dark Red
        "@c-g0": "\033[38;5;82m", # Green
        "@c-g1": "\033[38;5;193m", # Light Green
        "@c-y0": "\033[38;5;226m", # Yellow
        "@rb0": "\033[48;5;124m\033[1m\033[38;5;224m", # Red Bg
        "@ICO-ok": "\033[38;5;82m\033[1m[✔] \033[0m" # OK Icon
    }

    import os
    if os.environ.get("R3_RED", "0") == "1":
        clr["@c0"] = "\033[38;5;224m";
        clr["@c1"] = "\033[38;5;217m";
        clr["@c2"] = "\033[38;5;210m";
        clr["@c3"] = "\033[38;5;203m";
        clr["@c4"] = "\033[38;5;196m";
        clr["@c5"] = "\033[38;5;160m";

    if os.environ.get("R3_BORING", "0") == "1":
        for k, v in clr.items(): txt = txt.replace(k, "")
    else:
        for k, v in clr.items(): txt = txt.replace(k, v)
        
    print(txt, **karg)

def compile_py(src:str, on:str, s:bool=False) -> None:
    import subprocess as proc, sys, shutil
    base = path()

    loading()
    proc.run([
        sys.executable, "-m", "PyInstaller",
        "--onefile", "--windowed", "--noconfirm", "--log-level=ERROR",
        f"--distpath={base}/dist", "--workpath=/tmp/r3_build", f"--paths={path("lib")}",
        f"--specpath=/tmp/r3_build",f"--name={on}", f"{base}/{src}"
    ], stdout=proc.DEVNULL, stderr=proc.DEVNULL, check=True)
    shutil.rmtree("/tmp/r3_build")
    loading(True, f"SUCCESS @c4- @0@c1File located at @b@c-g1dist/{on}")

def run_py(p:str, a:list=[], s:bool=False) -> None:
    import subprocess, sys
    subprocess.run(["sudo" if s else "", sys.executable, path(p), *a], check=True)

def loading(d:bool=False, t:str="COMPILING"): # This is very simple, but what about a callable to execute when finished loading?
    if not d: goblint(f"@c-y0@b{t}...@0", end="", flush=True)
    else:
        from time import sleep
        goblint(f"\r\033[K", end="", flush=True)
        goblint(f"@ICO-ok@c-g0@b{t}")
        sleep(0.5) # I... I don't know if I'm comfortable with this.

def get_info() -> list:
    import configparser
    cfg = configparser.ConfigParser()
    cfg.read(path("/src/info.ini"))

    l = []
    for i in cfg:
        if i != "DEFAULT": l.append(get_module_info(i))
    
    return l

# Yeah, yeah, I can see it too. I'm a little lazy today aight?
def get_module_info(i:str) -> dict:
    import configparser
    cfg = configparser.ConfigParser()
    cfg.read(path("/src/info.ini"))

    if not i in cfg:
        return {
            "id": "r30XX",
            "name": "Module",
            "ver": "0.0-proto",
            "path": "src/goblin_wizard.py",
            "usage": "python3 goblin_wizard.py",
            "help": ""
        }
    else:
        return {
            "id": i,
            "name": cfg[i]["name"],
            "ver": cfg[i]["ver"],
            "path": cfg[i]["path"],
            "usage": cfg[i]["usage"],
            "help": ""
        }

#/ SRC - MAIN
#----------------------------------------------------------------------

# =====================================================================
