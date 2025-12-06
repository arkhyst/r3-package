#!/usr/bin/env python3
#======================================================================
# Brought to you by ~ arkhyst ⟨●_●⟩
# -------------------------------- R3 ---------------------------------
# r3-pkg/ether_device [r3901]
# v/0.3-alpha
# req : cryptsetup
# --------------------------- INSTRUCTIONS ----------------------------
# Usage: python3 ether_device.py [-d DEVICE_LABEL] [--open|--close]
# -d : Specifies the device to work with. (default: sdb)
# --open : Opens the encrypted device.
# --close : Closes the encrypted device.
# (?) : Be careful when selecting device. DO NOT USE /DEV/SDA
# (X) : python3 ether_device.py -d sdc --open 
# ------------------------------ NOTES --------------------------------
# Requires sudo permissions. Use a STRONG password for your sudo user.
# ---------------------------- DISCLAIMER -----------------------------
# Use only with explicit permission of the system owner.
# Breaking things or getting arrested is on you, I'm just a goblin.
# ----------------------------- LICENSE -------------------------------
# Licensed under the MIT License (see LICENSE file in repo).
#======================================================================

#============================ ALPHA TABLE =============================
#------------------------------- bugs ---------------------------------
# [ ] Encrypting whole disk has bad performance when using?
#----------------------------- features -------------------------------
# [X] Better flow of creating/deleting users and mounting/unmounting.
# [X] Q prompt to create new crypted device or destroy existing one.
# [ ] Increase pythonic code style. Reduce use of subprocess where possible.
# [X] Implement formatting option when device is corrupted or unformatted.
# [ ] Allow for multiple decryption instances.
# [ ] Improve security against sudo attacks.
# [ ] Real destruction of data
# [ ] Improve goblint user feedback
#======================================================================
#----------------------------------------------------------------------
#\ PRE

import sys, os, subprocess, secrets
from passlib.hash import sha512_crypt as crypt

from r3 import Core, ERR, QA
from r3.Utils import goblint, loading

def _pre(argv) -> Core:
    c = Core("r3901", argv, { 
        "-d%": False,
        "--open": False,
        "--close": False
    }, False, ["cryptsetup"])
    c.set_err({
        1: "Device not found.",
        2: "Are you really trying to open and close at the same time?",
        3: "Could not open device. Already opened?",
        4: "Could not close device. Is it opened?",
        5: "Device is corrupted or not formatted.",
    })
    return c

if __name__ == "__main__":
    _core = _pre(sys.argv)
    _core.load() # EXIT

#/ PRE
#----------------------------------------------------------------------
#\ H - Essentials

if __name__ == "__main__":
    def run(cmd, **kwargs) -> str:
        return subprocess.run(cmd, shell=True, capture_output=True, **kwargs).stdout.decode().strip()

    def gusr() -> str:
        return run(f'find /home/ -maxdepth 1 -type d -name "s3k*" -printf "%f\n" | head -n 1')

#/ H - Essentials
#----------------------------------------------------------------------
#\ SRC - Functions

