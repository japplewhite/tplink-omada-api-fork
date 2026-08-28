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

    Field names confirmed 2026-08-27 against a live controller (firmware
    6.2.14.12) GET response for the site's default network - see
    get_networks()'s docstring for the verified request shape. Not every
    field the controller returns is modeled here yet (e.g. dhcpSettings is
    a nested object, igmp/mld snooping, arp detection, ACL/isolation flags)
    - add more as real use cases need them; raw_data has everything.
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
        """802.1Q VLAN ID (controller field name is just "vlan")."""
        return self._data.get("vlan")

    @property
    def purpose(self) -> str | None:
        """Network purpose (e.g. "interface" for a standard LAN network). String, not an enum code."""
        return self._data.get("purpose")

    @property
    def gateway_subnet(self) -> str | None:
        """Gateway IP / subnet, e.g. '192.168.20.1/24'."""
        return self._data.get("gatewaySubnet")

    @property
    def dhcp_enabled(self) -> bool | None:
        """Whether this network's own DHCP server is enabled (nested under dhcpSettings.enable)."""
        dhcp = self._data.get("dhcpSettings")
        return dhcp.get("enable") if dhcp else None

    @property
    def is_primary(self) -> bool | None:
        """Whether this is the site's primary/default network."""
        return self._data.get("primary")


class PortLabel(OmadaApiData):
    """A reusable, named label ("tag") that can be applied to switch ports.

    CORRECTED 2026-08-28: confirmed against a live controller to be
    GET/POST openapi/v1/{controllerId}/sites/{siteId}/switches/port-tag -
    an OpenAPI endpoint, not the legacy site-scoped .../tags endpoint used
    until now. That legacy endpoint happens to share the name "tags" and
    accepts the same {"name": ...} create body, but is an unrelated
    resource: ids created there are rejected by networks/confirm's
    deviceConfig.tagIds ("Some tag IDs do not exist."). Verified by
    capturing the switch port editor's "Port Labels" dropdown request and
    matching its returned tagId against the tagIds value actually stored
    on a live switch port.
    """

    @property
    def id(self) -> str:
        """Label ID - this is what deviceConfig.tagIds (create_network(),
        update_switch_port()) actually references, not the name. The
        controller's field name for this is "tagId", not "id"."""
        return self._data["tagId"]

    @property
    def name(self) -> str | None:
        """Label display name."""
        return self._data.get("name")

    @property
    def resource(self) -> int | None:
        """Controller-internal resource type code (observed value: 0). Meaning unconfirmed."""
        return self._data.get("resource")


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
