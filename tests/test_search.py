import pytest

from landsatpystac.search import Search
from landsatpystac.stac import STACResult

# Search bbox is somewhere in Pasig, Metro Manila, Philippines
bbox = [
    121.06985628604887,
    14.553459827553915,
    121.07029080390929,
    14.553885595183766
]

def assert_scene_id(expected, actual):
    assert expected == actual, f'Actual scene ID "{actual}" does not match expected value "{expected}"'

def test_search_scene_id():
    s = Search(scene_id='LC91160502022132LGN00')
    _, results = s.search()
    r = STACResult(results)

    actual = r.scene_ids
    expected = ['LC91160502022132LGN00']
    assert_scene_id(expected, actual)

def test_bbox_and_datetime():
    """
    We search for a specific scene that covers Manila, Philippines
    """

    s = Search(bbox=bbox, date_range='2018-03-05/2018-03-07')
    _, results = s.search()
    r = STACResult(results)
    
    actual = r.scene_ids
    expected = ['LC81160502018065LGN00']
    assert_scene_id(expected, actual)

def test_sort_search():
    """
    Order results using ascending direction
    """
    s = Search(bbox=bbox, date_range='2022-05-01/2022-05-30', platform='LANDSAT_9', sort_col="eo:cloud_cover", sort_order="asc")
    _, results = s.search()
    r = STACResult(results)
    
    actual = [x.cloud_cover for x in r.features]
    expected = [11.84, 57.84]
    assert actual == expected, 'Sorted cloud cover values do not match expected results.'

def test_filter_cloud_level():
    s = Search(bbox=bbox, cloud_cover_max=12, date_range='2021-01-01/2021-06-01', platform='LANDSAT_8')
    _, results = s.search()
    
    r = STACResult(results)
    actual = r.scene_ids
    expected = ['LC81160502021121LGN00', 'LC81160502021057LGN00']
    assert_scene_id(expected, actual)

# Unsure why this fails. Maybe a bug?
# WRS filter works if used by itself.
@pytest.mark.xfail(reason='API returns an error when using WRS filter and date_range at the same time.')
def test_search_wrs():
    """
    Search using WRS Path and Row
    """
    s = Search(wrs_path='116', wrs_row='050', date_range='2022-05-01/2022-05-30')
    _, results = s.search()
    r = STACResult(results)

    actual = r.scene_ids
    expected = ['LC81160502014102LGN01']
    assert_scene_id(expected, actual)


if __name__ == '__main__':
    pass
