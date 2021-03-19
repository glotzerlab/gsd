"""Pytest fixtures common to all tests."""

import pytest
import collections

Mode = collections.namedtuple('Mode', 'read write')
mode_list = [Mode('rb', 'wb'), Mode('rb+', 'wb+')]


def open_mode_name(mode):
    """Provide a name for the open mode fixture."""
    return '(' + mode.read + ',' + mode.write + ')'


@pytest.fixture(params=mode_list, ids=open_mode_name)
def open_mode(request):
    """Pytest fixture parameterized over multiple file open modes."""
    return request.param
