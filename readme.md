# Gauthcli

Google Authenticator implementation in python.

## How to use

First install dependencies:

    $ sudo pip3 install requests
    $ sudo pip3 install pillow
    $ sudo pip3 install pyzbar

Then type

    ./gauthcli.py help

to see the usage.

    $ ./gauth.py add-secret <secret> [label] [issuer]
    $ ./gauth.py add-uri <qr-code url or key uri>
    $ ./gauth.py remove-by-label <label>
    $ ./gauth.py list

## Examples

    $ ./gauth.py add-secret HXDMVJECJJWSRB3HWIZR4IFUGFTMXBOZ Example:alice@google.com Example
    $ ./gauth.py add-uri 'otpauth://totp/Example:alice@google.com?secret=HXDMVJECJJWSRB3HWIZR4IFUGFTMXBOZ&issuer=Example'
    $ ./gauth.py remove-by-label 'Example:alice@google.com'

## Notes

Only totp is supported for now.
