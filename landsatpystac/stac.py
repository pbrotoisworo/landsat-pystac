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

        # Load scene IDs
        # These scene IDs will be used for other class methods
        self.scene_ids = [x['properties']['landsat:scene_id'] for x in result['features']]
        self.ids = [x['id'] for x in self.result['features']]


class Feature:

    def __init__(self, feature):
        """
        Parse individual scenes (labelled as "feature") in a feature
        collection from a STACResult.

        """
        self._feature = feature
        
        # Attributes
        self.description = self._feature['description']
        self.bbox = self._feature['bbox']
        self.geometry = self._feature['geometry']
        self.timestamp = self._get_property('datetime')
        self.cloud_cover = self._get_property('eo:cloud_cover')
        self.sun_azimuth = self._get_property('view:sun_azimuth')
        self.sun_elevation = self._get_property('view:sun_elevation')
        self.platform = self._get_property('platform')
        self.instruments = self._get_property('instruments')
        self.off_nadir = self._get_property('view:off_nadir')
        self.cloud_cover_land = self._get_property('landsat:cloud_cover_land')
        self.wrs_type = self._get_property('landsat:wrs_type')
        self.wrs_row = self._get_property('landsat:wrs_row')
        self.wrs_path = self._get_property('landsat:wrs_path')
        self.scene_id = self._get_property('landsat:scene_id')
        self.collection_category = self._get_property('landsat:collection_category')
        self.collection_number = self._get_property('landsat:collection_number')
        self.correction = self._get_property('landsat:correction')
        self.epsg = self._get_property('proj:epsg')
        self.shape = self._get_property('proj:shape')
        self.coeff_list = []
        self.coeff_names = {}
        self.qa_list = []
        self.qa_names = []
        self.band_list = []
        self.band_names = {}
        self.s3_tiff_paths = {}
        self.s3_metadata_paths = {}
        self.s3_qa_paths = {}
        self.s3_coeff_paths = {}
        self.landsatlook_tiff_paths = {}
        self.landsatlook_metadata_paths = {}
        self.landsatlook_qa_paths = {}
        self.landsatlook_coeff_paths = {}
        self.thumbnail = None
        self.metadata_txt_path = None
        self.metadata_xml_path = None
        self.metadata_json_path = None
        self.load_assets()

    def _get_property(self, attribute: str) -> str:
        """
        Helper function to get image properties.

        Parameters
        ----------
        attribute: str
            Name of property to load.

        """
        return self._feature['properties'][attribute]

    def load_assets(self):
        """
        Load STAC data that requires a bit more logic to parse.

        """

        mtl_files = ['MTL.txt', 'MTL.json', 'MTL.xml', 'ANG.txt']
        coeff_files = ['VAA', 'VZA', 'SAA', 'SZA']

        # Load band list and S3 path
        for asset in self._feature['assets']:
            
            if asset in coeff_files:
                self.coeff_list.append(self._feature['assets'][asset])
                self.coeff_names[asset] = self._feature['assets'][asset]['title']
                self.s3_coeff_paths[asset] = self._feature['assets'][asset]['alternate']['s3']['href']
                self.landsatlook_coeff_paths[asset] = self._feature['assets'][asset]['href']

            if asset in mtl_files:
                self.s3_metadata_paths[asset] = self._feature['assets'][asset]['alternate']['s3']['href']
                self.landsatlook_metadata_paths[asset] = self._feature['assets'][asset]['href']

            if 'qa_' in asset:

                self.qa_list.append(self._feature['assets'][asset])
                self.qa_names.append(self._feature['assets'][asset]['title'])
                self.landsatlook_qa_paths[asset] = self._feature['assets'][asset]['href']
                self.s3_qa_paths[asset] = self._feature['assets'][asset]['alternate']['s3']['href']
            
            if asset == 'thumbnail':
                self.thumbnail = self._feature['assets'][asset]['href']

            if 'eo:bands' in self._feature['assets'][asset]:

                # Load band data
                data = self._feature['assets'][asset]['eo:bands'][0]
                band_num = data['name']
                self.band_list.append(data)
                self.band_names[band_num] = data['common_name']

                # Load tiff urls
                self.s3_tiff_paths[band_num] = self._feature['assets'][asset]['alternate']['s3']['href']
                self.landsatlook_tiff_paths[band_num] = self._feature['assets'][asset]['href']


if __name__ == '__main__':
    pass
