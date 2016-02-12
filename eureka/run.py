import argparse

import configure

import eureka.application


def parse_args():
    """
    Add command-line arguments here
    """
    # command line arguments parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config',
        required=True,
        help='path to application config',
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    # load system config and start application
    eureka.application.Application(
        configure.Configuration.from_file(
            args.config
        ).configure()
    ).run()
