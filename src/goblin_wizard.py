#!/usr/bin/env python3
#======================================================================
# Brought to you by ~ arkhyst ⟨●_●⟩
# -------------------------------- R3 ---------------------------------
# r3-pkg/goblin_wizard [r3000]
# v/0.2-alpha
# --------------------------- INSTRUCTIONS ----------------------------
# Usage: python3 goblin_wizard.py
# ------------------------------ NOTES --------------------------------
# Goblin wizard for your convinience.
# Using r3 package scripts is more comfortable than ever.
# ---------------------------- DISCLAIMER -----------------------------
# Use only with explicit permission of the system owner.
# Breaking things or getting arrested is on you, I'm just a goblin.
# ----------------------------- LICENSE -------------------------------
# Licensed under the MIT License (see LICENSE file in repo).
#======================================================================

#============================ ALPHA TABLE =============================
#------------------------------- bugs ---------------------------------
# [ ] Looks like r3801 compilation suddenly fails.
# [ ] r3901 open device fails through goblin_wizard.
#----------------------------- features -------------------------------
# [X] Improve path handling when calling other scripts.
# [ ] r3901: Dynamic wrong device detection.
#======================================================================
#----------------------------------------------------------------------
#\ PRE

import sys, subprocess
from r3 import ERR, Core, QA
from r3.Utils import goblint, compile_py, get_info, get_module_info, path, run_py

def _pre(argv) -> Core:
    c = Core("r3000", argv, {

    })
    c.set_err({
        1: "Compilation process failed. Is PyInstaller installed on this system?",
        2: "Ether Device script failed to execute. Check script for requirements."
    })
    return c

if __name__ == "__main__":
    _core = _pre(sys.argv)
    _core.load() # EXIT

#/ PRE
#----------------------------------------------------------------------
#\ H - Essentials

#/ H - Essentials
#----------------------------------------------------------------------
#\ SRC - Functions

if __name__ == "__main__":
    def r3101(info:dict = get_module_info("r3101")) -> None: # lazy_scan
        goblint("@rb0Beep Boop Beep@0")

    def r3801(info:dict = get_module_info("r3801")) -> None: # keylogger
        goblint("I zee... Wise choice. I will compile this script into an " \
        "executable file for safety reasons.")
        ofn = QA("Executable file name").short([])
        if ofn:
            try: compile_py(info.get("path"), ofn, True)
            except subprocess.CalledProcessError as e:
                _core.stop(ERR.C(1), f"PyInstaller error: {e.returncode} {e.cmd}")

    def r3901(info:dict = get_module_info("r3901")) -> None: # ether_device
        dn = QA("Device label (/dev/sdb)").short([])
        try: run_py(info.get("path"), [dn], True)
        except subprocess.CalledProcessError as e:
            _core.stop(ERR.C(2), f"Script error: {e.returncode} {e.cmd}", False)
        _core.stop(ERR.NO_ERROR, "", False)

#/ SRC - Functions
#----------------------------------------------------------------------
#\ SRC - MAIN

if __name__ == "__main__":
    qar:list = []
    for m in get_info():
        if not m.get("id").startswith("r30"):
            qar.append(QA.R(
                m.get("id").lstrip("r3"),
                "@c1r3-pkg/@c0"+m.get("path").lstrip("src/"),
                locals()[m.get("id")]
            ))

    goblint("@0@c0Woopidy-woopidy, I'm the Goblin Wizard. I'm here to help you hack the Internetz.")
    goblint("My tower holdz powerful spells only available for thoze who are responsible and ethical.")
    QA("\n@c1@bNow tell me, which zpell do you wish to cast?").complex(qar)

    _core.stop(ERR.NO_ERROR)

#/ SRC - MAIN
#----------------------------------------------------------------------

# =====================================================================
