from pybatfish.client.commands import *
from pybatfish.question.question import load_questions
from pybatfish.datamodel.flow import (HeaderConstraints,PathConstraints)
from pybatfish.question import bfq

NETWORK_NAME = "cumulus"
BASE_SNAPSHOT_NAME = "cumulus"
SNAPSHOT_PATH = "/Users/anthony/batfish/networks/example/candidate"

load_questions()

print("[*] Initializing BASE_SNAPSHOT")
bf_set_network(NETWORK_NAME)
bf_init_snapshot(SNAPSHOT_PATH, name=BASE_SNAPSHOT_NAME, overwrite=True)

bgpSessStat = bfq.bgpSessionStatus().answer().frame()
print(bgpSessStat)
if len(bgpSessStat[bgpSessStat['Established_Status'] != 'ESTABLISHED']) > 0:
  print("Not All Devices Are Established")
else:
  print("All BGP Sessions Are Good")

