import os
from dotenv import load_dotenv
from pathlib import Path
#import github.GithubException
#from github import Github
import argparse
#import codecs
import json
import pymongo
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
assignment = "MiniProject2 (1380187)"
max_pts = 5

client = pymongo.MongoClient (host="localhost:27017")
db = client ['fdac22mp2']

with CanvasGradeFile(Path(args.gradefile)) as gradebook, roboyml.open(args.studentfile) as students: 
    gh2netid = lambda gh: next(s[0] for s in students.items() if s[1]["github"] == str(gh))

    colls = db.list_collection_names()

    for i, graderow in enumerate(gradebook.rows):
        netid = graderow[canvas_netid_col]

        if netid in colls:
            docs = list(db[netid].find())
            if len(docs):
                print(f"{netid}: has {len(docs)} entries")
                graderow[assignment] = max_pts
            else:
                print(f"{netid}: zero documents")
        else:
            print(f"{netid}: no collection found")

