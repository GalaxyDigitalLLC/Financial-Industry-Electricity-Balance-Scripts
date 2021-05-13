import helpers


class Gold:
    def __init__(self, file_path, contrib_str='\n'):
        self.contrib_str = contrib_str
        data = helpers.read_yaml(file_path)
        self.data = data['Production']
        self.get_usage()
        self.get_ghge()

    def get_usage(self):
        convert = helpers.conversion()
        tCO2e_per_kwh = convert['lb_per_tonne'] / convert['lb_co2_per_kwh']
        self.usage_contributions = {
                k: helpers.kw_to_tw(v * tCO2e_per_kwh)
                for k, v in self.data.items()
                }
        self.usage = helpers.kw_to_tw(sum(self.data.values()) * tCO2e_per_kwh)

    def get_ghge(self):
        self.ghge = sum(self.data.values())

    def __repr__(self):
        rep = 'Gold Production ...............'
        rep += " {:.2f} TWh/yr".format(self.usage)
        rep += '\n'
        rep += self.alignment('\t')

        return rep

    def __str__(self):
        print_str = 'Gold Production ...............'
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
