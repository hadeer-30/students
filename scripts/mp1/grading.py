import os
from dotenv import load_dotenv
from pathlib import Path
import github.GithubException
from github import Github
import argparse
import codecs
import json
import requests
import urllib.request
from unidiff import PatchSet

from .. import roboyml
from ..canvasgrades import CanvasGradeFile
from ..settings import *
from ..gh_settings import *

parser = argparse.ArgumentParser()
parser.add_argument('studentfile', type=Path)
parser.add_argument('gradefile', type=Path)
args = parser.parse_args()

canvas_netid_col = "SIS Login ID"
assignment = "MiniProject1 (1380186)"
max_pts = 15

repo = class_org.get_repo("MiniProject1")
pulls = repo.get_pulls(state="open")

with CanvasGradeFile(Path(args.gradefile)) as gradebook, roboyml.open(args.studentfile) as students: 
    gh2netid = lambda gh: next(s[0] for s in students.items() if s[1]["github"] == str(gh))
    marks = {netid: {} for netid in students.keys()}

    for pull in pulls:
        netid = gh2netid(pull.user.login)
        marks[netid]["pr_open"] = True
        marks[netid]["deductions"] = 0
        # marks[netid]["only_one_file_changed"] = pull.changed_files == 1 # not a good metric
        diff = urllib.request.urlopen(pull.diff_url)
        patch = PatchSet(diff, encoding=diff.headers.get_charsets()[0])
        
        marks[netid]["files_added"] = 0
        marks[netid]["files_modified"] = 0
        marks[netid]["files_deleted"] = 0
        for pf in patch:
            if pf.is_added_file:
                marks[netid]["files_added"] += 1
            elif pf.is_modified_file:
                marks[netid]["files_modified"] += 1
            elif pf.is_removed_file:
                marks[netid]["files_deleted"] += 1
        
        if marks[netid]["files_deleted"]:
            marks[netid]["deductions"] += -1
        if marks[netid]["files_modified"]:
            marks[netid]["deductions"] += -1

        print(f"{netid}: {marks[netid]}")

    print(json.dumps(marks))

    for i, graderow in enumerate(gradebook.rows):
        netid = graderow[canvas_netid_col]

        if netid in marks and "pr_open" in marks[netid] and marks[netid]["pr_open"]:
            graderow[assignment] = max_pts + marks[netid]["deductions"]
            print(f"{netid}: deducted {marks[netid]['deductions']} pts")

print(f"GH RL: {gh.rate_limiting}")
