# import blockdiag
import json
import sys
import pprint

filepath = sys.argv[1]

with open (filepath, "r") as myfile:
    data=json.load(myfile)

pp = pprint.PrettyPrinter(depth=6)
# pp.pprint(data)

# pp.pprint(insts)

# TODO go through each instance from 'insts' list, look up their refs in security groups
# TODO do the same for security groups and subnets
# TODO form resulting .diag file with schemas describing what instances are in which sec group, show which subnets they are located


def list_resource(data, resource):
    # Make list of aws resources
    res = []
    for key in data['Resources'].keys():
        if resource in data['Resources'][key]['Type']:
            res.append(key)
    return res

def get_ref(data, resource, property):
    refs = data['Resources'][resource]['Properties'][property]
    result = []
    for item in refs:
        result.append(item)
    return result

diagram_set = []
all_groups = []

all_instances = list_resource(data, 'AWS::EC2::Instance')

for inst in all_instances:
    interfaces = get_ref(data,inst,"NetworkInterfaces")

    groups = []

    for interface in interfaces:
        if interface['DeviceIndex'] == 0:
            for group in interface['GroupSet']:
                groups.append(group['Ref'])
                all_groups.append(group['Ref'])

    diagram_set.append({"Instance": inst, "Groups": groups})

diagram_out = {}

for group in all_groups:
    diagram_out.update({group: []})
    for inst in diagram_set:
        if group in inst['Groups']:
            diagram_out[group].append(inst['Instance'])

lines = []
for key,value in diagram_out.iteritems():
    for item in value:
        line = str(key+" -> "+item)
        lines.append(line)

# pp.pprint(lines)

out = str("blockdiag secgr{\n"+'\n'.join(lines)+"\n}")

# pp.pprint(out)
print(out)