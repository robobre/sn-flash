#!/usr/bin/python
import mysql.connector
from mysql.connector import Error
from metadata_parser import metadata_parser
import datetime

class MYSQL_SIM_DATA:
    def __init__(self,debug=0):
        print ("Constructing....")
        self.connection=None
        self.DEBUG=debug
        self.ConnectDatabase("localhost","simulation","simuser","pictreba1")
    def __del__(self):
        if self.connection is not None:
            self.connection.close()
        print ("destructing.....")
    def is_connected(self):
        return self.connection.is_connected()
    def ConnectDatabase(self,h, db, u ,pww):
        #type: (MYSQL_SIM_DATA,str,str,str,str)
        try:
            self.connection = mysql.connector.connect(host=h, database=db,user=u,password=pww)
            if self.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                if self.DEBUG>0:
                    cursor = self.connection.cursor()
                    cursor.execute("select database();")
#        cursor.execute("show tables;")
                    record = cursor.fetchone()
                    print("You're connected to database: ", record)
                    cursor.execute("show tables;")
                    record=cursor.fetchall()
                    for i in range(len(record)):
                        print("In database are these tables: ", record[i])
                        print("show columns from "+''.join(record[i]))
                        cursor.execute("show columns from "+''.join(record[i]))
                        record2=cursor.fetchall()
                        for j in range(len(record2)):
                            print(record2[j])
                    cursor.close()
        except Error as e:
            print("Error while connecting to MySQL", e)
            sys.exit(1)
#        finally:
#            if (self.connection.is_connected()):
#                cursor.close()
#                self.connection.close()
#                print("MySQL connection is closed")
    def init_prod(self,username,event_generator,vertex_generator,expsetURN,mag_field, source_mat):
         #type: (MYSQL_SIM_DATA,str,str,str,str,str,str)
         print username
         cursor=self.connection.cursor()
#         cursor.execute("select database()")
         now=datetime.datetime.utcnow()
         cursor.execute("INSERT INTO sim_production (prod_date,username,event_generator, vertex_generator, experimentalSetupUrn, magnetic_field,source_material) VALUES(%s,%s,%s,%s,%s,%s,%s)",(now, username,event_generator,vertex_generator,expsetURN,mag_field, source_mat) )
         
         cursor.execute('SELECT last_insert_id()')
         record = cursor.fetchone()
#         print("You're connected to database: ", record)
         self.connection.commit()
         cursor.close()
         return record[0]
     
    def store_simu (self, prodID, Site, Path_of_files, Nb_ev, Nb_of_files,md5sum, Falaise_version,comment):
         #type: (MYSQL_SIM_DATA,str,str,int,int,str,str,str)
         cursor=self.connection.cursor()
         cursor.execute("INSERT INTO sim_simulation ( Prod_ID, Site, Path_of_Files, Nb_of_events, Nb_of_files, Falaise_version, md5sum, long_comment) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",( ProdID, Site, Path_of_files, Nb_ev, Nb_of_files, Falaise_version, md5sum, comment))
         cursor.execute('SELECT last_insert_id()')
         record = cursor.fetchone()
         cursor.execute("UPDATE sim_production SET simulation=%s where ID=%s"%(1,prodID))
#         cursor.execute
         self.connection.commit()
         cursor.close()
         return record[0]
    def store_reco (self, prodID, simID, path_of_files, Nb_of_events, Nb_of_files, Sw_version,data_type, reconstruct_conf, md5sum, long_comment)
         #type:(MYSQL_SIM_DATA,int,int,str,int,int,str,str,str,str)
         cursor=self.connection.cursor()
         cursor.execute("INSERT INTO sim_simulation (ProdID, SimID,Path_of_Files,Nb_of_events,Nb_of_files, Sw_version,data_type, reconstruct_conf, md5sum,long_comment) VALUES(%s,%s,%s,%s,%s,%s,%s,%s, %s,%s) ",(prodID,simID,path_of_files, Nb_of_events, Nb_of_files, Sw_version,data_type, reconstruct_conf, md5sum, long_comment))
                 
myconnect=MYSQL_SIM_DATA(0)
rec=myconnect.init_prod("breier","nieco","nieco","nieco2","nieco3","nieco4")
rec1=myconnect.store_simu(rec,"cc","/adresa/suboru/",10000,10,"hash","5.6.7","comentujem si")
myconnect.store_reco(rec, rec1 ,"/adresa/recosuboru/",10000,10,10.6.1,1,,hash,comentujem )
#:print("You're connected to database: ", rec)
conf_path="../simdata/"
filename="output_files.d/file_0.meta"
mp=metadata_parser(0)
mp.parse_file(conf_path,filename)
print mp.data
