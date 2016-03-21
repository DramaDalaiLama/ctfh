# import blockdiag
import json
import sys
import pprint

filepath = sys.argv[1]

with open (filepath, "r") as myfile:
    data=json.load(myfile)

pp = pprint.PrettyPrinter(depth=6)
# pp.pprint(data)

# Make list of ec2 instances
insts = []
for key in data['Resources'].keys():
    if "AWS::EC2::Instance" in data['Resources'][key]['Type']:
        insts.append(key)
# pp.pprint(insts)

# TODO