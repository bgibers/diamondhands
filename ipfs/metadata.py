#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import time
import os
from progressbar import progressbar
import json
from copy import deepcopy

import warnings

from ipfs import upload_to_ipfs
warnings.simplefilter(action='ignore', category=FutureWarning)


# Base metadata. MUST BE EDITED.
BASE_IMAGE_URL = "ipfs://QmQyw1hGdSvcQVX8pAGirJ4UgzYAxddt1VQ6RzHQjTod9p"
BASE_NAME = "Diamond Hands"

BASE_JSON = {
    "name": BASE_NAME,
    "description": "Algorithmically generated. Forever on chain. Diamond hands.",
    "image": BASE_IMAGE_URL,
    "attributes": [],
}


# Get metadata and JSON files path based on edition
def generate_paths(edition_name):
    edition_path = os.path.join('output', 'edition ' + str(edition_name))
    metadata_path = os.path.join(edition_path, 'metadata.csv')
    json_path = os.path.join(edition_path, 'json')

    return edition_path, metadata_path, json_path

# Function to convert snake case to sentence case
def clean_attributes(attr_name):
    
    clean_name = attr_name.replace('_', ' ')
    clean_name = list(clean_name)
    
    for idx, ltr in enumerate(clean_name):
        if (idx == 0) or (idx > 0 and clean_name[idx - 1] == ' '):
            clean_name[idx] = clean_name[idx].upper()
    
    clean_name = ''.join(clean_name)
    return clean_name


# Function to get attribure metadata
def get_attribute_metadata(metadata_path):

    # Read attribute data from metadata file 
    df = pd.read_csv(metadata_path)
    df = df.drop('Unnamed: 0', axis = 1)
    df.columns = [clean_attributes(col) for col in df.columns]

    # Get zfill count based on number of images generated
    zfill_count = len(str(df.shape[0]))

    return df, zfill_count

# Main function that generates the JSON metadata
def run():

    # Get edition name
    print("Enter edition you want to generate metadata for: ")
    while True:
        edition_name = input()
        edition_path, metadata_path, json_path = generate_paths(edition_name)

        if os.path.exists(edition_path):
            print("Edition exists! Generating JSON metadata...")
            break
        else:
            print("Oops! Looks like this edition doesn't exist! Check your output folder to see what editions exist.")
            print("Enter edition you want to generate metadata for: ")
            continue
    
    # Make json folder
    if not os.path.exists(json_path):
        os.makedirs(json_path)
    
    # Get attribute data and zfill count
    df, zfill_count = get_attribute_metadata(metadata_path)
    
    for idx, row in progressbar(df.iterrows()):    
    
        # Get a copy of the base JSON (python dict)
        item_json = deepcopy(BASE_JSON)
        
        # Append number to base name
        item_json['name'] = item_json['name'] + str(idx)

        # Append image PNG file name to base image path
        item_json['image'] = item_json['image'] + '/' + str(idx).zfill(zfill_count) + '.png'
        
        # Convert pandas series to dictionary
        attr_dict = dict(row)
        
        # Add all existing traits to attributes dictionary
        for attr in attr_dict:
            
            if attr == 'File':
                file_path = os.path.join('assets', 'metadata', f'{attr_dict[attr]}.json')
                f = open(file_path)
                json_object = json.load(f)
                
                for key, value in json_object.items():
                    item_json['attributes'].append({ 'trait_type': key, 'value': json_object[key] })
                    
                f.close()

            if attr_dict[attr] != 'none' and attr != 'File':
                item_json['attributes'].append({ 'trait_type': attr, 'value': attr_dict[attr] })
        
        # Write file to json folder
        item_json_path = os.path.join(json_path, str(idx))
        
        with open(item_json_path, 'w') as f:
            json.dump(item_json, f)

run()