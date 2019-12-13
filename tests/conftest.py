import pytest
import collections

Mode = collections.namedtuple('Mode', 'read write')
mode_list = [Mode('rb', 'wb'), Mode('rb+', 'wb+')]


def open_mode_name(mode):
    return '(' + mode.read + ',' + mode.write + ')'

@pytest.fixture(params=mode_list,
                ids=open_mode_name)
def open_mode(request):
    return request.param
