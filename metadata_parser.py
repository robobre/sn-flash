#!/usr/bin/python
import re
#from __future__ import print_function
class metadata_parser:
    def __init__(self,debug=0):
        self.data={}
        self.DEBUG=debug
    def parse_file(self,conf_path,filename):
 #       print("Hello World") 
        if self.DEBUG>0 :
            print (conf_path,filename)
        conf_path="../simdata/"
#        filename="config.d/conf.d/launch_file_0.conf"
        filename="output_files.d/file_0.meta"
#        filename="config.d/variant.d/variant.profile"
        cf=open(conf_path+filename)
        line=cf.readline()
        while line:
           # print (line)
            m = re.match("\[name=\"(\w+.\w+)\" type=\"(\w+::\w+)\"\]", line)
            if m:
                section= m.group(1)
                self.data[section]={}
#               print m.group(0)
                if self.DEBUG>0:
                    print m.group(1)
#               print m.group(2)
            m= re.match("(\S+) \: string = \"(\S.+)\"",line)
            if m:
                self.data [section][m.group(1)]= m.group(2) 
                if self.DEBUG>0:
                    print (m.group(1)+'=',m.group(2))
            else :
                m=re.match("(\S+) \: integer = (\d+)",line)
                if m:
                    self.data[section][m.group(1)]=int(m.group(2))
                else:
                    m=re.match("(\S+) \: boolean = (\d)",line)
                    if m:
                        self.data[section][m.group(1)]=bool(int(m.group(2)))

            line=cf.readline()
        if self.DEBUG>0: 
            print (self.data)
        cf.close()

