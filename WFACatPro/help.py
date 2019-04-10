# -*- coding: utf-8 -*-

"""
WFACatPro.help
~~~~~~~~~~~~~~~~~~~
This is a help module.
"""


def print_help_info():
    print('= User manual =')
    print('You could analysis your weibo friends\' network with Gephi and MySQL software.')
    print('Using this python programme to produce csv file, then use Gephi. And you could only use MySQL module or Tools.')
    print('Make sure run get command to get basic data first !')
    print('- csv: First, get data. Second, analysing data and produce csv file. ')
    print('- MySQL: First, get data. Second, analysing data and store to mysql. ')
    print('- Tools: Many tools to get info about weibo user. ')
    print('By Marlous')
    print('')
    print('Some commands:')
    print('help')
    print('conf (settings info)')
    print('get (get data from internet)')
    print('tocsv (produce csv file)')
    print('tocsv (analysis data and store to MySQL (start MySQL service first!))')
    print('detail (Look some detail info about user deep analysis in MySQL)')
    print('tool (All about one user info)')
    print('quit')


if __name__ == '__main__':
    print_help_info()
