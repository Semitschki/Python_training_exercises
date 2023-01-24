"""This module is for subnetting."""

MAX_SUFFIX = 32


def change_octet(ip_address, mask):
    """This function create integer octets."""
    ip_address = ip_address.split(".")
    mask = mask.split(".")
    ip_address = [int(octet) for octet in ip_address]
    mask = [int(octet) for octet in mask]
    return (ip_address, mask)


def suffix_to_netmask(netmask):
    """Function to switch slash-notation to octet-notation of netmask."""
    if "/" not in netmask:
        return netmask
    new = netmask.strip("/")
    mask = int(new)
    bits = "1" * mask + "0" * (MAX_SUFFIX - mask)
    new_mask = ".".join(
        [str(int(i, 2))
         for i in [bits[0:8], bits[8:16], bits[16:24], bits[24:32]]]
    )
    return new_mask


def netmask_to_suffix(netmask):
    """Function to switch octet-notation to slash-notation"""
    end_mask = sum(bin(int(number)).count("1") for number in netmask.split("."))
    return end_mask


class Network:
    """Class to find out the broadcast-address, network-address, usable_host in a network."""
    def __init__(self, ip_address, mask):
        self.ip_address = ip_address
        self.mask = suffix_to_netmask(mask)

    def get_network(self):
        """This method calculate the network address."""
        (net_ip, netmask) = change_octet(self.ip_address, self.mask)
        network = ".".join(
            str(ip_octet & mask_octet)
            for (ip_octet, mask_octet) in zip(net_ip, netmask)
        )
        return network

    def get_broadcast(self):
        """This method calculate the broadcast address."""
        (broad_ip, broad_mask) = change_octet(self.ip_address, self.mask)
        broad_address = ".".join(
            str((ip_octet | ~mask_octet) & 0xff)
            for (ip_octet, mask_octet) in zip(broad_ip, broad_mask)
        )
        return broad_address

    def get_usable_hosts(self):
        """This method calculates the usable hosts."""
        new_mask = netmask_to_suffix(self.mask)
        new_mask = MAX_SUFFIX - new_mask
        if new_mask == 0:
            host = 1
        else:
            host = 2 ** new_mask -2
        return host

    def is_included(self, ip_address):
        """This method check if an ip_address isincludet in the network."""
        ip_check = Network(ip_address, self.mask)
        return ip_check.get_network() == self.get_network()
