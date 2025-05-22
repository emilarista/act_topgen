import yaml
import argparse

argparser = argparse.ArgumentParser()

argparser.add_argument(
    "-a",
    "--act-inventory",
    dest="act_inv",
    action="store",
    help="ACT downloaded inventory file.",
)

argparser.add_argument(
    "-i",
    "--inventory",
    dest="ansible_inv",
    action="store",
    default="inventory.yml",
    help="Target ansible inventory to update.",
)

options = argparser.parse_args()
sourcefile = options.act_inv
updatetarget = options.ansible_inv

def recursiveSearchAndReplace(nesteddict, host, updatedIp, path=()):
    if hasattr(nesteddict, 'items'):
        for subdict, contents in nesteddict.items():
            if hasattr(contents, 'items'):
                if "hosts" in contents:
                    if host in contents["hosts"]:
                        print(f"{host}: {contents["hosts"][host]["ansible_host"]} -> {updatedIp}" )
                        contents["hosts"][host]["ansible_host"] = updatedIp
            if subdict == "children":
                path = path+(subdict,)
                recursiveSearchAndReplace(contents, host, updatedIp, path)
            if hasattr(contents, 'items'):
                if "children" in contents:
                    path = path+(subdict,)
                    recursiveSearchAndReplace(contents, host, updatedIp, path)


def update(sourcefile, updatetarget):
    # Read source data
    with open(sourcefile, "r") as f1:
        act_inv = yaml.load(f1.read(), Loader=yaml.SafeLoader)

    # Read target data
    with open(updatetarget, "r") as f2:
        ansible_inv = yaml.load(f2.read(), Loader=yaml.SafeLoader)

    # Build dict of all hosts from downloaded ACT inventory
    veoshosts = act_inv["all"]["children"]["VEOS"]["hosts"]

    for host, info in veoshosts.items():
        recursiveSearchAndReplace(ansible_inv, host, info["ansible_host"])

    # Build dict of all hosts from downloaded ACT inventory
    if "SERVERS" in ansible_inv["all"]["children"] and "GENERIC" in act_inv["all"]["children"]:
        print("Updating SERVER IPs")
        serverhosts = act_inv["all"]["children"]["GENERIC"]["hosts"]

    for host, info in serverhosts.items():
        recursiveSearchAndReplace(ansible_inv, host, info["ansible_host"])

    # CVP Update:
    if "CLOUDVISION" in ansible_inv["all"]["children"] and "CVP" in act_inv["all"]["children"]:
        print("Updating CVP IPs")
        print(f"{ansible_inv["all"]["children"]["CLOUDVISION"]["hosts"]["cvp"]["ansible_host"]} -> {act_inv["all"]["children"]["CVP"]["hosts"]["cv_server"]["ansible_host"]}")
        ansible_inv["all"]["children"]["CLOUDVISION"]["hosts"]["cvp"]["ansible_host"] = act_inv["all"]["children"]["CVP"]["hosts"]["cv_server"]["ansible_host"]

    # Dump updated inventory to file
    with open(updatetarget, "w") as f:
        f.write(yaml.dump(ansible_inv, sort_keys=False))

if __name__ == "__main__":
    update(sourcefile, updatetarget)