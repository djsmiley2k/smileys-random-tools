#!/usr/bin/python3

# Display status of VPNs terminated within NSX
# Created Jul 2020
# Tim Bowers

import argparse
import datetime
import contextlib
import os

import requests
from lxml import etree




@contextlib.contextmanager
def absorb_stderr():
    with open(os.devnull, 'w') as devnull:
        with contextlib.redirect_stderr(devnull):
            yield


def get_vpn_status(user, password, url):
    """Login to NSX, get list of edges."""
    #print("Logging into " + url + " with username " + user)
    request_args = dict(
        auth=(user, password),
        verify=False,
        headers={
            'Accept': 'application/xml',
            'Content-Type': 'application/xml',
        },
    )

    with absorb_stderr():
        all_edges = requests.get(url, **request_args)

    data = {}

    # Convert result of call into XML object
    tree = etree.fromstring(all_edges.text.encode())

    # Create a dict containing all the edges
    data['edges'] = {}

    for edge_summary in tree[0]:
        if edge_summary.tag == 'pagingInfo':
            continue

        current_edge = {}

        for attribute_tag in edge_summary.iter('objectId', 'name'):
            current_edge[attribute_tag.tag] = attribute_tag.text

        data['edges'][current_edge['objectId']] = {
            'name': current_edge['name'],
        }

    # For each edge, check for VPN and VPN status
    for id, edge in data['edges'].items():
        edge_url = f'{url}/{id}/ipsec/statistics'

        with absorb_stderr():
           vpn_state = requests.get(edge_url, **request_args)

        vpn_tree = etree.fromstring(vpn_state.text.encode())

        # Create a dict of tunnels - keyed by network CIDR
        edge['tunnels'] = tunnels = {}

        if not len(vpn_tree):
            continue

        for site_statistics in vpn_tree:
            if site_statistics.tag != 'siteStatistics':
                continue

            for tunnel_stats in site_statistics.iter('tunnelStats'):
                current_tunnel = {}

                for attribute_tag in tunnel_stats.iter('tunnelStatus','peerSubnet'):
                    current_tunnel[attribute_tag.tag] = attribute_tag.text
                    #print(current_tunnel)

                #print("Checking tunnel" + current_tunnel['peerSubnet'] + ", with status " + current_tunnel['tunnelStatus'])

                if(tunnels.get(current_tunnel['peerSubnet']) == 'up'):
                #if(tunnels['peerSubnet'] = current_tunnel['peerSubnet'] and tunnels[''] =='up'):
                  print("Not adding duplicate down status: " + current_tunnel['peerSubnet'] + " = "  + current_tunnel['tunnelStatus'])
                else:
                  print("Adding tunnel status: " + current_tunnel['peerSubnet'] + " = " + current_tunnel['tunnelStatus'])
                  tunnels[current_tunnel['peerSubnet']] = current_tunnel['tunnelStatus']
                  #print(current_tunnel)

        if all(tunnel == 'up' for tunnel in edge['tunnels'].values()):
            edge['status'] = 'OK'
        else:
            edge['status'] = 'ERROR'

    return data


def show_vpn_status(data, html_output=False):
    if not html_output:
        print(data)
        return

    # Lazy loading on purpose - optional dependency.
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']),
    )
    print(env.get_template('show_vpn_status.html').render(
        data=data,
        now=datetime.datetime.now(),
    ))


def get_nonempty_input(prompt, value_name):
    value = ''

    while not value:
        value = input(f'{prompt}: ')
        if not value:
            print(f'A {value_name} must be provided to continue.')

    return value


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-u', '--user', help='NSX Manager username')
    parser.add_argument('-p', '--password', help='NSX Manager password')
    parser.add_argument('-url', '--url', help='NSX Manager URL')
    parser.add_argument(
        '--html',
        action='store_true',
        default=False,
        dest='html',
        help='Enables html output formatting',
    )

    args = parser.parse_args()

    if not args.user:
        args.user = get_nonempty_input('Username for logging in', 'username')

    if not args.password:
        args.password = get_nonempty_input('Password', 'password')

    if not args.url:
        args.url = get_nonempty_input('URL of NSX Manager', 'url')

    data = get_vpn_status(args.user, args.password, args.url)
    show_vpn_status(data, args.html)
