#!/usr/bin/env python3
#======================================================================
# Brought to you by ~ arkhyst ⟨●_●⟩
# -------------------------------- R3 ---------------------------------
# r3-lib/Core [r3]
# v/0.2-alpha
# --------------------------- INSTRUCTIONS ----------------------------
# Core module. Main framework for r3 scripts.
# --boring : Prints in plain text (so boring...).
# --blue : "Red is only for error, what's your problem???"
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
# [ ] Descriptive help page for each script.
# [ ] Stop function feels dirty, maybe I could improve the exit flow.
#======================================================================
#----------------------------------------------------------------------
#\ PRE

import sys, shutil, os, signal
from .ERR import ERR
from .Utils import goblint, get_module_info

#/ PRE
#----------------------------------------------------------------------
#\ H - Essentials

#/ H - Essentials
#----------------------------------------------------------------------
#\ SRC - Functions



#/ SRC - Functions
#----------------------------------------------------------------------
#\ SRC - Body

class Core:
    def __init__(self, id:str, argv:list, param:dict, s:bool=False, r:list=[]) -> None:
        self._info = get_module_info(id)
        self._valid:bool = True
        self._args:dict = {}
        self._err:dict = {}
        self._silent:bool = s
        self._req:list = r

        param["--help"] = False; param["-h"] = False
        self._config:list = ["boring", "red"]
        for pc in self._config: param[f"--{pc}"] = False

        for i, a in enumerate(argv):
            if a.startswith("-"):
                for p in param:
                    cp = p.rstrip("%")
                    if cp == a:
                        if p.endswith("%"):
                            try:
                                val = argv[i+1]
                                if not val.startswith("-"):
                                    self._args[cp.lstrip("-")] = val
                            except IndexError: pass
                        else:
                            self._args[cp.lstrip("-")] = True
        
        for ra in [k for k, p in param.items() if p is True]:
            if not ra.rstrip("%").lstrip("-") in self._args:
                self._valid = False
                break
        
        if self.arg("help") or self.arg("h"):
            self.print_help()
            self.stop(ERR.NO_ERROR)

        miss = [r for r in self._req if shutil.which(r) is None]
        if miss: self.stop(ERR.REQUIRED_MISSING, ', '.join(miss))

        if not self._silent:
            for pc in self._config:
                os.environ[f"R3_{pc.upper()}"] = "1" if pc in self._args else "0"
        
        signal.signal(signal.SIGINT, lambda s,f: self.stop(ERR.NO_ERROR))
        
    
    def welcome(self) -> None:
        if not self._silent:
            n=self._info.get("name").lower().replace(" ", "_")
            v=self._info.get("ver")
            goblint(f"@0@c4# @br3-pkg/@0@c2@b{n} v{v}@0\n")

    def set_err(self, d:dict) -> None:
        for k in d:
            if type(k) is int and type(d[k]) is str:
                self._err[ERR.C(k)] = d[k]
    
    def load(self) -> None:
        if not self._valid: self.stop(ERR.BAD_USAGE)
        else: self.welcome()
    
    def arg(self, a:str, d:str="") -> str|int|bool:
        return self._args.get(a, d)
    
    def stop(self, c:int, add:str="", bye:bool=True) -> None:
        if not self._silent:
            if c > ERR.NO_ERROR:
                goblint(f"\n@0@r4@b=============== ERROR =================")
                goblint(f"@r4@b# ERR[@r3{c}@r4] @r2", end="")
                if c == ERR.UNEXPECTED_ERROR: goblint("Unexpected error.")
                elif c == ERR.BAD_USAGE: goblint("Bad usage, check help page (-h).")
                elif c == ERR.REQUIRED_MISSING: goblint("Required package(s) missing.")
                else: goblint(self._err.get(c, "Unexpected error."))
                if add: goblint(f"@r4@b# => @0@r1{add}")
            elif c == ERR.NO_ERROR:
                if bye: goblint(f"\n@0@c4@b# @c2Bye bye! @c4~ @c3arkhyst ⟨●_●⟩@0")
        
        for pc in self._config: _=os.environ.pop(f"R3_{pc.upper()}", None)
        sys.exit(c)

    def print_help(self) -> None:
        goblint(f"@0@c4@b--------------- @c3HELP PAGE @c4---------------@0")
        goblint(f"@0@c4@b# @c2Usage@c4: @c0{self._info.get("usage", "")}")

        goblint(f"\n@0@c4@b------------ @c3R3 PACKAGE ARGS @c4------------@0")
        goblint(f"@0@c4@b# @c1--red@c4: @c0Changes color theme to red. (Red is cooler)")
        goblint(f"@0@c4@b# @c1--boring@c4: @c0Prints in plain text without formatting.")

#/ SRC - Body
#----------------------------------------------------------------------

# =====================================================================
