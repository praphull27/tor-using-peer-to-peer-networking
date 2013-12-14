import StringIO
import socket
import urllib

import neehi  # SocksiPy module
import stem.process

from stem.util import term

SOCKS_PORT = 9050

# Set socks proxy and wrap the urllib module

neehi.setdefaultproxy(neehi.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
socket.socket = neehi.socksocket

# Perform DNS resolution through the socket

def getaddrinfo(*args):
  return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

socket.getaddrinfo = getaddrinfo


def query(url):
  """
  Uses urllib to fetch a site using SocksiPy for Tor over the SOCKS_PORT.
  """

  try:
    return urllib.urlopen(url).read()
  except:
    return "Unable to reach %s" % url


# Start an instance of tor configured to only exit through Russia. This prints
# tor's bootstrap information as it starts. Note that this likely will not
# work if you have another tor instance running.

def print_bootstrap_lines(line):
#  if "Bootstrapped " in line:
#    print term.format(line, term.Color.BLUE)
  print term.format(line, term.Color.BLUE)


print term.format("Starting Tor:\n", term.Attr.BOLD)

tor_process = stem.process.launch_tor(
  torrc_path = '/home/praphull/torrc_No_Sharing_n2',
  init_msg_handler = print_bootstrap_lines,
)

print term.format("\nChecking our endpoint:\n", term.Attr.BOLD)
print term.format(query("https://www.atagar.com/echo.php"), term.Color.BLUE)

'''
from stem import CircStatus
from stem.control import Controller

with Controller.from_port(port=9051) as controller:
  pass

  controller.authenticate()
#  controller.signal(Signal.NEWNYM)

  for circ in controller.get_circuits():
    if circ.status != CircStatus.BUILT:
      continue

    exit_fp, exit_nickname = circ.path[-1]

    exit_desc = controller.get_network_status(exit_fp, None)
    exit_address = exit_desc.address if exit_desc else 'unknown'

    print "Exit relay"
    print "  fingerprint: %s" % exit_fp
    print "  nickname: %s" % exit_nickname
    print "  address: %s" % exit_address
'''

#from stem.connection import connect_port
#controller = connect_port(9051)

#tor_process.kill()  # stops tor
