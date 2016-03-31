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

    if isinstance(refs, list):
        result = []
        for item in refs:
            result.append(item)
    elif isinstance(refs, unicode):
        result = refs
    elif isinstance(refs, dict):
        result = refs
    return result

diagram_set = []
all_groups = []

all_instances = list_resource(data, 'AWS::EC2::Instance')

for inst in all_instances:
    try:
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
    except:
        pass

# Make diagram output. Dict with sec groups and assigned instances
diagram_out = {}

vpcs = []
for group in list(set(all_groups)):
    try:
        vpc = get_ref(data,group,"VpcId").get('Ref')
    except:
        vpc = get_ref(data,group,"VpcId")
    vpcs.append(vpc)
    diagram_out.update({group: {"Name": group, "Instances": [], "VPC": vpc}})
    for inst in diagram_set:
        if group in inst['Groups']:
            diagram_out[group]['Instances'].append(inst['Instance'])

# Form diagram groups with sec groups by vpc
vpcs = list(set(vpcs))

vpc_group_set = {}
for vpc in vpcs:
    vpc_group_set.update({vpc: []})
    for group in all_groups:
        if diagram_out[group]['VPC'] == vpc:
            vpc_group_set[vpc].append(group)

# Create list of strings for diagram block
lines = []
for group,insts in diagram_out.iteritems():
    line = str(group+" -> "+','.join(insts['Instances']))
    lines.append(line)

for vpc,groups in vpc_group_set.iteritems():
    line = "\n  group {\n" + "label=" + str(vpc) + " color=\"#cccccc\"" + ','.join(groups) + "\n}\n"
    lines.append(line)

# Set options for instance's diagram nodes and write down tags
for inst in diagram_set:
    node_size = 45 + 10 * len(inst['Tags'])
    label = inst['Instance'] + "\\n\\n"
    for tag in inst['Tags']:
        label = label + tag['Key']+"="+tag['Value']+"\\n"
    label = "\n" + inst['Instance'] +" [" + "label=\"" + label + "\", height=" + str(node_size) + ", width=400]"
    lines.append(label)

lines.append("\nspan_width=130")

# Join lines for output to file
out = str("blockdiag secgr{\n\t"+'\n\t'.join(lines)+"\n}")

# pp.pprint(out)
print(out)

# for inst in all_instances:
#     pp.pprint(get_ref(data,inst,"Tags"))

# print diagram_out
# print vpc_group_set