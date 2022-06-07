from landsatpystac.search import Search
from landsatpystac.stac import STACResult

def assert_scene_id(expected, actual):
    assert expected == actual, f'Actual scene ID "{actual}" does not match expected value "{expected}"'

def test_search_scene_id():
    s = Search(scene_id='LC91160502022132LGN00')
    response_code, results = s.search()
    if response_code != 200:
        raise ValueError('Error uploading search parameters. Test results will not valid.')
    r = STACResult(results)

    actual = r.scene_ids
    expected = ['LC91160502022132LGN00']
    assert_scene_id(expected, actual)

def test_bbox_and_datetime():
    """
    We search for a specific scene that covers Manila, Philippines
    """
    # bbox is somewhere in Pasig City, Philippines
    bbox = [
    121.06985628604887,
    14.553459827553915,
    121.07029080390929,
    14.553885595183766
    ]

    s = Search(bbox=bbox, date_range='2018-03-05/2018-03-07')
    _, results = s.search()
    r = STACResult(results)
    
    actual = r.scene_ids
    expected = ['LC81160502018065LGN00']
    assert_scene_id(expected, actual)


if __name__ == '__main__':
    pass
