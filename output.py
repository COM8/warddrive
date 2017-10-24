#!/usr/bin/python
# -*- coding: utf-8 -*-
import pickle
import sys
if __name__ == '__main__':
    try:
        with open('logFile' + '.pkl', 'rb') as f:
            loggedData = pickle.load(f)
        if len(sys.argv) >= 2:
            Thelist = sys.argv
            Thelist.pop(0)
            for (key, value) in loggedData.items():
                output = ''
                for option in Thelist:
                    try:
                        output = output + ', ' + str(option) + ': ' \
                            + str(value[option])
                    except KeyError:
                        Thelist.remove(output)
                print output
            exit(0)
        else:
            print 'no output info given'
            options = ''
            line = list(loggedData.keys())[0]
            print line
            for (key, value) in loggedData[line].items():
                options += ', ' + str(key)
            print 'options are: ' + options
            exit(-1)
    except FileNotFoundError:
        exit(-1)
