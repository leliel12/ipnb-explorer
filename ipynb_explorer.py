#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# FUTURES
# =============================================================================

from __future__ import unicode_literals


# =============================================================================
# DOC
# =============================================================================

__doc__ = """Constants for all oTree launcher

"""


# =============================================================================
# IMPORTS
# =============================================================================

import os
import subprocess
import atexit
import webbrowser
import sys

from six.moves import tkinter
from six.moves import tkinter_messagebox as messagebox
from six.moves import tkinter_tkfiledialog as filedialog
from six.moves import tkinter_ttk as ttk


# =============================================================================
# CONSTANTS
# =============================================================================

WEB_BROWSER_WAIT = 5 * 1000

HOME_DIR = os.path.expanduser("~")

IS_WINDOWS = sys.platform.startswith("win")


# =============================================================================
# MAIN FRAME
# =============================================================================

class IPYNBExplorerFrame(ttk.Frame):

    def __init__(self, root):
        ttk.Frame.__init__(self, root)

        self.proc = None

        self.do_open()


    def do_open(self):
        options = {
            'parent': self,
            'initialdir': HOME_DIR,
            'title': 'Select ipynb file',
            "defaultextension": ".ipynb",
            "filetypes": [
                ('ipynb files', '.ipynb'), ('all files', '.*')],
        }
        path = filedialog.askopenfilename(**options)
        if path:
            dirpath = os.path.abspath(os.path.dirname(path))
            self.proc = call([
                "ipython", "notebook", "--notebook-dir", dirpath, path])





# =============================================================================
# FUNCTIONS
# =============================================================================

def clean_proc(proc):
    """Clean process if is still runing on exit"""
    if proc.poll() is None:
        kill_proc(proc)


def call(command, *args, **kwargs):
    """Call an external command"""
    cleaned_cmd = [cmd.strip() for cmd in command if cmd.strip()]
    if IS_WINDOWS:
        win_cmd = "{} < Nul".format(" ".join(cleaned_cmd))
        proc = subprocess.Popen(win_cmd, shell=True, *args, **kwargs)
    else:
        proc = subprocess.Popen(
            cleaned_cmd, preexec_fn=os.setsid, *args, **kwargs)
    atexit.register(clean_proc, proc)
    return proc


def run():

    # create gui
    root = tkinter.Tk()
    root.option_add("*tearOff", False)

    root.geometry("500x530+50+50")
    root.title("ipynb Launcher")

    frame = IPYNBExplorerFrame(root)
    root.mainloop()

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    run()
