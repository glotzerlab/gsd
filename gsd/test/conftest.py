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

def pytest_addoption(parser):
    """Add GSD specific options to the pytest command line.

    * validate - run validation tests
    """
    parser.addoption(
        "--validate",
        action="store_true",
        default=False,
        help="Enable long running validation tests.",
    )


@pytest.fixture(autouse=True)
def skip_validate(request):
    """Skip validation tests by default.

    Pass the command line option --validate to enable these tests.
    """
    if request.node.get_closest_marker('validate'):
        if not request.config.getoption("validate"):
            pytest.skip('Validation tests not requested.')


def pytest_configure(config):
    """Define the ``validate`` marker."""
    config.addinivalue_line(
        "markers",
        "validate: Tests that perform long-running validations.")
