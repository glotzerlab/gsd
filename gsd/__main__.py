# Copyright (c) 2020 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.
import sys
import argparse
import code

from .version import __version__
from .hoomd import open as hoomd_open, _hoomd_fl_open


def _print_err(msg=None, *args):
    print(msg, *args, file=sys.stderr)


SHELL_BANNER = """Python {python_version}
gsd {gsd_version}

File:{fn}
{additional_attributes}
The GSD file handle is available via the "handle" variable.
For supported schema, you may access the trajectory using the "traj" variable.
Type "help(handle)" or "help(traj)" for more information.
The gsd and gsd.fl packages are always loaded.
Schema-specific modules (e.g. gsd.hoomd) are loaded if available."""


def main_read(args):
    # Default to a new line for well-formatted printing.
    additional_attributes = "\n"

    if args.schema == 'hoomd':
        handle = _hoomd_fl_open(args.file)
        traj = hoomd_open(handle)
        local_ns = {
            'handle': handle,
            'traj': traj,
            'gsd': sys.modules['gsd'],
            'gsd.hoomd': sys.modules['gsd.hoomd'],
            'gsd.fl': sys.modules['gsd.fl'],
        }
        additional_attributes = "Number of frames={}\n".format(len(traj))
    else:
        raise ValueError("Unsupported schema.")

    code.interact(
        local=local_ns,
        banner=SHELL_BANNER.format(
            python_version=sys.version,
            gsd_version=__version__,
            fn=args.file,
            additional_attributes=additional_attributes))


def main():
    parser = argparse.ArgumentParser(
        description="The gsd package encodes canonical readers and writers for"
                    "the gsd file format.")
    parser.add_argument(
        '--version',
        action='store_true',
        help="Display the version number and exit.")
    subparsers = parser.add_subparsers()

    parser_read = subparsers.add_parser('read')
    parser_read.add_argument(
        'file',
        type=str,
        nargs='?',
        help="GSD file to read.")
    parser_read.add_argument(
        '-c', '--command',
        type=str,
        help="Execute Python program passed as string.")
    parser_read.add_argument(
        '-s', '--schema',
        type=str,
        default='hoomd',
        choices=['hoomd'],
        help="The file schema.")
    parser_read.set_defaults(func=main_read)

    # This is a hack, as argparse itself does not
    # allow to parse only --version without any
    # of the other required arguments.
    if '--version' in sys.argv:
        print('gsd', __version__)
        sys.exit(0)

    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_usage()
        sys.exit(2)
    try:
        args.func(args)
    except KeyboardInterrupt:
        _print_err()
        _print_err("Interrupted.")
        if args.debug:
            raise
        sys.exit(1)
    except RuntimeWarning as warning:
        _print_err("Warning: {}".format(warning))
        if args.debug:
            raise
        sys.exit(1)
    except Exception as error:
        _print_err('Error: {}'.format(error))
        if args.debug:
            raise
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
