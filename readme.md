# Gauthcli

Google Authenticator implementation in python.

## How to use

First install dependencies:

    $ sudo pip3 install -r requirements.txt

Then type

    ./gauthcli.py help

to see the usage.

    $ ./gauthcli.py add-secret <secret> [label] [issuer]
    $ ./gauthcli.py add-uri <qr-code url or key uri>
    $ ./gauthcli.py remove-by-label <label>
    $ ./gauthcli.py list

## Examples

    $ ./gauthcli.py add-secret HXDMVJECJJWSRB3HWIZR4IFUGFTMXBOZ Example:alice@google.com Example
    $ ./gauthcli.py add-uri 'otpauth://totp/Example:alice@google.com?secret=HXDMVJECJJWSRB3HWIZR4IFUGFTMXBOZ&issuer=Example'
    $ ./gauthcli.py remove-by-label 'Example:alice@google.com'

## Notes

Only totp is supported for now.
