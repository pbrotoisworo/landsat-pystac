# Python file for navigating STAC spec data

class STACResult:

    def __init__(self, result: dict) -> None:
        """
        Access STAC search results.

        Parameters
        ----------
        result: dict
            Results of STAC search in dictionary format.

        """
        self.result = result
        self.platform = None
        self.scene_ids = []
        self.ids = []
        self.thumbnail_small_urls = {}
        self.thumbnail_large_urls = {}
        self.s3_urls = {}
        self._load_stac_results()

    def _load_stac_results(self):
        """
        Interpret the STAC results and store them in class attributes.
        """
        # Load platform name(s)
        self.platform = [x['properties']['platform'] for x in self.result['features']]
        if len(set(self.platform)) == 1:
            self.platform = self.platform[0]
        
        # Load a list of scene ids that were returned by the query
        self.scene_ids = [x['properties']['landsat:scene_id'] for x in self.result['features']]
        self.ids = [x['id'] for x in self.result['features']]

        ######################
        # Load asset data
        ######################
        
        # Get S3 paths
        # Iterate through feature and check platform name first
        for item in self.result['features']:
            feature = item

            # Get ID
            id = feature['id']
            
            platform = feature['properties']['platform']
            if platform in ['LANDSAT_9', 'LANDSAT_8']:
                bands = [
                    'coastal', 'blue', 'green', 'red', 'nir08',
                    'swir16', 'swir22', 'pan', 'cirrus', 'lwir11',
                    'lwir12'
                ]
            else:
                raise ValueError(f'Unknown platform name: "{self.platform}"')

            # Build S3 list
            self.s3_urls[id] = {}
            for band in bands:
                self.s3_urls[id][band] = feature['assets'][band]['alternate']['s3']['href']

            # Build thumbnail list
            self.thumbnail_small_urls[id] = feature['assets']['thumbnail']['href']
            self.thumbnail_large_urls[id] = feature['assets']['reduced_resolution_browse']['href']


if __name__ == '__main__':
    pass
