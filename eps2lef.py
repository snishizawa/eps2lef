#!/bin/python3
# program which translate eps into lef
# usage
# python3 eps2lef.py -i input.eps -o output.lef

import argparse, re, os 
import myObjects as mobj

def main():
	parser = argparse.ArgumentParser(description='argument')
	parser.add_argument('-i','--input', type=str, help='input eps')
	parser.add_argument('-n','--name', type=str, help='input cell name')
	parser.add_argument('-l','--lefout', type=str, help='output lef')
#	parser.add_argument('-g','--gdsout', type=str, help='output gds')
	args = parser.parse_args()
	print(args.input)
	print(args.lefout)
#	print(args.gdsout)
	
	print("::start read\n")

	vdd_yidx = 175
	vss_yidx = 1175

	# file open
	with open(args.input, 'r') as inf:
		lines = inf.readlines()
		polylist = []
		vddlist = []
		vsslist = []
		boxlist = []
		
		linecnt = None # line number counter
		mode = None 
		tmp_poly = None
		tmp_box  = None
		tmp_text = None
		box_area_max = 0 # get max box as boundary
		# coordinate of label
		tmp_x1 = 0
		tmp_y1 = 0
		for line in lines:
			line = line.strip('\n')
			line = line.lstrip() # remove spaces beggining on line
			
			# set mode
			if(mode == None):
				linecnt = 0 # reset counter
				if(line.startswith('% TEXT')):
					mode = 'text';
					tmp_text = mobj.MyObject()
				elif(line.startswith('% POLY')):
					mode = 'poly';
					tmp_poly = mobj.MyObject()
				elif(line.startswith('% BOX')):
					mode = 'box';
					tmp_box = mobj.MyObject()
				print(":: mode:"+str(mode)+"\n")
#			print(line)
			print(mode)
