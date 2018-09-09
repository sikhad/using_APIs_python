# Program to get geocodes based on Google API

import json
import urllib.request
import csv
import re

class geocoder():
    def __init__(self):
        self.key =  #### private key removed, but goes here ####
        self.fileInput()
        self.fileOutput()

    def fileInput(self):
        addressStr = ""
        self.addressList = []
        self.finalList = []
        self.originalRow = []
        j = 0
        self.k = 0 

        filePath = 'locations.csv'

        file = open(filePath)
        
        self.addressReader = csv.reader(file, delimiter = ',')
        
        for row in self.addressReader:
            print(row[1])
            self.originalRow.append(row[:]) # creates copy of the row (not alias) and stores in new list
            try:
                self.jsonParse(row[2], self.key) # function connects to Google API

                self.originalRow[j].append(self.lat) # adds the latitude to original list of non-formatted addresses 
                self.originalRow[j].append(self.long) # adds the longitude to original list of non-formatted addresses 

                self.finalList.append(self.originalRow[j]) # adds the updated row to the final list
                j+=1 
                print(j) # keeps track of the number of addresses processed
                
            except: # if coordinates are not found, simply adds the original row to the final list
                self.finalList.append(self.originalRow[j]) 
                j+=1
                self.k+=1 # counts the number of coordinates not found
                print(j, " [ coordinates not found ] ") # keeps track of the number of addresses processed

        file.close()

    def jsonParse(self, address, key):
        count = 0
        request = ('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}').format(address, key) # accesses Google API 
        j = urllib.request.urlopen(request) # opens the json file via url
        
        str_response = j.readall().decode('utf-8')
        obj = json.loads(str_response) # loads and stores json file
        
        ourResult = obj['results'][0]['geometry']['location'] # extracts needed section
        self.lat = ourResult['lat'] # extracts latitude value from the section
        self.long = ourResult['lng'] # extracts longitude value from the section 

    def fileOutput(self):
        filePath = 'locations.csv'
        
        file = open(filePath, 'w')
        
        self.addressWriter = csv.writer(file, delimiter = ',')
        for row in self.finalList: # iterates through the final list and writes each row to a new text file
            self.addressWriter.writerow(row)
            
        file.close()
        print("")
        print("Done!")
        print(self.k, " coordinates could not be found.")

# run       
Geo = geocoder()