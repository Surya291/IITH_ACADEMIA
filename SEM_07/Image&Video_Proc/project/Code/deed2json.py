
### imports here !!
import os
import re
import json

'''
Created on Dec-2, 2021

What does it do : 
>> Given a ocr'd version of the sale deed, we need to extract key entities like

1. Doc no
2. Header --> article name(Sale, etc)
3. execution date --> exec_date
4. Party info --> info of sellers and purchasers

---> Buyers : 
        -----> Name
        -----> age
        -----> care of 
---> Purchasers :
        -----> Name
        -----> age
        -----> care of 
5. Description of property 
        -----> Khatha no
        -----> Site No
        -----> Sy. No
        -----> Situated at
        -----> Measurements
                -----> North to South in feet
                -----> East to West in feet
                -----> Total in sq.feet
        -----> Bounded by
                        -----> North , East, West South

'''

class PID_obj(object):
    '''
    A Data struct consists of details of a single person : PID--> Person ID
    '''
    def __init__(self):
        self.nm = None
        self.ag =None
        self.co = None
        
    def __str__(self):
        string = str('----------------\n')
        string += str('name : {}\n'.format(self.nm))
        string += str('age : {}\n'.format(self.ag))
        string += str('care of : {}\n'.format(self.co))
        string += str('----------------')
        return string

    def export_json(self):
        data = {    "name":self.nm,
                    "age":self.ag,
                    "careof":self.co
        }

        return data

class parties_info_struct(object):
    '''
    Algo to extract info of all the mentioned properties
    --> From first page skim through all the names of the persons mentioned (done using finding the salutation Mr, Mrsm, Sri, Smt)
    ---> When you find one extract age, and care of 
    --> When you find the phrases of sellers and buyers you can stop finding for names 
    '''
    def __init__(self):
        
        self.roles_dict = {}
        self.roles = set()
        self.pid_list = []
        self.curr_pid = None
        
    def __repr__(self):
        
        string = '===============================\n'
        for role in list(self.roles):
            string += role
            string += str('\n---------\n')
            for pid_obj in self.roles_dict[role]:
                string +=str(pid_obj)
            string += str('\n---------\n')
        string += "==============================="
        return string

    def export_json(self):
        data = {}

        for role in list(self.roles):
            role_pid_dict = {}
            for i,pid_obj in enumerate(self.roles_dict[role]):
                role_pid_dict[i] = pid_obj.export_json()


            data[role] = role_pid_dict

        return data
    
    
    def find_PID_entities(self, page_txt):
        '''
        employ regex.. to find out necessary entities
        '''
        rx_name = r"((?:smt|sri|mr|mrs|miss)\b[^,]\b[^\n]*)"
        rx_co = r"((?:son|daughter|wife|s/o|w/o|d/o|s/|w/)\b[^,]\b[^\n]*)"
        rx_age = r"((?:aged|age:)\b[^,]\b[^\n]*)"
        rx_role = r"(vendor|purchaser)"
        rx = "|".join([rx_name,rx_co,rx_age,rx_role])
        self.pg_entity_list = re.findall(rx,page_txt,re.IGNORECASE)
        
    @staticmethod
    def find_entity_pos(ent_tuple):
        '''
        ent_tuple--> entity tuple
        Job: given a tuple return the entitity and the pos of it for knowing which ent it is
        '''
        
        for pos,ent in enumerate(ent_tuple):
            if(ent != ''):
                return ent, pos
        
    def create(self,page_txt):
        
        self.find_PID_entities(page_txt)

        for ent_tuple in self.pg_entity_list:
            ent,ent_pos = parties_info_struct.find_entity_pos(ent_tuple)

            if(ent_pos ==0): ## name
                if(self.curr_pid != None):
                    self.pid_list.append(self.curr_pid)
                self.curr_pid = PID_obj()
                self.curr_pid.nm = ent

            elif(ent_pos == 1):  ## careof
                self.curr_pid.co = ent

            elif(ent_pos == 2): ## age
                self.curr_pid.ag = ent

            elif(ent_pos == 3):
                self.pid_list.append(self.curr_pid)
                self.roles.add(ent)
                self.roles_dict[ent] = self.pid_list

                self.curr_pid = None
                self.pid_list = []

                if(len(self.roles) == 2):
                    return True
        return self.export_json()

