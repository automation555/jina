import pytest

from google.protobuf.struct_pb2 import ListValue

from jina.types.list import ListView


def test_empty_struct_view():
    list = ListValue()
    view = ListView(list)
    assert len(view) == 0


@pytest.fixture()
def list_proto():
    list = ListValue()
    l = [0, 1, 'hey', {'key': 'value'}, [0, 1, 2]]
    list.extend(l)
    return list


def test_list_view(list_proto):
    view = ListView(list_proto)
    assert len(view) == 5
    assert view[0] == 0
    assert view[1] == 1
    assert view[2] == 'hey'
    assert view[3] == {'key': 'value'}
    assert len(view[4]) == 3
    assert view[4][0] == 0
    assert view[4][1] == 1
    assert view[4][2] == 2


def test_list_view_set_items(list_proto):
    view = ListView(list_proto)
    view[0] = 20
    view[1] = 'now string'
    view[2] = {'key': 'value'}
    view[3]['key'] = 50
    view[4][0] = {'new_key': 'new_value'}
    assert view[0] == 20
    assert view[1] == 'now string'
    assert view[2] == {'key': 'value'}
    assert view[3] == {'key': 50}
    assert view[4][0] == {'new_key': 'new_value'}
    assert view[4][1] == 1
    assert view[4][2] == 2
    view[4][0]['new_key'] = None
    assert view[4][0] == {'new_key': None}


def test_list_view_delete(list_proto):
    view = ListView(list_proto)
    del view[1]
    assert len(view) == 4
    assert view[0] == 0
    assert view[1] == 'hey'
    assert view[2] == {'key': 'value'}
    assert len(view[3]) == 3
    assert view[3][0] == 0
    assert view[3][1] == 1
    assert view[3][2] == 2


# def test_struct_view_clear(struct_proto):
#     view = StructView(struct_proto)
#     view.clear()
#     assert len(view) == 0
#
#
# def test_struct_view_iterate(struct_proto):
#     view = StructView(struct_proto)
#     assert set(view.keys()) == {
#         'key_int',
#         'key_float',
#         'key_string',
#         'key_array',
#         'key_nested',
#     }
#     assert set([key for key, value in view.items()]) == {
#         'key_int',
#         'key_float',
#         'key_string',
#         'key_array',
#         'key_nested',
#     }
#     assert set([element for element in view]) == {
#         'key_int',
#         'key_float',
#         'key_string',
#         'key_array',
#         'key_nested',
#     }
#
#
# def test_struct_view_update(struct_proto):
#     view = StructView(struct_proto)
#     update_dict = {'new_dict': 'new_value'}
#     view.update(update_dict)
#     assert len(view) == 6
#     assert 'new_dict' in view.keys()
#     assert view['new_dict'] == 'new_value'
#
#     update_dict2 = {'key_int': 100}
#     view.update(update_dict2)
#     assert len(view) == 6
#     assert 'new_dict' in view.keys()
#     assert view['key_int'] == 100
#
#     update_dict3 = {'key_nested': {'new_key_nested': 'very_new'}}
#     view.update(update_dict3)
#     assert len(view) == 6
#     assert len(view['key_nested'].keys()) == 1
#     assert view['key_nested']['new_key_nested'] == 'very_new'
#
#
# def test_struct_view_dict():
#     struct = Struct()
#     d = {'a': 1, 'b': 2}
#     struct.update(d)
#     view = StructView(struct)
#     assert view.dict() == d
#
#
# def test_struct_contains(struct_proto):
#     view = StructView(struct_proto)
#     assert 'key_nested' in view
#     assert not 'a' in view
