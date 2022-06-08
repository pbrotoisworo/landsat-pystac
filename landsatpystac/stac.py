# Python file for navigating STAC spec data
from collections import Sequence


class Scene:

    def __init__(self, feature):
        """
        Parse individual scenes (labelled as "feature") in a feature
        collection from a STACResult.

        """
        self._feature = feature

        # Attributes
        self.description = self._feature['description']
        self.id = self._feature['id']
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

    def __str__(self):
        return f'ID: {self.scene_id}\nTimestamp: {self.timestamp}'

    def __repr__(self):
        return f'ID: {self.scene_id}\nTimestamp: {self.timestamp}'

    def _get_property(self, attribute: str) -> str:
        """
        Helper function to get image properties.

        Parameters
        ----------
        attribute: str
            Name of property to load.

        """
        try:
            return self._feature['properties'][attribute]
        except KeyError:
            return None

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


class STACResult(Sequence):

    def __init__(self, result):
        """
        Handle scenes from a STACResult as a single group.
        `STACResult` is an interable sequence.

        Parameters
        ----------
        result: dict
            The result from `landsatpystac.search.Search() method`

        """
        self.result = result
        self.features = []
        self._n = 0
        for item in self.result['features']:
            self.features.append(Scene(item))

        # Metadata of results
        self.meta = self.result['meta']

        # Get list of properties from each scene
        self.ids = [x.id for x in self.features]
        self.scene_ids = [x.scene_id for x in self.features]
        self.cloud_cover = [x.cloud_cover for x in self.features]
        self.cloud_cover_land = [x.cloud_cover_land for x in self.features]

    def __iter__(self):
        """
        Index for loop
        
        """
        self._n = 0
        return self

    def __next__(self):
        """
        Logic for class iteration

        """
        if self._n < len(self.features):
            if self._n + 1 != len(self.features):
                self._n += 1
            else:
                raise StopIteration
            return self.features[self._n]
        else:
            raise StopIteration

    def __getitem__(self, index):
        """
        Make class indexable.

        """
        return self.features[index]

    def __len__(self):
        """
        `len()` of class is based on number of scenes in
        `self.features`.

        """
        return len(self.features)


if __name__ == '__main__':
    pass
