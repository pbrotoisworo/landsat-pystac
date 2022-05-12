# Search Landsat catalogue
import requests
from typing import Union

from landsatpystac.validators import check_if_int, check_if_string
from landsatpystac.errors import SearchError


class JsonConstructor:

    def __init__(self, limit: int = 10) -> None:
        """
        Create JSON data that is used to easily search through the 
        USGS Landsat archive using STAC methods.

        Init arguments and class parameters provide the most important
        functions but other query filtering options can be manually 
        added using the `set_metadata` method.

        Parameters
        ----------
        limit: int
            Maximum scenes to return in the search. Default is 10 scenes.

        """
        self.params = {}
        self._limit = limit
        self._wrs_path = None
        self._wrs_row = None
        self._cloud_cover_max = None
        self._image_shape = None
        self._collection = None
        self._platform = None
        self._manual_json_params = {}

        # Properties that don't need error checking
        self.id = None
        self.scene_id = None

    def generate_json(self):
        """
        Generate JSON output used to create POST request. This will loop
        through all class attributes which are not None and include them
        in the output JSON. Will not include `Search.json` class 
        attribute.

        Important note: If user has manually inputted variables using the
        `set_metadata` method then priority will be given to existing data
        written by the `set_metadata` method.

        """
        query_label = 'query'
        json_out = {query_label: {}}
        if self._manual_json_params:
            for k, v in self._manual_json_params.items():
                json_out[query_label][k] = v

        # Loop through class attributes
        for k, v in self.params.items():
            json_out[query_label][k] = v


        # skip_attrs = ['json']
        # for k, v in self.__dict__.items():
        #     # Class attrs to ignore or
        #     # If exists through manual input then ignore
        #     if k in skip_attrs or k in self.json.keys():
        #         continue
        #     # Ignore class attrs that are None
        #     if not v:
        #         continue
        #     self.json[k] = v
        return json_out
        
    def set_metadata(self, metadata: dict) -> None:
        """
        Manually set metadata in a single batch operation using a 
        dictionary as input. The key is the name of the element and value
        is the value for the specified element.

        Manually setting metadata will allow user to modify search
        parameters with any element and value but no error checking will 
        be done so the user must ensure the inputs are valid.

        Parameters
        ----------
        metadata: dict
            Dictionary where key is the name of elements to add and value
            is the value to set for the specified element.

        Returns
        -------
        None

        """
        for k, v in metadata.items():
            self.json[k] = v
            # Save metadata in self._manual_json_params attr
            self._manual_json_params[k] = v

    @property
    def collection(self):
        return self._collection

    @collection.setter
    def collection(self, val):
        valid = ['landsat-c2l1']
        if val not in valid:
            raise SearchError(f'Collection "{val}" not a valid collection.')
        self._collection = val

    @property
    def platform(self):
        return self._platform

    @platform.setter
    def platform(self, val):
        valid = ['LANDSAT_1', 'LANDSAT_2', 'LANDSAT_3', 'LANDSAT_4',
        'LANDSAT_5', 'LANDSAT_6', 'LANDSAT-7', 'LANDSAT_8', 'LANDSAT_9']
        if val not in valid:
            raise SearchError(f'Platform "{val}" not a valid platform.')
        self._platform = {'platform': val}
        self.params['platform'] = val

    @property
    def image_shape(self):
        return self._image_shape
    
    @image_shape.setter
    def image_shape(self, val: list):
        """
        Set filter for image shape
        """
        if not isinstance(val, list):
            raise ValueError('Image shape requires a list with 2 integers as input.')
        self._image_shape = {'proj:shape': val}
        self.params['proj:shape'] = val

    @property
    def cloud_cover_max(self):
        return self._cloud_cover_max
    
    @cloud_cover_max.setter
    def cloud_cover_max(self, val):
        """
        Set max cloud cover filter.
        """
        check_if_int(val)
        if val < 0 or val > 100:
            raise ValueError('Cloud cover value is not an integer ranging from 0 and 100.')
        self._cloud_cover_max = {'eo:cloud_cover': val}
        self.params['eo:cloud_cover'] = val

    @property
    def wrs_path(self):
        return self._wrs_path
    
    @wrs_path.setter
    def wrs_path(self, val: str) -> str:
        """
        Set WRS Path filter. 
        """
        check_if_string(val)

        # Error checking
        # Generate a list of strings with zero padded numbers ranging from
        # 001 to 255
        valid_vals = range(0, 255)
        valid_vals = map(lambda x: str(x).zfill(3), valid_vals)

        if val not in valid_vals:
            raise SearchError(f'Input WRS path {val} is invalid.')
        self._wrs_path = {'landsat:wrs_path': val}
        self.params['landsat:wrs_path'] = val

    @property
    def wrs_row(self) -> str:
        return self._wrs_row

    @wrs_row.setter
    def wrs_row(self, val: str):
        """
        Set WRS row filter.
        """
        check_if_string(val)

        # Error checking
        # Generate a list of strings with zero padded numbers ranging from
        # 001 to 248
        valid_vals = range(0, 248)
        valid_vals = map(lambda x: str(x).zfill(3), valid_vals)

        if val not in valid_vals:
            raise SearchError(f'Input WRS row {val} is invalid.')
        self._wrs_row = {'landsat:wrs_row': val}
        self.params['landsat:wrs_row'] = val