class property_descript_struct:
    '''
    a data struct with property descriptions

    Algo : first need to find where the schedule is present by finding the phrase "All that piece and parcel"
    Find desired entities thereafter
    '''
    def __init__(self):
        self.siteno= None
        self.khatano = None
        self.surveyno = None
        self.location = None
        
        ## boundaries
        self.east ,self.west, self.north, self.south = None, None, None, None

        ## measurements
        self.E2W = None
        self.N2S = None
        self.area = None

    
    def create(self,doc_txt):
        
        ## find the text 
        ## finding by the phrase "All the piece and parcel by"
        
        rx_schedule_str = r"all that piece and parcel of"
        res = re.search(rx_schedule_str,doc_txt, re.IGNORECASE)
        page_str = res.start()
        doc_txt = doc_txt[page_str:]
        
        self.extract_siteno(doc_txt)
        self.extract_khatano(doc_txt)
        self.extract_survey(doc_txt)
        self.extract_boundaries(doc_txt)
        self.extract_measurements(doc_txt)

        return self.export_json()
        
    def __repr__(self):
        string = '---------------\n'
        string += str('Site No.{}\n'.format(self.siteno) )
        string += str('{}\n'.format(self.khatano) )
        string += str('{}\n'.format(self.surveyno) )
        string += '=================\n'
        string += 'boundaries\n'
        string += '=================\n'
        string += self.east + '\n'
        string += self.west + '\n'
        string += self.north + '\n'
        string += self.south + '\n'
        string += '=================\n'
        string += 'measurements\n'
        string += '=================\n'
        string += str('East to West : {}\n'.format(self.E2W)) 
        string += str('North to South : {}\n'.format(self.N2S)) 
        string += str('Area : {}\n'.format(self.area))
        
        return string


    def export_json(self):
        data = {
            'site_no': self.siteno, 
            'khata_no':self.khatano, 
            'survey_no': self.surveyno, 
            'location': self.location, 
            'measure': { 
                        'N2S': self.N2S, 
                        'E2W': self.E2W, 
                        'area':self.area
                        }, 
            'boundaries' : {
                            'N':self.north, 
                            'E': self.east ,
                            'W' : self.west ,
                            'S' : self.south 
                            }

        }


        return data
        
    def extract_siteno(self,doc_txt):
        rx_siteno = r"((?:Site No.|Site bearing No.|property bearing No.)(\d+)\b[^,^\n ^\s]*)"
        res = re.search(rx_siteno,doc_txt,re.IGNORECASE)
        
        if(res):
            self.siteno = res.group(2) ## extracting the no.
            
    def extract_khatano(self,doc_txt):
        rx_khata = r"((?:Katha No.)\b[^,^\n ^\s]*)"
        ### TODO : extract just the no. phrase
        res = re.search(rx_khata,doc_txt,re.IGNORECASE)
        
        if(res):
            self.khatano = res.group(0) ##
    def extract_survey(self,doc_txt):
        rx_survey = r"((?:Sy.)\b[^,^\n ^\s]*)"
        res = re.search(rx_survey, doc_txt,re.IGNORECASE)
        if(res):
            self.surveyno = res.group(0) ##
    def extract_boundaries(self,doc_txt):
        rx_east = r'(?:east by)\b[^\n]*'
        rx_west = r'(?:west by)\b[^\n]*'
        rx_north = r'(?:north by)\b[^\n]*'
        rx_south = r'(?:south by)\b[^\n]*'
        
        self.east = re.search(rx_east,doc_txt,re.IGNORECASE).group(0)
        self.west = re.search(rx_west,doc_txt,re.IGNORECASE).group(0)
        self.north = re.search(rx_north,doc_txt,re.IGNORECASE).group(0)
        self.south = re.search(rx_south,doc_txt,re.IGNORECASE).group(0)
    
    def extract_measurements(self,doc_txt):
        rx_E2W = r"east to west\s?[^\w]*\s?(\d+) feet"
        rx_N2S = r"north to south\s?[^\w]*\s?(\d+) feet"
        rx_area = r"(\d+) square feet"
        
        txt_wout_enter = doc_txt.replace('\n',' ')
        self.E2W = float(re.search(rx_E2W, txt_wout_enter, re.IGNORECASE).group(1))
        self.N2S = float(re.search(rx_N2S, txt_wout_enter, re.IGNORECASE).group(1))
        self.area = float(re.search(rx_area, txt_wout_enter, re.IGNORECASE).group(1))

