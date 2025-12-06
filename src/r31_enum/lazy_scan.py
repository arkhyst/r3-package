#!/usr/bin/env python3
#======================================================================
# Brought to you by ~ arkhyst ⟨●_●⟩
# -------------------------------- R3 ---------------------------------
# r3-pkg/lazy_scan [r3101]
# v/0.1-alpha
# req : nmap, masscan, ffuf, gobuster.
# --------------------------- INSTRUCTIONS ----------------------------
# Usage: python3 r3_lazy_scan.py -t TARGET -r REPORT FOLDER [-i INTERFACE] [-a LEVEL] [-v]
# -t : Defines the target host to scan. *REQ*
# -r : Defines the report folder file. *REQ*
# -i : Defines the network interface to use. eth0 by default.
# -s : Defines agressiveness level. 0-3 (0: safe, 3: extreme). 0 by default.
# -v : Outputs report contents on shell. (verbose)
# (?) : If you are connected to a VPN, remember to set -i parameter.
# (X) : python3 r3_lazy_scan.py -t 10.10.23.52 -r candy_store.txt -i tun0 -a 1
# ------------------------------ NOTES --------------------------------
# As the name suggests, this is just a lazy scan. It can miss critical
# information, alert the blue team, or return useless data.
# Report folder includes lazy_scan report and raw reports from each tool.
# ---------------------------- DISCLAIMER -----------------------------
# Use only with explicit permission of the system owner.
# Breaking things or getting arrested is on you, I'm just a goblin.
# ----------------------------- LICENSE -------------------------------
# Licensed under the MIT License (see LICENSE file in repo).
#======================================================================

#============================ ALPHA TABLE =============================
#------------------------------- bugs ---------------------------------
# [ ]
#----------------------------- features -------------------------------
# [ ]
#======================================================================
#----------------------------------------------------------------------
#\ PRE

import sys
from r3 import Core

def _pre(argv) -> Core:
    c = Core("r3101", argv, { 
        "-t%": True,
        "-r%": True,
        "-i%": False,
        "-a%": False,
        "-v": False
    }, False, ["nmap", "masscan", "ffuf", "gobuster"])
    c.set_err({
        1: "Host is not reachable",
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

def rep() -> None:
    pass

def scan() -> dict:
    d = {}
    return d

def dtl(rd:dict) -> dict:
    d = {}
    return d

#/ SRC - Functions
#----------------------------------------------------------------------
#\ SRC - MAIN

if __name__ == "__main__":
    rep()
    rd = scan()
    data = dtl(rd)


#/ SRC - MAIN
#----------------------------------------------------------------------

# =====================================================================
