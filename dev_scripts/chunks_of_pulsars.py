import os
import glob

from psrqpy import QueryATNF

from psrdb.tables.pulsar import Pulsar
from psrdb.graphql_client import GraphQLClient
from psrdb.utils.other import setup_logging

def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

# PSRDB setup
logger = setup_logging()
client = GraphQLClient(os.environ.get("PSRDB_URL"), False, logger=logger)
puslar_client = Pulsar(client, os.environ.get("PSRDB_TOKEN"))
puslar_client.get_dicts = True
puslar_client.set_use_pagination(True)

pulsars = []
# Query based on provided parameters
pulsar_data = puslar_client.list()
for pulsar in pulsar_data:
    if "_" in pulsar['name']:
        continue
    pulsar_name = pulsar['name']

    if pulsar_name in [
            "J1939-6342", # J0437 mislabeled
            "J1924-2914", # J0437 mislabeled
            "J2052-3640", # J0437 mislabeled
            "J2214-3835", # J0437 mislabeled
            "J0710-1604", # Perhaps a candidate that wasn't detectable
            "J2003-0934", # A craft candidate
            "J1823-3022", # A trapum candidate
        ]:
        continue

    if pulsar_name in [
            "J1644-4657",
            "J1444-6026",
            "J1835-09242",
            "J0024-7204F",
            "J2140-2310B",
            "J1402-5021", # Missing archive files
        ]:
        # Skipping because single TPA detections with no template
        continue

    pulsars.append(pulsar_name)

print(len(pulsars))
pulsars_with_templates = []
for pulsar in pulsars:
    template = glob.glob(f"/fred/oz005/users/meerpipe/templates/*/*/{pulsar}.std")
    if len(template) > 0:
        pulsars_with_templates.append(pulsar)
print(len(pulsars_with_templates))

query = QueryATNF(psrs=pulsars_with_templates).pandas

print(len(query))

for pulsar_chunk in chunk_list(list(query.sort_values("P0")["PSRJ"]), 100):
    print(",".join(pulsar_chunk))