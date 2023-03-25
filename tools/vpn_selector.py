import os
import random
import time
import subprocess
from os import listdir
from os.path import isfile, join
from config.config import config


class VpnSelector:

    def __init__(self):
        self.vpn_provider = None
        self.vpn_region = None
        self.vpn_login = None
        self.vpn_password = None
        self.tools_path = 'tools'

    def find_vpn_region(self):
        ovpn_files = [f for f in listdir(os.path.join(self.tools_path, self.vpn_provider)) if isfile(join(os.path.join(self.tools_path, self.vpn_provider), f))]
        return random.choice(ovpn_files)

    def connect_to_cyberghost(self, region, bot, bot_sql):
        self.vpn_region = region
        os.system("sudo cyberghostvpn --country-code {0} --city '{1}' --server {2} --connect".format(
            self.vpn_region.split('|')[0],
            self.vpn_region.split('|')[1],
            self.vpn_region.split('|')[2]))
        time.sleep(20)
        ethernet = os.listdir('/sys/class/net/')
        if 'tun0' in ethernet:
            return True
        else:
            new_region = os.popen("sudo cyberghostvpn --country-code {0} --city '{1}'".format(self.vpn_region.split('|')[0], self.vpn_region.split('|')[1])).read()
            search_server = self.vpn_region.split('|')[1].replace(" ", "").lower()
            all_servers = []
            for server in new_region.split('+')[10].split(self.vpn_region.split('|')[1]):
                if search_server in server:
                   all_servers.append(server.split(' | ')[1])
            new_server = random.choice(all_servers).replace(" ", "")
            os.system("sudo cyberghostvpn --country-code {0} --city '{1}' --server {2} --connect".format(
                self.vpn_region.split('|')[0],
                self.vpn_region.split('|')[1],
                new_server))
            time.sleep(20)
            ethernet = os.listdir('/sys/class/net/')
            if 'tun0' in ethernet:
                new_server = "{0}|{1}|{2}".format(self.vpn_region.split('|')[0], self.vpn_region.split('|')[1], new_server)
                bot_sql.update_bot_vpn_region(new_server, bot)
                return True
            else:
                return False

    def add_config(self, config_file):
        with open("/etc/openvpn/pass.txt", "w") as f:
            f.write(self.vpn_login + "\n")
            f.write(self.vpn_password)
        region_file = open(config_file, 'r')
        conf_list = region_file.readlines()
        region_file.close()
        found = False
        for line in conf_list:
            if "/etc/openvpn/pass.txt" in line:
                found = True
        if not found:
            region_file = open(config_file, 'a')
            region_file.write("auth-user-pass /etc/openvpn/pass.txt\n")
            region_file.close()

    def connect_to_vpn(self, provider, region, login, password, ca, bot, bot_sql):
        self.vpn_region = region
        self.vpn_provider = provider
        self.vpn_login = login
        self.vpn_password = password
        if os.path.isfile(os.path.join(self.tools_path, self.vpn_provider, self.vpn_region)):
            print("Config exist")
        else:
            print("Config not exist")
            self.vpn_region = self.find_vpn_region()
            bot_sql.update_bot_vpn_region(bot, self.vpn_region)
        print(os.getcwd())
        config_file = os.path.join(self.tools_path, self.vpn_provider, self.vpn_region)
        self.add_config(config_file)
        if ca is not None:
            ca_file = os.path.join(self.tools_path, self.vpn_provider, ca)
            subprocess.Popen(["sudo", "/usr/sbin/openvpn", "--config", config_file, "--ca", ca_file])
        else:
            subprocess.Popen(["sudo", "/usr/sbin/openvpn", "--config", config_file])
        time.sleep(15)
        ethernet = os.listdir('/sys/class/net/')
        if 'tun0' in ethernet:
            return True
        else:
            return False

    def check_vpn(self):
        ethernet = os.listdir('/sys/class/net/')
        if 'tun0' in ethernet:
            return True
        else:
            return False

