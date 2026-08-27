"""Tests for network data models."""

from unittest.mock import MagicMock

import pytest

from tplink_omada_client.networks import DhcpReservation, LanNetwork
from tplink_omada_client.omadasiteclient import OmadaSiteClient


def test_dhcp_reservation():
    """Smoke test: DhcpReservation reads from raw data dict."""
    data = {
        "id": "res-1",
        "mac": "AA-BB-CC-11-22-33",
        "ip": "192.168.1.100",
        "description": "web-server",
        "status": True,
        "netId": "net-1",
        "netName": "Main",
    }
    r = DhcpReservation(data)
    assert r.id == "res-1"
    assert r.mac == "AA-BB-CC-11-22-33"
    assert r.ip == "192.168.1.100"
    assert r.description == "web-server"
    assert r.status is True
    assert r.net_id == "net-1"
    assert r.net_name == "Main"
    assert r.raw_data == data


def test_dhcp_reservation_optional_fields_default_to_none():
    """Optional fields return None when not present in the API response."""
    r = DhcpReservation({"id": "res-2", "mac": "11-22-33-44-55-66", "ip": "10.0.0.10"})
    assert r.description is None
    assert r.status is None
    assert r.net_id is None
    assert r.net_name is None
    assert r.client_name is None
    assert r.export_to_ip_mac_binding is None


def test_dhcp_reservation_optional_fields():
    """All optional fields populate correctly."""
    data = {
        "id": "res-3",
        "mac": "AA-BB-CC-DD-EE-FF",
        "ip": "10.0.0.50",
        "description": "printer",
        "status": False,
        "netId": "net-2",
        "netName": "Guest",
        "clientName": "HPLaserJet",
        "exportToIpMacBinding": True,
    }
    r = DhcpReservation(data)
    assert r.description == "printer"
    assert r.status is False
    assert r.net_id == "net-2"
    assert r.net_name == "Guest"
    assert r.client_name == "HPLaserJet"
    assert r.export_to_ip_mac_binding is True


def test_dhcp_reservation_repr():
    """repr() includes property names and values, not raw_data."""
    r = DhcpReservation({"id": "r1", "mac": "AA-BB-CC-11-22-33", "ip": "10.0.0.1", "description": "test"})
    rep = repr(r)
    assert "DhcpReservation" in rep
    assert "id=r1" in rep
    assert "mac=AA-BB-CC-11-22-33" in rep
    assert "ip=10.0.0.1" in rep
    assert "description=test" in rep
    assert "_data" not in rep


def test_lan_network_fields():
    """LanNetwork reads real controller field names (verified against a live
    controller, firmware 6.2.14.12: "vlan" not "vlanId", "primary" for the
    default network, dhcpSettings.enable nested for DHCP status)."""
    data = {
        "id": "net-1",
        "name": "Default",
        "purpose": "interface",
        "vlan": 1,
        "gatewaySubnet": "192.168.0.1/24",
        "dhcpSettings": {"enable": True},
        "primary": True,
    }
    n = LanNetwork(data)
    assert n.id == "net-1"
    assert n.name == "Default"
    assert n.purpose == "interface"
    assert n.vlan_id == 1
    assert n.gateway_subnet == "192.168.0.1/24"
    assert n.dhcp_enabled is True
    assert n.is_primary is True
    assert n.raw_data == data


def test_lan_network_optional_fields_default_to_none():
    n = LanNetwork({"id": "net-2"})
    assert n.name is None
    assert n.purpose is None
    assert n.vlan_id is None
    assert n.gateway_subnet is None
    assert n.dhcp_enabled is None
    assert n.is_primary is None


@pytest.mark.asyncio
async def test_get_networks():
    """get_networks() paginates the legacy setting/lan/networks endpoint and
    returns LanNetwork objects - verified against a live controller."""
    api = MagicMock()
    api.format_url = MagicMock(side_effect=lambda path, site=None: f"/api/v2/sites/{site}/{path}")

    async def _fake_iterate_pages(url, params=None):
        assert url == "/api/v2/sites/site-1/setting/lan/networks"
        for item in [
            {"id": "net-1", "name": "Default", "purpose": "interface", "vlan": 1},
            {"id": "net-2", "name": "Surveillance", "purpose": "interface", "vlan": 30},
        ]:
            yield item

    api.iterate_pages = _fake_iterate_pages
    site_client = OmadaSiteClient("site-1", api)

    result = await site_client.get_networks()

    assert len(result) == 2
    assert result[0].name == "Default"
    assert result[0].vlan_id == 1
    assert result[1].name == "Surveillance"
    assert result[1].vlan_id == 30
