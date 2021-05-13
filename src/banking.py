import statistics
import helpers
from contribution import Contribution


class Banking:
    def __init__(self, file_path):
        self.data = helpers.read_yaml(file_path)
        self.datacenters = Datacenters(self.data['server'])
        self.branches = Branches(self.data['branch'])
        self.atms = ATMs(self.data['atm'])
        self.cns = CardNetworks(self.data['cn'])
        self.usage = self.datacenters.usage
        self.usage += self.branches.usage
        self.usage += self.atms.usage
        self.usage += self.cns.usage

        self.usage_contributions = {
                'DataCenters': self.datacenters.usage,
                'Branches': self.branches.usage,
                'ATMs': self.atms.usage,
                'Card Networks': self.cns.usage,
                }

    def __repr__(self):
        rep = 'Banking System ...............'
        rep += " {:.2f} TWh/yr".format(self.usage)
        rep += '\n\n'
        rep += self.alignment('\t')

        return rep

    def __str__(self):
        print_str = 'Banking System ...............'
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


class Datacenters(Contribution):

    def get_usage(self):
        op_hours = self.data['hours']

        deposits_total = self.data['total_deposit_100']
        deposits_boa = self.data['boa']['total_deposit']

        num_dc_boa = self.data['boa']['num_dc']
        num_dc = deposits_total * num_dc_boa / deposits_boa

        area_dc = self.data['dc_area']
        demand_per_area = self.data['server_demand_per_sq_ft']

        total_dc_demand = num_dc * area_dc * demand_per_area
        self.usage = helpers.kw_to_tw(total_dc_demand * op_hours)


class Branches(Contribution):
    def get_usage(self):
        num_per_100k_adults = self.data['num_per_100k_adults']
        bus_usage = self.ave_bus_usage()
        num_branches = round(helpers.pop() * num_per_100k_adults / 100_000, 0)
        self.usage = helpers.kw_to_tw(num_branches * bus_usage)

    def ave_bus_usage(self):
        us_bus = self.data['business']['us']
        uk_bus = self.data['business']['uk']

        us_res = self.data['residential']['us']
        uk_res = self.data['residential']['uk']
        mexico_res = self.data['residential']['mexico']
        china_res = statistics.mean(self.data['residential']['china'].values())

        us_ratio = us_bus / us_res
        uk_ratio = uk_bus / uk_res
        ratio = statistics.mean([us_ratio, uk_ratio])

        mexico_bus = ratio * mexico_res
        china_bus = ratio * china_res

        return statistics.mean([us_bus, uk_bus, mexico_bus, china_bus])


class ATMs(Contribution):
    def get_usage(self):
        op_hours = self.data['hours']
        single_atm_demand = self.data['demand']
        num_per_100k_adults = self.data['num_per_100k_adults']
        num_atms = round(helpers.pop() * num_per_100k_adults / 100_000, 0)
        self.usage = helpers.kw_to_tw(num_atms * single_atm_demand * op_hours)


class CardNetworks(Contribution):
    def get_usage(self):
        op_hours = self.data['hours']
        total_area_visa_dc = sum(self.data['visa']['facility'].values())
        server_demand_per_sq_ft = self.data['server_demand_per_sq_ft']
        visa_usage = total_area_visa_dc * server_demand_per_sq_ft * op_hours
        visa_btx = self.data['visa']['b_tx']
        total_btx = self.data['b_tx']
        self.usage = helpers.kw_to_tw(visa_usage / visa_btx * total_btx)
