import sqlite3
import subprocess
import os
import json

_listnodes = [
    #{"Title": "Note test 1", "Body": "asdasdasdasdasdasd"},
]

_cwd = os.getcwd()

def get_nodes():

    child = subprocess.Popen(['tailscale', 'status','--json'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    _nodes = json.loads( child.stdout.read() )
    _peers = _nodes["Peer"]

    for _item in _peers:
        _key = _item

        if _peers[_key]['ExitNodeOption'] == True:
            print(_peers[_key]["HostName"])
            _exitnode = _peers[_key]["ExitNode"]
            _host = _peers[_key]["HostName"]
            _ip = _peers[_key]["TailscaleIPs"][0]
            _title = f"{_host} ( {_ip} )"
            if _exitnode:
                _body = "active"
            else:
                _body = "inactive"
            _listnodes.append({"Title": _title, "Body": _body, "IP": _ip, "status": ""})


def localdb_con():
    global _listnodes
    get_nodes()

    return _listnodes

def status_reset(_ip):

    for _node in _listnodes:
        if _node["IP"] == _ip:
            child = subprocess.Popen(['tailscale', 'up', '--exit-node='], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                     universal_newlines=True)

def set_exit_node(_ip):
    child = subprocess.Popen(['tailscale', 'up', '--exit-node='+_ip], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             universal_newlines=True)

def clear_listnodes():
    global _listnodes
    _listnodes = []

def getNode(_id):
    return _listnodes[_id]

def disconnect_all():
    child = subprocess.Popen(['tailscale', 'up', '--exit-node='], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             universal_newlines=True)
