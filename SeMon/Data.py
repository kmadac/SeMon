__author__ = 'kmadac'

from fabric.api import env, run
from fabric.exceptions import NetworkError
import yaml
import datetime
import copy

class Collector(object):
    def __init__(self, servers, path_results='./semon_results.yaml'):
        self.path_results = path_results
        if isinstance(servers, str):
            self.servers = [servers]
        else:
            self.servers = servers
        self.commands = {'hostname': 'hostname',
                         'uptime': "uptime | cut -d',' -f 1",
                         'product_name': 'cat /sys/class/dmi/id/product_name',
                         'em1_mac': 'cat /sys/class/net/em1/address',
                         'p1p1_mac': 'cat /sys/class/net/p1p1/address',
                         'eth0_mac': 'cat /sys/class/net/eth0/address'}

    def run_commands(self):
        """
        Runs commands on each server over ssh and returns list of dictionaries:
         [{'server': '192.168.122.104', 'p1p1 mac': '', 'uptime': '00:03:12 up  2:07', 'hostname': 'ubuntu',...}, ]
        If server is not reachable, empty result set is returned and list looks like this:
         [{'server': '192.168.122.104'}, ]
        """
        result_data = []

        for server in self.servers:
            env.host_string = server
            result_server = {'server': server, 'update_time': datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}
            for name, command in self.commands.iteritems():
                try:
                    result = run(command, quiet=True)
                except NetworkError:
                    result_server['online'] = False
                    break

                result_server['online'] = True

                if result.return_code == 0:
                    result_server[name] = str(result)
                else:
                    result_server[name] = ''

            result_data.append(result_server)

        return result_data

    def save_results_yaml(self):
        """
        Get data and save all data (removes all old data)
        """
        results = self.run_commands()
        yaml.dump(results, stream=file(self.path_results, 'w'))
        return True

    def update_results_yaml(self):
        """
        Compare data with existing data.
        If server which is not reachable is included in old data, old data will stay, and it will just put
        online: False into dictionary.
        """
        results_new = self.run_commands()
        results_old = self.load_results_yaml()

        results = []
        # merge both results
        for result_new in results_new:
            updated_server_results = copy.deepcopy(result_new)
            for result_old in results_old:
                if result_old['server'] == result_new['server'] and not result_new['online']:
                    updated_server_results = copy.deepcopy(result_old)
                    updated_server_results['update_time'] = result_new['update_time']
                    updated_server_results['online'] = False

            results.append(updated_server_results)

        yaml.dump(results, stream=file(self.path_results, 'w'))
        return True

    def load_results_yaml(self):
        results = []
        try:
            results = yaml.load(file(self.path_results, 'r'))
        except IOError:
            pass
        return results

