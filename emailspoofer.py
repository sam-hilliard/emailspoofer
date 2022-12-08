#!/usr/bin/env python3

import argparse

def main():
    parser = argparse.ArgumentParser(
                    prog = 'EmailSpoofer',
                    description = 'Uses the gmail cloud API to send an email.',
                    epilog = 'Use at your own discretion.')

    parser.add_argument('-t', '--to', action='store_true', help='The address to send the email to.', required=True)
    parser.add_argument('-f', '--from', action='store_true', help='The from address.', required=True)
    parser.add_argument('-s', '--subject', action='store_true', help='The subject of the email.', required=True)
    parser.add_argument('-a', '--auth-file', action='store_true', help='The file path of the credentials.json used for authentication.', required=True)
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-m', '--message', action='store_true', help='The message/body of the email.')
    group.add_argument('-o', '--file', action='store_true', help='The message specified from a file.')

    args = parser.parse_args()

    print(args)


if __name__ == '__main__':
    main()