import yaml


# Read yaml data file
def read_yaml(file_path):
    with open(file_path) as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def read_data_yaml():
    data_file = './rsc/data.yaml'
    return read_yaml(data_file)


def kw_to_gw(kw):
    return kw * 10 ** -6


def kw_to_tw(kw):
    return kw * 10 ** -9


def pop():
    data = read_data_yaml()
    return data['pop']['global'] * data['pop']['percent_adults']


def conversion():
    data = read_data_yaml()
    return data['conversion']
