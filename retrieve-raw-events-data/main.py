import csv
import json
import re
from copy import deepcopy

class DataToJson():
    def __init__(self, _json_file="smart-contracts-data.json", _csv_file="organizers-data.csv", _json_output="result"): #les fichiers sont prédéfinis
        self.format_allowed = [".png", ".mp4", ".jpeg"]
        self.json_file = _json_file
        self.csv_file = _csv_file
        self.json_output = _json_output

        self.json_file = self.add_extension(self.json_file, ".json")
        self.csv_file = self.add_extension(self.csv_file, ".csv")
        self.json_output = self.add_extension(self.json_output, ".json")

        #json template
        self.template_json = [{
            "id": "",
            "name": "",
            "title": "",
            "startDateTime": "",
            "endDateTime": "",
            "address": "",
            "locationName": "",
            "totalTicketsCount": "",
            "assetUrl": "",
            "lineup": [],
            "ticketCollection": [
                {
                    "collectionName": "",
                    "scAddress": "",
                    "collectionAddress": "",
                    "pricePerToken": "",
                    "maxMintPerUser": "",
                    "saleSize": "",
                }
            ]
        }
    ]

    def add_extension(self, file, end): #ajout des .json ou .csv si omis
        if (not file.endswith(end)):
            file = file + end 
        return(file)

    def get_csv_informations(self):
        file = self.csv_file
        self.dict_csv_infos= []

        with open(file, 'r') as file: #r = read
            reader = csv.DictReader(file, skipinitialspace=True)  
            for infos in reader:
                self.dict_csv_infos.append(infos) #lets add our informations into a list

        for i in range(len(self.dict_csv_infos)):
            replace_artists = self.dict_csv_infos[i]["line up"].split("-") #transformation of artists string into a list
            self.dict_csv_infos[i]["lineup"] = replace_artists

            if not any(self.dict_csv_infos[i]["asset url"].endswith(word) for word in self.format_allowed): #gestion d'erreur si l'url ne finit pas par mp4 etc
                    self.dict_csv_infos[i]["asset url"] = ""
        
        #sort self.dict_csv_infos by id
        self.dict_csv_infos = sorted(self.dict_csv_infos, key=lambda k: k['id'])
        
    def get_json_informations(self):
        with open(self.json_file) as json_file:
            data = json.load(json_file)
            self.json_informations = data

            for i in range(len(self.json_informations)): #loop on all events
                try: 
                    self.json_informations[i]['smart_contract']['collectionName'] = self.json_informations[i]['smart_contract'].pop('collection') #on remplace collection par collectionName
                except Exception:
                    pass
                try:
                    self.json_informations[i]['smart_contract']['scAddress'] = self.json_informations[i]['smart_contract'].pop('crowdsale')
                except Exception:
                    pass

    def remove_whitespace(self):
        copy_a = self.dict_trie_csv_infos[0].copy()
        for i in range(len(self.dict_trie_csv_infos)):
            copy_a = self.dict_trie_csv_infos[i].copy()

            for key in copy_a.items():
                if ' ' in key:
                    # match string with regex
                    new_str = re.sub(r'\s\b[a-z]', lambda m: m.group().upper(), key)
                    # replace 1st char of word to upper case except 1st word
                    new_key = new_str.replace(" ", "")
                    self.dict_trie_csv_infos[i][new_key] = self.dict_csv_infos[i][key]
                    # delete key from input_data
                    del self.dict_trie_csv_infos[i][key]
    
    def merge_jsons(self):
        self.dict_trie_csv_infos = []
        self.sales_params = []
        compteur = -1
        
        for y in self.json_informations:
            compteur += 1
            self.sales_params.append([])
            for i in self.dict_csv_infos:
                #check if  same 'event_id' before
                if float(y['event_id']) == float(i['id']):   
                    self.sales_params[compteur].append(y['smart_contract']['sale_params'])
                    #merge the two dictionaries
                    
                    y.update(i)
                    self.dict_trie_csv_infos.append(y)

    def fill_templates_value(self):
            #add values to json
        
        compteur = 0
        for i in range(len(self.dict_trie_csv_infos)):

            if (self.dict_trie_csv_infos[i]['id']) != self.dict_trie_csv_infos[i - 1]['id']:
                self.template_json.append(deepcopy(self.template_json[0]))

                self.template_json[i]['id'] = self.dict_trie_csv_infos[i]['id']
                print(self.template_json[i]['id'])
                self.template_json[i]['name'] = self.dict_trie_csv_infos[i]['name']
                self.template_json[i]['title'] = self.dict_trie_csv_infos[i]['event title']
                self.template_json[i]['startDateTime'] = self.dict_trie_csv_infos[i]['smart_contract']['sale_params']['start_time']
                self.template_json[i]['endDateTime'] = self.dict_trie_csv_infos[i]['smart_contract']['sale_params']['end_time']
                self.template_json[i]['adress'] = (self.dict_trie_csv_infos[i]['smart_contract']['scAddress'])
                self.template_json[i]['locationName'] = self.dict_trie_csv_infos[i]['address of the location']
                self.template_json[i]['totalTicketsCount'] = self.dict_trie_csv_infos[i]['total ticket number']
                self.template_json[i]['assetUrl'] = self.dict_trie_csv_infos[i]['asset url']
                self.template_json[i]['lineup'] = self.dict_trie_csv_infos[i]['lineup']

                #fill the smartcontract now
                self.template_json[i]['ticketCollection'][0]['collectionName'] = self.dict_trie_csv_infos[i]['smart_contract']['collectionName']
                self.template_json[i]['ticketCollection'][0]['endTime'] = self.dict_trie_csv_infos[i]['smart_contract']['sale_params']['end_time']                
                self.template_json[i]['ticketCollection'][0]['pricePerToken'] = self.dict_trie_csv_infos[i]['smart_contract']['sale_params']['price_per_token']
                self.template_json[i]['ticketCollection'][0]['totalTicketsCount'] = ''             
                self.template_json[i]['ticketCollection'][0]['soldTicketsCount'] = ''
            
            else: #check if same event (same id)
                compteur +=1
                self.template_json[i-compteur]['ticketCollection'].append(
                {
                    "collectionName": "",
                    "scAddress": "",
                    "collectionAddress": "",
                    "pricePerToken": "",
                    "maxMintPerUser": "",
                    "saleSize": "",
            })

                self.template_json[i - compteur]['ticketCollection'][-1]['collectionName'] = self.dict_trie_csv_infos[i]['smart_contract']['collectionName']
                self.template_json[i - compteur]['ticketCollection'][-1]['endTime'] = self.dict_trie_csv_infos[0]['smart_contract']['sale_params']['end_time']
                self.template_json[i - compteur]['ticketCollection'][-1]['pricePerToken'] = self.dict_trie_csv_infos[i]['smart_contract']['sale_params']['price_per_token']
                self.template_json[i - compteur]['ticketCollection'][-1]['totalTicketsCount'] = ''             
                self.template_json[i - compteur]['ticketCollection'][-1]['soldTicketsCount'] = ''

        self.template_json =self.template_json[:-1] #had to delete the last
        
    def write_informations_into_json(self):
        with open(self.json_output, 'w') as outfile:
            json.dump(self.template_json, outfile, indent=4)
            print("JSON file created")
        outfile.close()
        
    def transform_json_and_csv_to_json(self):
        self.get_csv_informations()
        self.get_json_informations()
        self.merge_jsons()
        self.remove_whitespace()
        self.fill_templates_value()
        self.write_informations_into_json()

def main():
    data_to_json = DataToJson(_json_output="test.json")
    data_to_json.transform_json_and_csv_to_json()

# main()

