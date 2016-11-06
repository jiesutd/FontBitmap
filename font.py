# -*- coding: utf-8 -*-
# @Author: Jie
# @Date:   2016-11-05 21:17:27
# @Last Modified by:   Jie     @Contact: jieynlp@gmail.com
# @Last Modified time: 2016-11-06 19:18:09
# 
# The code is to extract bitwise information for bdf font file, and output bitmap from given char/strings

import matplotlib.pyplot as plt
import numpy as np


### read bdf file, return chars and the np binary array
def read_bdf(bdf_file):
	print "Reading bdf file: ", bdf_file, " ..."
	in_lines = open(bdf_file,'rU').readlines()
	## read general information
	WIDTH = 0
	HEIGHT = 0
	FONT_NAME = "Default"
	CHAR_NUM = "Default"
	BOX_POS = []
	print "SUMMARY: "
	for line in in_lines:
		line_split = line.strip(' \n').split(' ')
		start_info = line_split[0]
		if start_info == "STARTCHAR":
			break
		elif start_info == "DWIDTH":
			WIDTH = line_split[1]
			print "  WIDTH: ", WIDTH
		elif start_info == "DWIDTH1":
			HEIGHT = line_split[1]
			print "  HEIGHT: ", HEIGHT
		elif start_info == "FONT_NAME":
			FONT_NAME = line_split[1]
			print "  FONT_NAME: ", FONT_NAME
		elif start_info == "CHARS":
			CHAR_NUM = line_split[1]
			print "  CHARS NUMBER: ", CHAR_NUM
		elif start_info == "FONTBOUNDINGBOX":
			BOX_POS = line_split[1:]
			print "  BOX_POSTION: ", BOX_POS
		else:
			continue
	print "END SUMMARY."
	## read char and array
	char_array_dict = {}
	char = "NULL"
	hex_list = []
	start_flag = False
	for line in in_lines:
		line_split = line.strip(' \n').split(' ')
		start_info = line_split[0]
		if start_info == "ENDPROPERTIES":
			start_flag = True
			continue
		if start_flag:
			if start_info == "ENCODING":
				hex_list = []
				char = line_split[1]
				# print char
			elif start_info == "BBX":
				BBX = line_split[1:]
				hex_list.append(BBX)
			elif start_info == "ENDCHAR":
				char_array_dict[char] = hex2binary_array(hex_list, WIDTH,HEIGHT,BOX_POS)
				hex_list = []
			elif start_info == "BITMAP" or start_info == "STARTCHAR":
				continue
			elif char != "NULL" and len(line_split) == 1:
				hex_list.append(start_info)
			else:
				continue
	print "bdf file loaded."
	return char_array_dict


## turn hex array to binary, input format [['15', '16', '0', '-2'], '1000', '10FC', ...] first element list is BBX information, following hex value. BOX POS is list [a,b,c,d] c,d means start point
## consider the offset
def hex2binary_array(hex_array, width, height, BOX_POS):
	## node X, Y are reversed here
	width = int(width)
	height = int(height)
	size = (width, height)
	out_array = np.zeros(size)

	BBX = hex_array[0]
	Y_offset = int(BOX_POS[2])
	X_offset = int(BOX_POS[3])
	## start from left down corner
	Y_start = int(hex_array[0][2]) - Y_offset
	X_start = int(hex_array[0][3]) - X_offset

	init_list = []
	for hex_string in hex_array[1:]:
		hex_value = init_list.append(hex2binary(hex_string))
	init_array = np.asarray(init_list)
	init_X_size =  init_array.shape[0]
	init_Y_size = init_array.shape[1]
	# print "init X,Y: ",init_X_size, init_Y_size
	# print  "X start ", X_start, "Y start ", Y_start
	up_left_X = height -(X_start +init_X_size)
	down_right_X = height - X_start

	up_left_Y = Y_start
	down_right_Y = Y_start + init_Y_size
	Y_loss = 0
	if down_right_Y > width:
		Y_loss = down_right_Y- width
		down_right_Y = width
	# print "Up X,Y: ",up_left_X,up_left_Y
	# print "Down X,Y: ",down_right_X,down_right_Y
	# print "Loss: ", Y_loss
	out_array[up_left_X:down_right_X, up_left_Y:down_right_Y] = init_array[:,:init_Y_size-Y_loss]
	return out_array


#### show font, input is 2D np array
def font_show(font_array):
	plt.matshow(font_array,cmap=plt.cm.gray)
	

### convert hex_string to binary(4 bit for each hex) list 
def hex2binary(hex_string):
	out_list = []
	for hx in hex_string:
		binary_int = '{0:04b}'.format(int(hx,16))
		out_list += list(binary_int)
	return out_list


### print string's font in one picture for one char, input array_dict, and string
def print_string_font(char_array_dict,string):
	print "print bitwise map of: ", string 
	char_list = list(string.decode('utf-8'))
	for char in char_list:
		char = str(ord(char))
		font_show(char_array_dict[char])
	plt.show()


if __name__ == '__main__':
	bdf_file = "SimSun-16.bdf"
	char_array_dict = read_bdf(bdf_file)
	test_string = "羊样洋佯徉烊"
	print_string_font(char_array_dict,test_string)
