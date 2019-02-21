# Gauthcli

Google Authenticator implementation in python.

## How to use

First install dependencies:

    $ sudo pip3 install -r requirements.txt

Then type

    ./gauthcli.py help

to see the usage.

    $ ./gauth.py add-secret <secret> [label] [issuer]
    $ ./gauth.py add-uri <qr-code url or key uri>
    $ ./gauthcli.py add-file <local qr-code image>
    $ ./gauth.py remove-by-label <label>
    $ ./gauth.py list

## Examples

    $ ./gauth.py add-secret HXDMVJECJJWSRB3HWIZR4IFUGFTMXBOZ Example:alice@google.com Example
    $ ./gauth.py add-uri 'otpauth://totp/Example:alice@google.com?secret=HXDMVJECJJWSRB3HWIZR4IFUGFTMXBOZ&issuer=Example'
    $ ./gauth.py add-uri 'https://www.google.com/chart?chs=200x200&chld=M|0&cht=qr&chl=otpauth://totp/Example%3Aalice%40google.com%3Fsecret%3DHXDMVJECJJWSRB3HWIZR4IFUGFTMXBOZ%26issuer%3DExample'
    $ ./gauthcli.py add-file qrcode.png
    $ ./gauth.py remove-by-label 'Example:alice@google.com'

## Notes

Only totp is supported for now.
