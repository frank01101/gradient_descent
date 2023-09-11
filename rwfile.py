#!/usr/bin/env python
#-*- coding: utf-8 -*-
# author: Franciszek Humieja
# email: frank.humieja@gmail.com
# version 1.2 -- 2023-08-26

from sys import argv

def load_raw(file_name):
    """
    Reads data from the input file and returns a string list, each element of which is one line from the input file.
    """
    file = open(file_name, "r")
    data = file.readlines()
    file.close()
    return data

def sort_out(data_list):
   """
   Organizes data: returns a two-dimensional list of numbers with the same order as in the input file.
   """
   n = len(data_list)
   list_sorted = []
   for i in range(n):
      list_sorted[i:i] = [data_list[i].split()]
      list_sorted[i] = [float(k) for k in list_sorted[i]]
   return list_sorted

def sort_out_nan(data_list):
   """
   Version of the function sort_out for data where text may occur.
   Organizes data: returns a two-dimensional list of strings with the same arrangement as in the input file (does not convert text to number).
   """
   n = len(data_list)
   list_sorted = []
   for i in range(n):
      list_sorted[i:i] = [data_list[i].split()]
   return list_sorted

def load(file_name):
    """
    Reads data from the file and organizes it in one step.
    """
    list_sorted = sort_out(load_raw(file_name))
    return list_sorted

def load_nan(file_name):
    """
    Version of the function load for data there text may occur.
    Reads data from the file and organizes it in one step.
    """
    list_sorted = sort_out_nan(load_raw(file_name))
    return list_sorted

def sort_out_segr(data_list, is_third_quant = False):
   """
   Organizes data:
    1) The numbers from the first column of the input file are placed in the list d1.
    2) If the user has declared that there is a third type of quantity in the last column, then:
       2.1) Numbers from the columns: from the second to the penultimate of the input file, it puts them in the two-dimensional list d2.
       2.2) The numbers from the last column of the input file are placed in the list d3.
    3) If the user declared that there is no third type of quantity in the last column, then:
       2.1) Numbers from the columns: from the second to the last of the input file, it places it in the two-dimensional list d2.
    4) Returns the lists d1, d2, d3.
   """
   list_sorted = sort_out(data_list)
   n = len(list_sorted)
   d1 = []
   d2 = []
   d3 = []
   for i in range(n):
      m = len(list_sorted[i])
      d1[i:i] = [list_sorted[i][0]]
      if is_third_quant:
         d2[i:i] = [list_sorted[i][1:m-1]]
         d3[i:i] = [list_sorted[i][m-1]]
      else:
         d2[i:i] = [list_sorted[i][1:m]]
   return d1, d2, d3

def sort_out_segr_nan(data_list, is_third_quant = False):
   """
   The version of the sort_out_segr function for data where text may occur.
   Organizes data:
    1) The numbers from the first column of the input file are placed in the list d1.
    2) If the user has declared that there is a third type of quantity in the last column, then:
       2.1) Numbers from the columns: from the second to the penultimate of the input file, it puts them in the two-dimensional list d2.
       2.2) The numbers from the last column of the input file are placed in the list d3.
    3) If the user declared that there is no third type of quantity in the last column, then:
       2.1) Numbers from the columns: from the second to the last of the input file, it places it in the two-dimensional list d2.
    4) Returns the lists d1, d2, d3.
   """
   list_sorted = sort_out_nan(data_list)
   n = len(list_sorted)
   d1 = []
   d2 = []
   d3 = []
   for i in range(n):
      m = len(list_sorted[i])
      d1[i:i] = [list_sorted[i][0]]
      if is_third_quant:
         d2[i:i] = [list_sorted[i][1:m-1]]
         d3[i:i] = [list_sorted[i][m-1]]
      else:
         d2[i:i] = [list_sorted[i][1:m]]
   return d1, d2, d3

def remove_comments(data_list, comment_char = '#'):
   """
   Deletes all characters from the character specified as a comment character to the end of the line.
   """
   n = len(data_list)
   list_no_comm = []
   for i in range(n):
      cut = len(data_list[i])
      if comment_char in data_list[i]:
         m = len(data_list[i])
         for k in range(m):
            if data_list[i][k] == comment_char and cut >= k:
               cut = k
      list_no_comm[i:i] = [data_list[i][0:cut]]
   list_cleaned = [k for k in list_no_comm if k != '']
   return list_cleaned

def create_name_out(file_in_name, file_out_extension = ".out"):
   """
   Returns the name of the output file. If the name of the input file has an extension, the name of the output file is the same with the extension changed to a string of file_out_extension. When the input file name has no extension (or has the same extension as the file_out_extension), the output file name is the same with the string out_file_extension added to the end.
   """
   n = len(file_in_name)
   if "." in file_in_name and file_out_extension not in file_in_name:
      for i in range(1, n+1):
         if file_in_name[-i] == ".":
            file_out_name = file_in_name[0:n-i] + file_out_extension
            return file_out_name
   else:
      file_out_name = file_in_name + file_out_extension
      return file_out_name

def join_data_of_one_line(*data_lists):
   """
   Returns a two-dimensional list whose elements of the ith row will be stored in the ith line of the output file.
   """
   lists_number = len(data_lists)
   n = len(data_lists[0])
   d = [data_lists[i] for i in range(lists_number) if len(data_lists[i]) == n]   
   m = len(d)
   line = []
   for i in range(n):
      line[i:i] = [[]]
      for k in range(m):
         if type(d[k][i]) != list:
            line[i] += [d[k][i]]
         else:
            line[i] += d[k][i]
      line[i] = [str(l) for l in line[i]]
   return line

def save(file_out_name, rows_list, separator = "\t"):
   """
   Concatenates all elements of the i-th row of rows_list into one string (separates elements from each other with a given separator) and saves it to a file. Repeats the procedure for all n rows of the list.
   """
   n = len(rows_list)
   file_out = open(file_out_name, "w")
   for i in range(n):
      line = separator.join(rows_list[i])
      file_out.write(line)
      file_out.write("\n")
   file_out.close()

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