if __name__ == "__main__":
    def chk(act:str) -> None:
        if act == "min":
            e = os.path.exists(f"/sys/block/{dev}")
            if not e: _core.stop(ERR.C(1))
            elif _core.arg("open") and _core.arg("close"): _core.stop(ERR.C(2))
        else:
            usr = gusr()
            if act == "open" and usr: _core.stop(ERR.C(3))
            elif act == "close" and not usr: _core.stop(ERR.C(4))

    def open() -> None: # This could be cleaner
        chk("open")

        usr = "s3k" + secrets.token_hex(8)
        run(f"sudo cryptsetup open /dev/{dev} {usr} || exit 1")

        dir=f"/home/{usr}"
        pwd=secrets.token_hex(16) # Saving password on memory? Hmm...
        run(f"sudo useradd -s /bin/bash {usr} -m")
        run(f"sudo usermod {crypt.hash(pwd)} {usr}")

        for df in [".profile", ".bashrc", ".zshrc"]:
            run(f"printf '%s\n' 'umask 077' | sudo tee -a {dir}/{df} > /dev/null")
            run(f"sudo chown {usr}:{usr} {dir}/{df}")

        run(f"sudo mkdir {dir}/mnt")
        run(f"sudo mount /dev/mapper/{usr} {dir}/mnt")

        run(f"printf '%s\n' {pwd} | sudo tee {dir}/.creds > /dev/null")
        run(f"sudo chmod 400 {dir}/.creds")
    
        run(f"sudo chown -R {usr}:{usr} {dir}")
        run(f"sudo chmod -R 600 {dir}/mnt") # Slow?

        run(f"sudo find {dir}/mnt -type d -exec chmod 700 {{}} +") # Slow?
        run(f"sudo find {dir}/mnt -type f -name '*.sh' -exec chmod 700 {{}} +") # Slow?
        
        goblint(f"@0@c4# @c2Session started for user {usr}. Check ~/.creds for password.@0")
        subprocess.call(["sudo", "-u", usr, "-i", os.environ["SHELL"]])
        close()

    def close() -> None:
        chk("close")

        usr = gusr() # ñeh...
        run(f"sudo umount /home/{usr}/mnt")
        run(f"sudo cryptsetup close {usr}")
        run(f"sudo userdel -r {usr}")
        goblint(f"@0@c4# @c2Device closed and user {usr} deleted.@0")

    def create() -> None:
        ok = run(f"sudo blkid /dev/{dev}") != ""
        if not ok:
            fix = QA(f"@0@r2@bDevice /dev/{dev} is unformatted or corrupted. Do you want to format it now?").confirm()
            if fix: destroy(True)
            else: _core.stop(ERR.C(5))

        safe = QA(f"@0@c-y0@bThis will erase everything from /dev/{dev}. Are you sure?").confirm()
        if safe:
            run(f"sudo cryptsetup -q luksFormat /dev/{dev}")
            run(f"sudo cryptsetup open /dev/{dev} r3_crypt")
            loading(False, f"Encrypting /dev/{dev}")
            run(f"sudo mkfs.ext4 /dev/mapper/r3_crypt")
            run(f"sudo cryptsetup close /dev/mapper/r3_crypt")
            loading(True, f"Device /dev/{dev} is now encrypted.")

            if QA(f"@c1@bDo you wish to open /dev/{dev}").confirm(): open()

    def destroy(f:bool=False) -> None:
        safe = f or QA(f"@0@c-y0@bAre you sure do you want to destroy /dev/{dev}?").confirm()
        if safe:
            loading(False, f"Erasing all data from /dev/{dev}")
            run(f"sudo cryptsetup -q luksErase /dev/{dev}")
            run(f"sudo wipefs -a /dev/{dev}")
            run(f"sudo sgdisk --zap-all /dev/{dev}")
            loading(True, f"Data has been erased")
            loading(False, f"Rebuilding /dev/{dev}")
            run(f"sudo parted /dev/{dev} -- mklabel gpt mkpart primary ext4 1MiB 100%")
            run(f"sudo mkfs.ext4 -F /dev/{dev}1")
            loading(True, f"Device /dev/{dev} rebuilt")

#/ SRC - Functions
#----------------------------------------------------------------------
#\ SRC - MAIN

if __name__ == "__main__":
    dev=_core.arg("d","sdb")
    
    chk("min")

    if _core.arg("open"): open()
    elif _core.arg("close"): close()
    else:
        QA(f"@0@c1@bTell me youngz one, what do you wish to do with /dev/{dev}?").complex([
            QA.R("open", "Open the encrypted device", open),
            QA.R("close", "Close the encrypted device", close),
            QA.R("create", "Create encryption on device", create),
            QA.R("destroy", "Destroy everything on an existing device", destroy)
        ])

    _core.stop(ERR.NO_ERROR)

#/ SRC - MAIN
#----------------------------------------------------------------------

# =====================================================================
