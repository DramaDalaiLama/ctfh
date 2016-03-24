# import blockdiag
import json
import sys
import pprint

filepath = sys.argv[1]

with open (filepath, "r") as myfile:
    data=json.load(myfile)

pp = pprint.PrettyPrinter(depth=6)

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

    # Make a list of all existing groups and diagram set with instances and assigned groups
    for interface in interfaces:
        if interface['DeviceIndex'] == 0:
            for group in interface['GroupSet']:
                groups.append(group['Ref'])
                all_groups.append(group['Ref'])

    diagram_set.append({"Instance": inst, "Groups": groups})

# Make diagram output. Dict with sec groups and assigned instances
diagram_out = {}

for group in all_groups:
    diagram_out.update({group: []})
    for inst in diagram_set:
        if group in inst['Groups']:
            diagram_out[group].append(inst['Instance'])

# Create list of strings for diagram block
lines = []
for group,insts in diagram_out.iteritems():
    line = str(group+" -> "+','.join(insts))
    lines.append(line)

# Join lines for output to file
out = str("blockdiag secgr{\n\t"+'\n\t'.join(lines)+"\n}")

# pp.pprint(out)
print(out)

print()

for inst in all_instances:
    pp.pprint(get_ref(data,inst,"Tags"))