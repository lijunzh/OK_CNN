import pandas as pd
from aux import ROOT_DIR

def load_catalog(cat_file=None):
    if not cat_file:
        cat_file = "Guthrie_catalog.h5"
    return pd.read_hdf("/".join([ROOT_DIR,
                                 "catalog",
                                 cat_file]),
                       'cat')

if __name__ == '__main__':
    import time

    # Read Catalog into a Pandas dataframe
    t0 = time.time()
    cat_file = "/".join([ROOT_DIR,
                         "catalog",
                         "Guthrie.catalog.15MAD.6chan"])
    cat = pd.read_csv(cat_file, delim_whitespace=True)
    print("Loading catalog from original" 
          "file takes {} second".format(time.time() - t0))
    
    # Save catalog in fast access HDF5 format
    t0 = time.time()
    cat.to_hdf("/".join([ROOT_DIR,
                         "catalog",
                         "Guthrie_catalog.h5"]),
               'cat',
               format='table', mode='w')
    print("Saving catalog to HDF5" 
          "file takes {} second".format(time.time() - t0))
    
    # Load catalog in fast HDF5 format
    t0 = time.time()
    cat = pd.read_hdf("/".join([ROOT_DIR,
                                "catalog",
                                "Guthrie_catalog.h5"]),
                      'cat')
    print("Loading catalog from HDF5"
          "file takes {} second".format(time.time() - t0))

    #----------------------------------------------------------------------# 

    # Count number of events and store in json
    import json
    log = {}
    for i in range(-3, 5):
        mask = (cat['Magnitude'] > i) & (cat['Magnitude'] < i+1)
        count = len(cat[mask].index)
        mag_range = "{:2} ~ {:2}".format(i, i+1)
        log[mag_range] = count

    print(log)
    with open("/".join([ROOT_DIR, 
                        "log", 
                        "magnitude_distribution.json"]), 'w') as f:
        json.dump(log, f)
