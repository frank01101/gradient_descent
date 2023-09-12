#!/usr/bin/env python
#-*- coding: utf-8 -*-
# author: Franciszek Humieja
# email: frank.humieja@gmail.com
# version 1.0 -- 2023-09-12

from sys import argv

def is_option(option_content, start_from = 2, arguments = argv):
   """
   Returns True when an option with content option_content is given as the start_from-th or further argument of the program call.
   """
   n = len(arguments)
   is_called = False
   for i in range(start_from, n):
      if arguments[i] == option_content:
         is_called = True
   return is_called

def find_option_arg(option_content, start_from = 2, arguments = argv):
   """
   Returns the value of the argument of the option_content option. The user should enter the arguments after the options corresponding to them (e.g. -t 0.95).
   """
   n = len(arguments)
   for i in range(start_from, n-1):
      if arguments[i] == option_content:
         option_arg = arguments[i+1]
   return option_arg
