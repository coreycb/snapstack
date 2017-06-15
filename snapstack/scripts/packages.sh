#!/bin/bash
#
# A script for testing OpenStack snap packages on a single node.
#

set -ex

sudo apt update
DEBIAN_FRONTEND='noninteractive' sudo -E apt install --yes python3-openstackclient rabbitmq-server mysql-server \
    memcached libvirt-bin qemu-kvm apparmor-utils python-neutronclient openvswitch-switch

SCRIPT=$(readlink -f $0)
export BASE_DIR=$(dirname $SCRIPT)

scripts="rabbitmq database keystone nova neutron glance nova-hypervisor neutron-ext-net"

sudo snap install core
