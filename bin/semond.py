__author__ = 'kmadac'

import time
import sys
import os.path

import SeMon.Data


def main():
    if len(sys.argv) >= 2:
        while True:
            semon = SeMon.Data.Collector(['192.168.122.104'], sys.argv[1])
            semon.update_results_yaml()
            time.sleep(60)
    else:
        print "usage: python {0} path_to_reson_file".format(os.path.basename(sys.argv[0]))

if __name__ == "__main__":
    main()
