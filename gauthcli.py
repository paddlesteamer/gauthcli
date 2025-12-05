#!/usr/bin/env python3

import base64
import hashlib
import hmac
import os
import pickle
import struct
import sys
import time
import urllib.parse

config = {
  "directory"  : "{0}/.gauthcli".format( os.path.expanduser("~") ),
  "path"       : "{0}/.gauthcli/secrets.pickle".format( os.path.expanduser("~") )
}

# The otp codes below are taken from this question in stackoverflow:
# https://stackoverflow.com/questions/8529265/google-authenticator-implementation-in-python
# It is slightly edited due to a bug
def get_hotp_token(secret, intervals_no):
  key = ''
  try:
    key = base64.b32decode(secret, True)
  except: # assume hex string
    key = bytes.fromhex(secret)
  msg = struct.pack(">Q", intervals_no)
  h = hmac.new(key, msg, hashlib.sha1).digest()
  try:
    o = ord(h[19]) & 15
  except:
    o = h[19] & 15
  h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
  return h

def get_totp_token(secret):
  return get_hotp_token(secret, intervals_no=int(time.time())//30)

########################################

def loadSecrets():

  if not os.path.isdir( config["directory"] ):
    print("[+] Looks like you're running this first time...")
    os.mkdir( config["directory"] )
    print("[+] Config file is created at {0}".format( config["directory"] ))
    return []  

  if not os.path.isfile( config["path"] ):
    return []

  return pickle.load( open(config['path'], "rb") )

def saveSecrets(secrets):
  pickle.dump( secrets, open(config["path"], "wb") )
  print("[+] Your secrets are updated.")
  

def add(secret, label, issuer):
  secrets = loadSecrets()

  for entry in secrets:

    if entry["secret"] == secret:
      print("[-] You have already added this secret! Nothing is changed.")
      return

  secrets.append({
    "secret" : secret,
    "label"  : label,
    "issuer" : issuer
  })

  saveSecrets(secrets)

def addSecret(args):
  secret = args[0]
  label  = ""
  issuer = ""
    
  if len(args) == 3:
    label  = args[1]
    issuer = args[2]

  elif len(args) == 2:
    label = args[1]

  add(secret, label, issuer)

def addURI(args):
  uri = urllib.parse.urlparse(args[0])

  if "http" in uri.scheme: # Assume qr code link is provided
    import io
    import requests

    from PIL import Image
    from pyzbar.pyzbar import decode

    try:
      r = requests.get(args[0])
    except:
      print("[-] Couldn't reach to {0}. Exiting...".format(args[0]))
      return

    qr = decode(Image.open(io.BytesIO(r.content)))   

    uri = urllib.parse.urlparse(qr[0].data.decode('utf-8'))

  if uri.scheme != "otpauth" or uri.netloc != "totp":
    print("[-] Only totp is supported.")
    return

  query = urllib.parse.parse_qs(uri.query)

  secret = query['secret'][0]
  issuer = query['issuer'][0]

  label = uri.path[1:]

  add(secret, label, issuer)

def addFile(args):
  import io

  from PIL import Image
  from pyzbar.pyzbar import decode

  path = args[0]

  if not os.path.isfile( path ):
    print("[-] {0} is not exist!".format(path))
    return

  qr = decode(Image.open(path))   

  uri = urllib.parse.urlparse(qr[0].data.decode('utf-8'))

  if uri.scheme != "otpauth" or uri.netloc != "totp":
    print("[-] Only totp is supported.")
    return

  query = urllib.parse.parse_qs(uri.query)

  secret = query['secret'][0]
  issuer = query['issuer'][0]

  label = uri.path[1:]

  add(secret, label, issuer)

def eraseLines(n):
  CURSOR_UP_ONE = '\x1b[1A'
  ERASE_LINE = '\x1b[2K'

  for i in range(n):
    sys.stdout.write(CURSOR_UP_ONE)
    sys.stdout.write(ERASE_LINE)

def listCodes():
  secrets = loadSecrets()

  if len(secrets) == 0:
    print("[-] Nothing to list. You need to add some secrets first.")
    return

  import signal

  def sigintHandler(signum, frame):
    sys.exit(0)

  signal.signal(signal.SIGINT, sigintHandler)

  while True:
    prog = int( (int(time.time()) % 30) / 3 )

    
    pbar = "|" + "█"*prog + " "*(9-prog) + "|"

    for entry in secrets:
      print("[+] {0:<30} {1:<20}: {2:<14} {3:11}".format( entry['label'], entry['issuer'], get_totp_token(entry['secret']), pbar ))

    time.sleep(1)

    eraseLines(len(secrets))

def removeEntry(args):
  label = args[0]

  secrets = loadSecrets()

  nsecrets = []
  for entry in secrets:
    if entry['label'] == label: continue

    nsecrets.append(entry)

  saveSecrets(nsecrets)


def usage():
  print("Usage:")
  print("  $ ./{0} add-secret <secret> [label] [issuer]".format(sys.argv[0]))
  print("  $ ./{0} add-uri <qr-code url or key uri>".format(sys.argv[0]))
  print("  $ ./{0} add-file <local qr-code image>".format(sys.argv[0]))
  print("  $ ./{0} remove-by-label <label>".format(sys.argv[0]))
  print("  $ ./{0} list".format(sys.argv[0]))
  print("")
  print("Examples:")
  print("  $ ./{0} add-secret HXDMVJECJJWSRB3HWIZR4IFUGFTMXBOZ Example:alice@google.com Example".format(sys.argv[0]))
  print("  $ ./{0} add-uri 'otpauth://totp/Example:alice@google.com?secret=HXDMVJECJJWSRB3HWIZR4IFUGFTMXBOZ&issuer=Example'".format(sys.argv[0]))
  print("  $ ./{0} add-file qrcode.png".format(sys.argv[0]))
  print("  $ ./{0} remove-by-label 'Example:alice@google.com'".format(sys.argv[0]))



def main(args):
  if len(args) < 2:
    usage()
  elif args[1] == 'add-secret' and len(args) >= 3 and len(args) <=5:
    addSecret(args[2:])
  elif args[1] == 'add-uri' and len(args) == 3:
    addURI(args[2:])
  elif args[1] == 'add-file' and len(args) == 3:
    addFile(args[2:])
  elif args[1] == 'list':
    listCodes()
  elif args[1] == 'remove-by-label' and len(args) == 3:
    removeEntry(args[2:])
  else:
    usage()

if __name__ == '__main__':
  main(sys.argv)
