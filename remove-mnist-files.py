import string
import re
import json
import pandas as pd
from datetime import datetime
import numpy as np
import math

from collections import OrderedDict
from datetime import date

import os
import glob
import sys
from scipy.stats import shapiro
from os.path import dirname, abspath

LIPI_PATH = '/home/jamaltoutouh/euro-gp2021/lipizzaner-gan/src/'
DATASET = 'mnist'


def get_all_distributed_clients(lipizzaner_path, dataset, file_pattern):
    print(lipizzaner_path + '/output/lipizzaner_gan/distributed/' + dataset + '/*/*/' + file_pattern)
    return [filepath for filepath in glob.iglob(lipizzaner_path + '/output/lipizzaner_gan/distributed/' + dataset + '/*/*/' + file_pattern)]

def get_file_size(filename):
    st = os.stat(filename)
    return st.st_size

def get_stats(files_list):
    space_cleaned = 0
    for file_to_remove in files_list:
        if os.path.exists(file_to_remove):
            space_cleaned += get_file_size(file_to_remove)
    return space_cleaned/1024

def remove_files(files_list):
    deleted_files, undeleted_files = list(), list()
    space_cleaned = 0
    for file_to_remove in files_list:
        if os.path.exists(file_to_remove):
            space_cleaned += get_file_size(file_to_remove)
            deleted_files.append(file_to_remove)
            os.remove(file_to_remove)
        else:
            undeleted_files.append(file_to_remove)
    return deleted_files, undeleted_files, space_cleaned/(1024 * 1024)


def read_option(files_list):
    option = input('Are you sure that you want to remove {} files? [y/n]'.format(len(files_list)))
    while (option != 'y' and option != 'Y') and (option != 'n' and option != 'N'):
        option = input('Wrong option. Please select y or n')
    return (option == 'y' or option == 'Y')

def create_log_file(deleted_files, undeleted_files, space_cleaned):
    option = input('Do you want to create a log file? [y/n]')
    while (option != 'y' and option != 'Y') and (option != 'n' and option != 'N'):
        option = input('Wrong option. Please select y or n')

    if (option == 'y' or option == 'Y'):
        log_file = open('lipizzaner-cleaning.log', 'a')
        log_file.write('- Deleted {} files\n- Undeleted {} files \n- Space cleaned: {} kB'.format(len(deleted_files), len(undeleted_files), space_cleaned))
        log_file.write('Deleted files:\n')
        for file in deleted_files:
            log_file.write(file + '\n')
        for file in undeleted_files:
            log_file.write(file + '\n')
        log_file.close()



files = list()
for i in range(0, 190):
    pattern = 'fake_images-{:02d}.jpg'.format(i)
    files += get_all_distributed_clients(LIPI_PATH, DATASET, pattern)
space = get_stats(files)
print('Found {} files that uses {} MB'.format(len(files), space))
# pattern = '*.jpg'
# files = get_all_distributed_clients(LIPI_PATH, DATASET, pattern)
if read_option(files):
    print('Removing files')
    deleted_files, undeleted_files, space_cleaned = remove_files(files)
    print('End.\n - Deleted {} files\n - Undeleted {} files - Space cleaned: {} MB' .format(len(deleted_files), len(undeleted_files), space_cleaned))
    create_log_file(deleted_files, undeleted_files, space_cleaned)
else:
    print('Good bye! No files deleted.')