def default_search_parameters(
    wrs_path: Union[str, None]=None,
    wrs_row: Union[str, None]=None
    ):
    """
    Create a basic search request for Landsat STAC search. Mainly used for
    testing purposes.

    Parameters
    ----------
    wrs_path: str, None
        Input Landsat WRS path value to include with default search 
        parameters.
    wrs_row : str, None
        Input Landsat WRS row value to include with default search
        parameters.

    Returns
    -------
    dict
        JSON search request in a dictionary object.

    """
    json = {
        "query": {
            "eo:cloud_cover": {"lt": 50},
            "view:off_nadir": {"lt": 100},
            "collections": ["landsat-c2l1"]
        },
        "limit": 10
    }
    if wrs_path:
        json["landsat:wrs_path"] = wrs_path
    if wrs_row:
        json["landsat:wrs_row"] = wrs_row    


class Search:

    def __init__(self, limit=10, cloud_cover_max=100, wrs_path=None,
        wrs_row=None, image_shape=None, collection='landsat-c2l1',
        scene_id=None, id=None, platform='LANDSAT_9', **kwargs
        ) -> None:
        """
        Instantiate a search object with the required search parameters.
        """
        self.json_handler = JsonConstructor(limit)
        self._URL_STAC_SEARCH = 'https://landsatlook.usgs.gov/sat-api/stac/search'
        self.response = None

        # Load search arguments
        if cloud_cover_max:
            self.json_handler.cloud_cover_max = cloud_cover_max
        if wrs_path:
            self.json_handler.wrs_path = wrs_path
        if wrs_row:
            self.json_handler.wrs_row = wrs_row
        if collection:
            self.json_handler.collection = collection
        if platform:
            self.json_handler.platform = platform
        if scene_id:
            self.json_handler.scene_id = scene_id
        if id:
            self.json_handler.id = id
        if image_shape:
            self.json_handler.image_shape = image_shape

    @property
    def parameters(self):
        return self.json_handler.generate_json()

    def search(self, raise_error_if_failed=True) -> tuple:
        """
        Search Landsat database.

        Parameters
        ----------
        raise_error_if_failed: bool
            If True, it will raise an Exception if status code is not 200.

        Returns
        -------
        tuple
            Tuple where zero index is the response status code from the
            POST request. The first index is the JSON response.

        """
        search_params = self.json_handler.generate_json()
        r = requests.post(url=self._URL_STAC_SEARCH, json=search_params)
        if r.status_code != 200 and raise_error_if_failed:
            raise SearchError(f'POST request failed. Status code {r.status_code}')
        self.response = r.json()
        return r.status_code, self.response

        
if __name__ == '__main__':
    pass
