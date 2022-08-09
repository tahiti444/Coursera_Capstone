# -*- coding: utf-8 -*-

from pathlib import Path
import sys
import os

CURRENTPATH = os.path.dirname(os.path.abspath(__file__))
PROJECTPATH = Path(CURRENTPATH).parent.absolute()
LOGPATH = os.path.join(PROJECTPATH, "log")
