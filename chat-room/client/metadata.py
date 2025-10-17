import json 
from hatchling.metadata.plugin.interface import MetadataHookInterface

class JSONMetaDataHook(MetadataHookInterface):
    def update(self, metadata):
        with open("metadata.json") as src:
            constants = json.load(src)

            metadata["version"] = constants["version"]
            metadata["authors"] = [
                {
                    "name": author["name"],
                    "email": author["email"]
                } for author in constants["authors"]
            ]
            metadata["license"] = constants["license"]