class DATE(object):
    '''
    Date data struct 
    '''
    def __init__(self,d=None,m=None,y = None):
        self.d = d
        self.m = m
        self.y = y

    def export_json(self):
        data = {
            "d" : self.d, 
            "m" : self.m, 
            "y" : self.y 
        }

        return data

    def __repr__(self):
        return str(self.d) + '-' + str(self.m) + '-' + str(self.y)

class doc_struct(object):
    '''
    Bringing all things together...
    '''
    def __init__(self):
        '''
        Each defines a col. in EC
        '''

        
        self.doc_no = None
        self.article_nm = None
        self.exec_date = DATE()
        self.parties_info = parties_info_struct()
        self.prop_descript = None
        self.page_str = 0
        self.schedule_info = property_descript_struct()
        
    def turn_next_page(self):
        '''
        retruns chuck of text corresponding to a page 
        '''
        rx_end_pg = r"===================================================================================================================================================================="
        res = re.search(rx_end_pg,self.doc_txt)
        self.page_end = res.end()
        self.page = self.doc_txt[self.page_str:self.page_end]
        self.doc_txt = self.doc_txt[self.page_end:]

    def create(self, doc_path):

        self.dir_name = os.path.dirname(doc_path)

        self.doc_name = doc_path
        self.doc_file = open(doc_path,'r+')
        self.doc_txt = self.doc_file.read()
        
        self.extract_doc_no()
        
        ## insert the page here .. the first page..
        self.turn_next_page() ## returns first page
        self.extract_article_name()
        self.extract_exec_date()
        self.extract_parties_info()
        self.extract_schedule_info()
        json_obj = self.export_as_json()
        
        return json_obj 
            
        
    def extract_doc_no(self):
        self.doc_no = os.path.basename(self.doc_name)[:-4] ## removes the .txt extension
        
    def extract_article_name(self):
        
        ### TODO : All possible regex here !!
        rx_anm_sale = r'\babsolute sale deed\b|\bdeed of absolute sale\b'

        if(re.search(rx_anm_sale, self.page, re.IGNORECASE)):
            self.article_nm= 'sale'
            
    def extract_exec_date(self):
        
        ## TODO : Add possible date specifying versions
        ## As of now : added dd.mm.yyyy or dd/mm/yyyy
        rx_date = r'\((\d+)\.(\d+)\.(\d+)\)|\((\d+)-(\d+)-(\d+)\)'

        date = re.search(rx_date,self.page,re.IGNORECASE)
        
        idx = 1 if date.group(1)!=None else 4 #if  + format occurs in 1,2,3 else 4,5,6
        self.exec_date.d,self.exec_date.m,self.exec_date.y  = int(date.group(idx)) , int(date.group(idx+1)) , int(date.group(idx+2))
        
    def extract_parties_info(self):
        done = False
        while(not done):
            done = self.parties_info.create(self.page)
            self.turn_next_page() ## move to next page ...

    def extract_schedule_info(self):
        self.schedule_info.create(self.doc_txt)

    def export_as_json(self):
        data = {
            'doc_no' : self.doc_no, 
            'article_type' : self.article_nm , 
            'exec_date' : self.exec_date.export_json() ,
            'parties_info' : self.parties_info.export_json(), 
            'schedule_info' : self.schedule_info.export_json()

        }


        json_name = self.doc_no + str('.json')
        path = os.path.join(self.dir_name,json_name)
        with open(path, 'w', encoding ='utf8') as json_file:
            json.dump(data, json_file, allow_nan=True,ensure_ascii=False)
            print("JSON created")


        return data


if __name__ == "__main__":
    ### Testing 
    test= doc_struct()
    json_obj = test.create('/home/surya/Desktop/Lending_Kat/MVP_folder/deeds_ocr/MDSD_2018.txt')



    print(test.doc_no)
    print(test.article_nm)
    print(test.exec_date)
    print(test.parties_info)
    print(test.schedule_info)