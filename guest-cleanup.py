#!/usr/bin/env python3

import sqlite3
import argparse
import datetime
import os
import shutil

##########################################
# Parse the command line arguments       #
##########################################

# Handle the userdir and database arguments
parser = argparse.ArgumentParser(description='Remove guest accounts, files and projects after use')
parser.add_argument('-p', '--prefix', type=str, default='guest_', help='Username prefix used by guest accounts')
parser.add_argument('-r', '--repodir', type=str, default='/data/repository/', help='Path to the repository directory')
parser.add_argument('-u', '--userdir', type=str, default='/data/users/', help='Path to the users directory')
parser.add_argument('-j', '--jupyterhub', type=str, default='/data/jupyterhub.sqlite', help='Path to jupyterhub db')
parser.add_argument('-d', '--database', type=str, default='/data/projects.sqlite', help='Path to projects database')

# Parse the arguments
args = parser.parse_args()


##########################################
# Remove guest spawners                  #
##########################################

# Get a connection to the database
db = None
try: db = sqlite3.connect(args.jupyterhub)
except sqlite3.Error as e:
    print(e)

# Get a list of all guest spawners older than a day
cur = db.cursor()
cur.execute(f"SELECT * FROM spawners s, users u WHERE s.user_id=u.id AND u.name LIKE '{args.prefix}%' AND s.last_activity <= date('now', '-1 days')")
spawners = cur.fetchall()

# Delete the spawner from the database
for s in spawners:
    cur.execute(f"DELETE FROM spawners WHERE id={s[0]}")

# Close the connection to the database
db.commit()
db.close()

##########################################
# Connect to projects database           #
##########################################

db = None
try: db = sqlite3.connect(args.database)
except sqlite3.Error as e:
    print(e)
cur = db.cursor()

##########################################
# Remove guest projects                  #
##########################################

cur.execute(f"DELETE FROM myprojects WHERE owner LIKE '{args.prefix}%'")

##########################################
# Remove guest shares                    #
##########################################

# Remove entries from the shares table
cur.execute(f"SELECT * FROM shares WHERE owner LIKE '{args.prefix}%'")
deleted = cur.fetchall()
cur.execute(f"DELETE FROM shares WHERE owner LIKE '{args.prefix}%'")

# Remove entries from the invites table
for p in deleted: cur.execute(f"DELETE FROM invites WHERE share_id={p[0]}")

##########################################
# Remove guest published projects        #
##########################################

# Remove entries from the projects table
cur.execute(f"SELECT * FROM projects WHERE owner LIKE '{args.prefix}%' AND updated <= date('now', '-1 days')")
deleted = cur.fetchall()
cur.execute(f"DELETE FROM projects WHERE owner LIKE '{args.prefix}%' AND updated <= date('now', '-1 days')")

# Remove entries from the updates table
for p in deleted: cur.execute(f"DELETE FROM updates WHERE project_id={p[0]}")

# Remove entries from the project_tags table
for p in deleted: cur.execute(f"DELETE FROM project_tags WHERE projects_id={p[0]}")

# Close the connection to the database
db.commit()
db.close()


##########################################
# Remove guest user directories and zips #
##########################################

def remove_guests(rootdir):
    day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
    for d in os.listdir(rootdir):
        path = os.path.join(rootdir, d)
        modified = datetime.datetime.fromtimestamp(os.stat(path).st_mtime)
        if d.startswith(args.prefix) and modified < day_ago: shutil.rmtree(path)


# Remove all published project zips
remove_guests(args.repodir)

# Remove all user and project directories
remove_guests(args.userdir)
