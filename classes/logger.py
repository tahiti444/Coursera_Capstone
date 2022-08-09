# -*- coding: utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
from classes.globals import *

logFile = os.path.join(LOGPATH, "ai.log")

# create logging directory if missing
if not os.path.exists(LOGPATH):
    os.makedirs(LOGPATH)

# get logger
logger = logging.getLogger(__name__)

# FILE logger
##################################################
# the handler determines where the logs go: stdout/file
# fileHandler = logging.FileHandler(logFile, encoding='utf-8')
fileHandler = RotatingFileHandler(
    logFile, maxBytes=50000, backupCount=5, encoding="utf-8"
)
ffmt = (
    "[  %(levelname)s  ] %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
)
fileFormater = logging.Formatter(ffmt)
fileHandler.setFormatter(fileFormater)
logger.addHandler(fileHandler)

# CLI logger
##################################################
streamHandler = logging.StreamHandler()
sfmt = (
    "[  %(levelname)s  ] %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
)
streamFormater = logging.Formatter(sfmt)
streamHandler.setFormatter(streamFormater)
logger.addHandler(streamHandler)

# set a logging level
##################################################
logger.setLevel(logging.DEBUG)