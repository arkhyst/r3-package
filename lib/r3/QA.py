#!/usr/bin/env python3
#======================================================================
# Brought to you by ~ arkhyst ⟨●_●⟩
# -------------------------------- R3 ---------------------------------
# r3-lib/QA [r3]
# v/0.1-alpha
# --------------------------- INSTRUCTIONS ----------------------------
# Question-Answer module. Execute functions depending on user input.
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

from .Utils import goblint

#/ PRE
#----------------------------------------------------------------------
#\ H - Essentials

#/ H - Essentials
#----------------------------------------------------------------------
#\ SRC - Functions

def sp_input(pre:str, suf:str) -> str:
    pass

#/ SRC - Functions
#----------------------------------------------------------------------
#\ SRC - Body

class QA:
    class R:
        def __init__(self, i:str, t:str="", f=lambda *a,**ka:None):
            self.inp:str = i
            self.text:str = t
            self.fn = f

    def __init__(self, t:str):
        self.text:str = t
    
    def confirm(self) -> bool:
        return self.short(["yes", "no"]) == "yes"

    # ol: list of options
    def short(self, ol:list=[]) -> str:
        q:str = ""
        q += "@0@c3@b--------------------------------------\n"
        q += f"@c1@b{self.text}@0@c0"
        if ol: q += " ("

        for o in ol: q += f"{o}/"
        if ol: q += "\b)"

        goblint(q, end="")

        ans:str = ""
        valid:bool = False
        while not valid:
            goblint(f"@c4@b: @0@c0", end="")
            ans = input().lower().replace(" ", "_")
            
            valid = not ol
            for o in ol:
                if o == ans:
                    valid = True
                    goblint("\r\033[K", end="")
            
            if not valid:
                goblint(f"@rb0NOT VALID. Try again c:@0", end="")
                goblint(f"\033[F\033[K", end="", flush=True)
                goblint(f"{q}", end="")

        return ans

    # rl: list of QA.R
    def complex(self, rl:list=[]) -> None:
        q:str = ""
        q += f"@0@c1@b{self.text}\n"
        q += "@0@c3@b--------------------------------------\n@0"

        for r in rl:
            if isinstance(r, QA.R):
                q += f"@0@c3[@c0@b {r.inp} @0@c3] @0@c0@b{r.text}\n"
        
        goblint(q, end="")

        valid:bool = False
        while not valid:
            goblint(f"@c4@b> @0@c0", end="")
            ans:str = input().lower().replace(" ", "_")
            
            valid = not rl
            for r in rl:
                if isinstance(r, QA.R) and r.inp == ans:
                    valid = True
                    goblint("\r\033[K", end="")
                    r.fn()
                    break
            
            if not valid:
                goblint(f"@rb0NOT VALID. Try again c:@0", end="")
                goblint(f"\033[F\033[K", end="", flush=True)

#/ SRC - Body
#----------------------------------------------------------------------

# =====================================================================
