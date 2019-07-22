from pybatfish.client.commands import *
from pybatfish.question.question import load_questions
from pybatfish.datamodel.flow import (HeaderConstraints,PathConstraints)
from pybatfish.question import bfq
import logging
import sys
import re
import pandas as pd

NETWORK_NAME = "cumulus"
BASE_SNAPSHOT_NAME = "cumulus"
SNAPSHOT_PATH = "/Users/anthony/batfish/networks/example/candidate"

load_questions()

print("[*] Initializing BASE_SNAPSHOT")
bf_set_network(NETWORK_NAME)
bf_init_snapshot(SNAPSHOT_PATH, name=BASE_SNAPSHOT_NAME, overwrite=True)


#print(bfq.bgpSessionStatus().answer().frame())
bgpLeafStatus = bfq.bgpSessionStatus(nodes="/leaf/").answer().frame()
#bgpSessStatus.set_index("Node", inplace=True)
#print(bgpSessStatus.loc[['leaf01'], ['Remote_Node']])
#print(bgpSessStatus.loc['leaf01'].Remote_Node)

for index, row in bgpLeafStatus.iterrows():
	#print(row['Node'], row['Remote_Node'])
	if(re.match(r'spine', str(row['Remote_Node'])) is not None):
		print("%s Has A Matching Spine BGP Neighbor" %str(row['Node']))
	else:
		print("%s Does NOT Have A Matching Spine BGP Neighbor" %str(row['Node']))

#############################################################################################################
bgpSpineStatus = bfq.bgpSessionStatus(nodes="/spine/").answer().frame()

for index, row in bgpSpineStatus.iterrows():
        if((re.match(r'65020', str(row['Local_AS'])) is not None)):
                print("%s is Using The Correct Spine AS" %str(row['Node']))
        else:
                print("%s is NOT Using The Correct Spine AS" %str(row['Node']))

##############################################################################################################

for index, row in bgpLeafStatus.iterrows():
	if ((int((str(row['Node']).split("f"))[1])) % 2) == 0:
		#clag_peer = ("leaf0" + str((int((str(row['Node']).split("f"))[1])-1)))
		if(bgpLeafStatus.at[index-1,'Local_AS'] == row['Local_AS']):
			print("Leaf AS's Match")
		else:
			print("Leaf AS's DO NOT Match")
	else:
                if(bgpLeafStatus.at[index+1,'Local_AS'] == row['Local_AS']):
                        print("Leaf AS's Match")
                else:
                        print("Leaf AS's DO NOT Match")
