#!/usr/bin/env python3

import os
import json
import hashlib
import time
from zipfile import ZipFile
from typing import TypedDict, Union, Optional

DB_FILE = "mappings-reflexadapt.json"
DB_ID = "misteraddons/mappings-reflexadapt"
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
MAPPINGS_DIR = os.path.join(SCRIPT_DIR, "config", "inputs")
MAPPING_SUFFIX = "_v3.map"
INPUTS_DIR = "config/inputs"
DOWNLOAD_BASE_URL = "https://github.com/misteraddons/mappings-reflex_adapt/raw/main/"

# TODO: investigate the zips repo option


class RepoDbFilesItem(TypedDict):
    hash: str
    size: int
    url: Optional[str]
    overwrite: Optional[bool]
    reboot: Optional[bool]


RepoDbFiles = dict[str, RepoDbFilesItem]


class RepoDbFoldersItem(TypedDict):
    tags: Optional[list[Union[str, int]]]


RepoDbFolders = dict[str, RepoDbFoldersItem]


class RepoDb(TypedDict):
    db_id: str
    timestamp: int
    files: RepoDbFiles
    folders: RepoDbFolders
    base_files_url: Optional[str]


def create_repo_db(input_files: list[str]) -> RepoDb:
    folders: RepoDbFolders = {
        "{}/".format(INPUTS_DIR): RepoDbFoldersItem(tags=None),
        "Scripts/": RepoDbFoldersItem(tags=None),
    }

    files: RepoDbFiles = {}
    for file in input_files:
        key = "{}/{}".format(INPUTS_DIR, os.path.basename(file))
        size = os.stat(file).st_size
        md5 = hashlib.md5(open(file, "rb").read()).hexdigest()
        files[key] = RepoDbFilesItem(
            hash=md5, size=size, url=None, overwrite=False, reboot=None
        )

    updater = RepoDbFilesItem(
        hash=hashlib.md5(open("reflex_updater.sh", "rb").read()).hexdigest(),
        size=os.stat("reflex_updater.sh").st_size,
        url=DOWNLOAD_BASE_URL + "reflex_updater.sh",
        overwrite=True,
        reboot=None,
    )
    files["Scripts/reflex_updater.sh"] = updater

    return RepoDb(
        db_id=DB_ID,
        timestamp=int(time.time()),
        files=files,
        folders=folders,
        base_files_url=DOWNLOAD_BASE_URL,
    )


def remove_nulls(v: any) -> any:
    if isinstance(v, dict):
        return {key: remove_nulls(val) for key, val in v.items() if val is not None}
    else:
        return v


def generate_json(repo_db: RepoDb) -> str:
    return json.dumps(remove_nulls(repo_db), indent=4)


def main():
    map_files: list[str] = []

    # find all mapping files
    for subdir, _dirs, files in os.walk(MAPPINGS_DIR):
        for file in files:
            if file.endswith(MAPPING_SUFFIX):
                map_files.append(os.path.join(subdir, file))

    # create json repo db
    repo_db = create_repo_db(map_files)
    with open(DB_FILE, "w") as f:
        f.write(generate_json(repo_db))

    # create a zip file containing json file
    with ZipFile("{}.zip".format(DB_FILE), "w") as zf:
        zf.write(DB_FILE)


if __name__ == "__main__":
    main()
