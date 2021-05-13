import statistics
import helpers
from contribution import Contribution


class Bitcoin:
    def __init__(self, file_path):
        self.data = helpers.read_yaml(file_path)
        self.miners = Miners(self.data['miners'])
        self.pools = Pools(self.data['pools'])
        self.nodes = Nodes(self.data['nodes'])
        self.usage = self.miners.usage + self.pools.usage + self.nodes.usage
        self.usage_contributions = {
                'Miners': self.miners.usage,
                'Pools': self.pools.usage,
                'Nodes': self.nodes.usage,
                }

    def __repr__(self):
        rep = 'Bitcoin Network ...............'
        rep += " {:.2f} TWh/yr".format(self.usage)
        rep += '\n\n'
        rep += self.alignment('\t')

        return rep

    def __str__(self):
        print_str = 'Bitcoin Network ...............'
        print_str += " {:.2f} TWh/yr".format(self.usage)
        print_str += '\n\n'
        print_str += self.alignment('\t')

        return print_str

    def alignment(self, tabs=''):
        res = ''
        max_pad = 28
        max_num_char = 0

        # Get max number of characters in each value in order to get proper
        # number of '.' and ' ' on value print
        for k, v in self.usage_contributions.items():
            value = '{:.2f}'.format(v)
            value_len = len(value)
            if value_len > max_num_char:
                max_num_char = value_len

        for k, v in self.usage_contributions.items():
            # Number of characters in value name
            first_len = len(k)
            value = '{:.2f}'.format(v)
            # Number of characters in value
            second_len = len(value)
            # Align value wrt char length of longest value
            diff_len = max_num_char - second_len
            # Number of dots is the dfference of `max_pad` and the combined key
            # and value character length
            num_dots = max_pad - (first_len + second_len)

            # Create resulting string
            res += tabs + k
            res += ' '
            res += '.' * (num_dots - diff_len)
            res += ' ' * (diff_len + 1)
            res += value
            res += ' TWh/yr'
            res += '\n'

        return res


class Miners(Contribution):
    def get_usage(self):
        self.usage = helpers.kw_to_tw(self.data['usage'])
        self.demand = helpers.kw_to_gw(self.data['demand'])


class Pools(Contribution):
    def get_usage(self):
        self.usage = 1
        op_hours = self.data['hours']
        server_demand = self.data['demand']
        total_blocks_mined = sum(self.data['blocks_mined'].values())

        slush_blocks_mined = self.data['blocks_mined']['SlushPool']
        num_slush_servers = sum(self.data['slush_servers'].values())
        slushpool_demand = num_slush_servers * server_demand

        self.usage = helpers.kw_to_tw(
            slushpool_demand /
            slush_blocks_mined *
            total_blocks_mined *
            op_hours)


class Nodes(Contribution):
    def get_usage(self):
        hardware_demand = statistics.mean(
            self.data['hardware_demand'].values())
        self.usage = helpers.kw_to_tw(
            self.data['num'] * self.data['hours'] * hardware_demand)
