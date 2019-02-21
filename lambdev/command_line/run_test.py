import yaml


def main(file):
    try:
        with open(file, 'r') as f:
            sequence = yaml.load(f)
        return sequence
    except FileNotFoundError:
        print('the file {} does not exist.'.format(file))
