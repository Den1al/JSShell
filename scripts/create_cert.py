from argparse import ArgumentParser
from subprocess import call


parser = ArgumentParser('')
parser.add_argument('domain', help='the domain to create the cert for', default='from config.json')
parser.add_argument('-e', '--email', help='the email to register with', default='me@<domain>')


def main():
    args = parser.parse_args()

    if args.email == 'me@<domain>':
        args.email = f'me@{args.domain}'

    call([
        'sudo', 'certbot', 
        'certonly', '--standalone', 
        '--preferred-challenge', 'http',
        '-d', args.domain,
        '-m', args.email,
        '--agree-tos'
    ])


if __name__ == "__main__":
    main()

