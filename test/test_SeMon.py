import SeMon.Data

__author__ = 'kmadac'

import unittest


class SeMon_TestCase(unittest.TestCase):
    def test_Collect(self):
        semon = SeMon.Data.Collector(['192.168.122.104'], path_results='/tmp/test_results.j2')
        results = semon.run_commands()
        print results
        self.assertEqual(len(results), 1)

    def test_SaveAndLoad(self):
        """
        Save and load results.
        """
        semon = SeMon.Data.Collector(['192.168.122.104'], path_results='/tmp/test_results.j2')
        ret = semon.save_results_yaml()
        self.assertEqual(ret, True)
        loadresults = semon.load_results_yaml()
        self.assertEqual(len(loadresults), 1)

if __name__ == '__main__':
    unittest.main()
