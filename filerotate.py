import os
import yaml

def filerotate(fname: str,fdata: dict, root_dir:str = os.path.abspath('.')) -> None:
    """
    A function that receives a dict and converts it to a yaml file. It then
    checks if a yaml of the same name exists in the 'latest' dir and if it does
    moves it to the 'previous' dir and creates the new yaml file in the
    'latest' dir.
    """

    # create yaml file from fdata dict object to be written to a file in
    # a later step
    yaml_file = yaml.dump(fdata)

    # create variables for the dirs. These will be used for making sure they
    # exist or to create them if they don't
    latest_dir = os.path.join(root_dir,"latest")
    previous_dir = os.path.join(root_dir,"previous")

    # Create dirs if they do not exist
    all_dirs = [latest_dir, previous_dir]
    for dir in all_dirs:
        if os.path.exists(dir) == False:
            os.mkdir(dir)

    # create variables for the 'dir' + 'file name' so the can be manipulated
    # in the next step
    latest_file = os.path.join(latest_dir, fname)
    previous_file = os.path.join(previous_dir, fname)

    # logic for moving and creating yaml files to ensure we have two to
    # compare. If a file does not exist in the "previous" dir then it will
    # be created from the same yaml dump used for the file in the "latest"
    # dir
    if os.path.exists(previous_file):
        os.remove(previous_file)
    if os.path.exists(latest_file):
        os.rename(latest_file, previous_file)
    else:
        with open(previous_file, 'w') as prev_f:
            prev_f.write(yaml_file)
    with open(latest_file, 'w') as latest_f:
            latest_f.write(yaml_file)

