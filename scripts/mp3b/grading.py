import os
from dotenv import load_dotenv
from pathlib import Path
#import github.GithubException
#from github import Github
import argparse
#import codecs
#import json
#import pymongo
#import requests
#import urllib.request
#from unidiff import PatchSet

from .. import roboyml
from ..canvasgrades import CanvasGradeFile
from ..settings import *
#from ..gh_settings import *

parser = argparse.ArgumentParser()
parser.add_argument('studentfile', type=Path)
parser.add_argument('gradefile', type=Path)
args = parser.parse_args()

canvas_netid_col = "SIS Login ID"
assignment = "MiniProject3 part B (1380190)"
max_pts = 5

image_exts = ['.png', '.jpg']

with CanvasGradeFile(Path(args.gradefile)) as gradebook, roboyml.open(args.studentfile) as students: 

    for i, graderow in enumerate(gradebook.rows):
        netid = graderow[canvas_netid_col]

        files = Path(f"/home/{netid}").glob(f"{netid}.*")

        images = filter(lambda f: f.suffix.lower() in image_exts, files)
        others = filter(lambda f: f.suffix.lower() not in image_exts, files)

        images = list(images)
        others = list(others)

        if len(images):
            print(f"{netid}: has {len(images)} images")
            graderow[assignment] = max_pts
        elif len(files):
            print(f"WARN: {netid}: no expected image files found, but others present, needs manual check")
        else:
            print(f"{netid}: no files matching format")

