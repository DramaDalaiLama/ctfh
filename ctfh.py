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

# TODO go through each instance from 'insts' list, look up their refs in security groups
# TODO do the same for security groups and subnets
# TODO form resulting .diag file with schemas describing what instances are in which sec group, show which subnets they are located