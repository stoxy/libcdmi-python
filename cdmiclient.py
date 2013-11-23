from libcdmi.cli import run, create_parser

if __name__ == '__main__':
    parser = create_parser()
    run(parser.parse_args())

