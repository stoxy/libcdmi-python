#!/usr/bin/env python
"""
CLI wrapper around libcdmi

Manipulates CDMI objects, stores file data and metadata to a CDMI server (like STOXY)
"""

import argparse
import os

import libcdmi


LIBCDMI_ACTIONS = ['create_container',
                   'create_object',
                   'delete',
                   'head',
                   'get',
                   'update_container',
                   'update_object']


def create_parser():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('action', choices=LIBCDMI_ACTIONS,
                        help='Action to perform on the URL')
    parser.add_argument('url', help='URL of the object to apply action to')
    parser.add_argument('-f', '--filename',
                        help='Input file path (required, when calling create* and update*)')
    parser.add_argument('-m', '--mimetype', default='text/plain',
                        help='Input file MIME-type')
    parser.add_argument('-u', '--auth', help='Authentication credentials (user:password)')
    parser.add_argument('-o', '--output', choices=['json', 'yaml', 'raw'],
                        help='Pretty-print in a format specified (YAML, JSON or raw dict)')
    return parser


def run(args, print_=True):
    credentials = tuple(args.auth.split(':')) if args.auth else None
    c = libcdmi.open(args.url, credentials=credentials)

    if args.action != 'create_object':
        response = getattr(c, args.action)('')
    else:
        if not args.filename:
            return {'_error': 'Filename is mandatory with create_object'}
        if not os.path.exists(args.filename):
            return {'_error': 'File does not exist: "%s"' % args.filename}
        response = getattr(c, args.action)('', args.filename, mimetype=args.mimetype)

    if not response:
        return

    if not print_:
        return response

    if args.output == 'yaml':
        import yaml
        print yaml.dump(response)
    elif args.output == 'json':
        import json
        print json.dumps(response, indent=4, separators=(', ', ': '), sort_keys=True)
    else:
        from pprint import pprint
        pprint(response)


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    run(args)
