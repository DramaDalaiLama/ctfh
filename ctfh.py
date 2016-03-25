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

    tags = get_ref(data,inst,"Tags")

    diagram_set.append({"Instance": inst, "Groups": groups, "Tags": tags})

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

# Set options for instance's diagram nodes and write down tags
for inst in diagram_set:
    node_size = 45 + 10 * len(inst['Tags'])
    label = inst['Instance'] + "\\n\\n"
    for tag in inst['Tags']:
        label = label + tag['Key']+"="+tag['Value']+"\\n"
    label = "\n" + inst['Instance'] +" [" + "label=\"" + label + "\", height=" + str(node_size) + ", width=200]"
    lines.append(label)

lines.append("\nspan_width=130")

# Join lines for output to file
out = str("blockdiag secgr{\n\t"+'\n\t'.join(lines)+"\n}")

# pp.pprint(out)
print(out)

# for inst in all_instances:
#     pp.pprint(get_ref(data,inst,"Tags"))