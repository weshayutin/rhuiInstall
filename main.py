#!/usr/bin/python -tt

import os
import sys
import optparse
import getpass


parser = optparse.OptionParser()
parser.add_option('-n', '--name', help='name the environment')
parser.add_option('-e', '--env', help='pick environment: ec2,local', dest='env', type='string')


(opts, args) = parser.parse_args()

# Making sure all mandatory options appeared.
if not opts.env:
    print "requires an environment"
    parser.print_help()
    exit(-1)

if __name__ == '__main__':

    print('in main')
