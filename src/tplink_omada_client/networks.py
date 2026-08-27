"""Definitions for Omada network data objects."""

from .definitions import OmadaApiData


class DhcpReservation(OmadaApiData):
    """DHCP reservation on an Omada controller."""

    @property
    def id(self) -> str:
        """Reservation ID."""
        return self._data["id"]

    @property
    def mac(self) -> str:
        """Device MAC address."""
        return self._data["mac"]

    @property
    def ip(self) -> str:
        """Reserved IP address."""
        return self._data["ip"]

    @property
    def description(self) -> str | None:
        """Description / name for the reservation."""
        return self._data.get("description")

    @property
    def status(self) -> bool | None:
        """Whether the reservation is active."""
        return self._data.get("status")

    @property
    def net_id(self) -> str | None:
        """ID of the network this reservation belongs to."""
        return self._data.get("netId")

    @property
    def net_name(self) -> str | None:
        """Name of the network this reservation belongs to."""
        return self._data.get("netName")

    @property
    def client_name(self) -> str | None:
        """Name of the client associated with this reservation."""
        return self._data.get("clientName")

    @property
    def export_to_ip_mac_binding(self) -> bool | None:
        """Whether to export this reservation to IP-MAC binding."""
        return self._data.get("exportToIpMacBinding")


class LanNetwork(OmadaApiData):
    """LAN network (VLAN) configuration.

    NOTE: field names below are a best-effort guess based on this codebase's
    conventions for adjacent objects (DhcpReservation's netId/netName, the
    Omada Controller UI's "Wired Networks > LAN" terminology) and have NOT
    been confirmed against a live controller response yet. Verify raw_data
    against a real GET before trusting anything beyond raw_data itself.
    """

    @property
    def id(self) -> str:
        """Network ID."""
        return self._data["id"]

    @property
    def name(self) -> str | None:
        """Network name."""
        return self._data.get("name")

    @property
    def vlan_id(self) -> int | None:
        """802.1Q VLAN ID, if tagged."""
        return self._data.get("vlanId")

    @property
    def purpose(self) -> int | None:
        """Network purpose/type code (e.g. LAN vs. other roles). Raw controller value - not yet mapped to an enum."""
        return self._data.get("purpose")

    @property
    def gateway_subnet(self) -> str | None:
        """Gateway IP / subnet, if present (e.g. '192.168.20.1/24')."""
        return self._data.get("gatewaySubnet") or self._data.get("subnet")


class LanProfile(OmadaApiData):
    """LAN port profile (VLAN profile for switch ports)."""

    # Properties defined during vlan-listing implementation


class GatewayAcl(OmadaApiData):
    """Gateway ACL rule."""

    # Properties defined during acl-listing implementation


class SwitchAcl(OmadaApiData):
    """Switch ACL rule."""

    # Properties defined during acl-listing implementation


class EapAcl(OmadaApiData):
    """EAP (access point) ACL rule."""

    # Properties defined during acl-listing implementation


class GroupProfile(OmadaApiData):
    """Group profile (IP group, MAC group, IP-Port group, etc.)."""

    # Properties defined during ip-groups implementation


class IpMacBinding(OmadaApiData):
    """IP-MAC binding entry."""

    # Properties defined during ip-mac-bindings implementation