#			print(linecnt)
			# detect coordinate
			if(mode == 'poly'):
				linecnt += 1	
				#print(":: poly:line"+str(linecnt)+"\n")
				print(line)
				if(linecnt == 5):
					sparray = line.split()
					tmp_x1 = sparray[0]
					tmp_y1 = sparray[1]

				elif(linecnt == 6):
					sparray = line.split()

					# this is vdd poly
					print(str(tmp_y1)+" "+str(vdd_yidx)+" "+str(sparray[1])+" "+str(vdd_yidx)+"\n")
					if((int(tmp_y1) == int(vdd_yidx)) or (int(sparray[1]) == int(vdd_yidx))):
						# port, layer, x1, x2, y1, y2
						tmp_poly.add_poly('VDD', 'M1', tmp_x1, sparray[0], tmp_y1, sparray[1])
						vddlist.append(tmp_poly)
						print("Add VDD\n")
					# this is vss poly
					elif((int(tmp_y1) == int(vss_yidx)) or (int(sparray[1]) == int(vss_yidx))):
						# port, layer, x1, x2, y1, y2
						tmp_poly.add_poly('VSS', 'M1', tmp_x1, sparray[0], tmp_y1, sparray[1])
						vsslist.append(tmp_poly)
						print("Add VSS\n")
					# this is signal poly
					else:	
						# port, layer, x1, x2, y1, y2
						tmp_poly.add_poly('noName', 'M1', tmp_x1, sparray[0], tmp_y1, sparray[1])
						polylist.append(tmp_poly)
						print("Add SIG\n")
					
					# finish mode
					#print(str(tmp_poly.x1)+" "+str(tmp_poly.x2)+" "+str(tmp_poly.y1)+" "+str(tmp_poly.y2)+"\n")
					linecnt = 0
					mode = None
					continue # back to for
					
			elif(mode == 'box'):
				linecnt += 1	
				if(linecnt == 6):
					sparray = line.split()
					# This is BOX and coordinate is 0,0 
					if((int(sparray[1]) == 0) and (int(sparray[2]) == 0)):
						# port, layer, x1, x2, y1, y2
						tmp_box.add_box('noName', 'BND', sparray[1], sparray[7], sparray[2], sparray[8])
						#tmp_box.box2rect()
						# finish mode
						boxlist.append(tmp_box)
					linecnt = 0
					mode = None
					#continue # back to for
					
			elif(mode == 'text'):
				linecnt += 1	
				# store x and y
				if(linecnt == 6):
					sparray = line.split()
					tmp_x = sparray[0]
					tmp_y = sparray[1]
				# store label
				elif(linecnt == 10):
					sparray = line.split()
					label = sparray[0]
					label = label.replace('(','')
					label = label.replace(')','')
					
					# If this is not a port (matched with []),
					# reset to mode=None
					print("::"+str(label)+"\n")
					if (re.match(r'\[.*]', label) ):
						linecnt = 0
						mode = None
						continue # back to for
						
					# Search poly which should be labeled
					for poly in polylist:
						# accepatable error of coordinate
						ambiguity = 3 
						print(str(tmp_x)+" "+str(tmp_y)+"")
						print(str(poly.x1)+" "+str(poly.x2)+" "+str(poly.y1)+" "+str(poly.y2)+"\n")
						if(((int(poly.x1) - ambiguity) <= int(tmp_x)) and \
								(int(tmp_x)  <= ( int(poly.x2) + ambiguity)) and \
							 ((int(poly.y1) - ambiguity) <= int(tmp_y)) and \
								(int(tmp_y)  <= ( int(poly.y2) + ambiguity))):
							poly.set_port(label)
							# finish mode
							linecnt = 0
							mode = None
							continue # back to for
  
					# if search finish w/o match, report it
					if(mode == None):
						continue # back to for
					else:
						print(":: ERROR!! not matched label "+str(label)+" at "+str(tmp_x)+","+str(tmp_y)+"\n")
						exit()

	# output
	with open(args.lefout, 'w') as lef:
		outlines = []
		

		outlines.append("MACRO "+str(args.name)+" ;\n") 
		outlines.append("CLASS CORE ;\n") 
		outlines.append("FOREIGN "+str(args.name)+" 0.0 0.0 ;\n") 
		for box in boxlist:
			box.box2rect(1.0)
			outlines.append("ORIGIN "+str(box.x1)+" "+str(box.y1)+";\n") 
			outlines.append("SIZE "+str(box.x2)+" BY "+str(box.y2)+";\n") 
		outlines.append("SYMMETRY X Y ;\n") 
		outlines.append("SITE UNIT ;\n\n") 

		for poly in polylist:
			# if this metal is not labeled
			if(poly.port != 'noName'):
				poly.poly2path(1.0)
				outlines.append("PIN "+str(poly.port)+" ;\n") 
				outlines.append("DIRECTION "+str(poly.portdir)+" ;\n") 
				outlines.append("PORT\n")
				outlines.append("LAYER "+str(poly.layer)+" ;\n") 
				outlines.append("RECT "+str(poly.x1)+" "+str(poly.y1)+" "+str(poly.x2)+" "+str(poly.y2)+"\n") 
				outlines.append("END\n")
				outlines.append("END "+str(poly.port)+" ;\n\n") 

		# VDD VSS DEF
		print("::gen!\n")
		print(vddlist)
		outlines.append("PIN VDD ;\n") 
		outlines.append("USE GROUND ;\n") 
		outlines.append("PORT\n")
		outlines.append("LAYER M1 ;\n") 
		for poly in vddlist:
			poly.poly2path(1.0)
			outlines.append("RECT "+str(poly.x1)+" "+str(poly.y1)+" "+str(poly.x2)+" "+str(poly.y2)+" ;\n") 
		outlines.append("END\n")
		outlines.append("END VDD\n\n") 

		outlines.append("PIN VSS ;\n") 
		outlines.append("USE GROUND ;\n") 
		outlines.append("PORT\n")
		outlines.append("LAYER M1 ;\n") 
		for poly in vsslist:
			poly.poly2path(6.0)
			outlines.append("RECT "+str(poly.x1)+" "+str(poly.y1)+" "+str(poly.x2)+" "+str(poly.y2)+" ;\n") 
		outlines.append("END\n")
		outlines.append("END VSS\n\n") 

		# OBS for M1
		outlines.append("OBS \n") 
		outlines.append("LAYER M1 ;\n") 
		for poly in polylist:
			# if this metal is not labeled
			if(poly.port == 'noName'):
				poly.poly2path(6.0)
				outlines.append("RECT "+str(poly.x1)+" "+str(poly.y1)+" "+str(poly.x2)+" "+str(poly.y2)+"\n") 
		outlines.append("END\n\n")

		outlines.append("END  "+str(args.name)+"\n") 

		lef.writelines(outlines)
	lef.close()	
		
	

if __name__ == '__main__':
	main()
