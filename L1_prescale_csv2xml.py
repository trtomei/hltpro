#!/usr/bin/env python
import csv
import sys

##########################################
##########################################
###########
###########  usage: python L1_prescale_csv2xml.py <your_csv_file> <# of ps columns in menu>
###########  example: python L1_prescale_csv2xml.py test.csv 13
###########
##########################################
##########################################

input_file = open(sys.argv[1], 'rb')
reader = csv.reader(input_file)

output_file_name = "l1_prescales.txt"
output_file = open(output_file_name,"w")

number_of_ps_columns = int(sys.argv[2])

#######
##  writing xml header
#######

header_str = "        algo/prescale-index"
type_str = "        uint"
for col in range(number_of_ps_columns):
    header_str += ",%d" % (col)
    type_str += ",uint"

output_file.write("<run-settings id=\"uGT\">\n")
output_file.write("  <context id=\"uGtProcessor\">\n")
output_file.write("    <param id=\"prescales\" type=\"table\">\n")
output_file.write("      <columns>\n")
output_file.write(header_str+"\n")
output_file.write("      </columns>\n")
output_file.write("      <types>\n")
output_file.write(type_str+"\n")
output_file.write("      </types>\n")
output_file.write("      <rows>\n")

previous_bit = -1

for row in reader:
    try: int(row[0])
    except: continue #skip rows with text in them

    if int(row[0]) != previous_bit+1: 
        print "\n ERROR: non consecutive bit # starting @ bit %d, %s\n Quitting...." % (int(row[0]),row[1])
        sys.exit()

    output_file.write("        <row>\n")
    ps_str = "          %s" % (row[0])

    for col_count,col in enumerate(row[2:]):
        if col_count >= number_of_ps_columns: break #ignores additonal comments column(s)
        ps_str += ",%d" % (int(col))

    output_file.write(ps_str+"\n")
    output_file.write("        </row>\n")                    
    previous_bit = int(row[0])
            
input_file.close()

output_file.write("      </rows>\n")
output_file.write("    </param>\n")
output_file.write("  </context>\n")
output_file.write("</run-settings>\n")
output_file.close()

print "\n converted csv file to l1 format: %s\n" % (output_file_name)
