from pathlib import Path
import requests
import os

def upload_to_ipfs(filepath, name):
  #Open file
  with Path(filepath).open("rb") as fp:
    image_binary = fp.read()

    #Local IPFS service
    ipfs_url = "http://localhost:5001"

    #Upload to local IPFS instance
    response = requests.post(
        ipfs_url + "/api/v0/add", files={"file": image_binary})

    #Save IPFS hash (location) from response
    ipfs_hash = response.json()['Hash']

    #Save full URI for IPFS 
    uriForOpenSea = "ipfs://{}".format(ipfs_hash)


    requests.post(
       "{}/api/v0/pin/remote/add?arg={}&name={}&service=Pinata".format(ipfs_url, ipfs_hash, name))

    return uriForOpenSea

upload_to_ipfs(os.path.join('output/edition test1'), 'test')