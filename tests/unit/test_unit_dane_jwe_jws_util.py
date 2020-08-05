"""Test the DANE object."""
import os

import pytest

from dane_jwe_jws.util import Util

here_dir = os.path.dirname(os.path.abspath(__file__))
dyn_assets_dir = os.path.join(here_dir, "../fixtures/dynamic/")
identity_name = "abc123.air-quality-sensor._device.example.net"


class TestUnitUtil:
    """Unit tests for Util class."""

    def test_unit_util_get_name_from_dns_uri(self):
        """Ensure that we can parse a legit DNS URIs."""
        dnsname = "device.helloworld.example.com"
        valid_1 = "dns:{}?type=TLSA".format(dnsname)
        valid_2 = "dns://1.1.1.1/{}?type=TLSA".format(dnsname)
        assert Util.get_name_from_dns_uri(valid_1) == dnsname
        assert Util.get_name_from_dns_uri(valid_2) == dnsname

    def test_unit_util_get_name_from_dns_uri_raise(self):
        """Make sure a bad URI fails the right way."""
        with pytest.raises(ValueError):
            Util.get_name_from_dns_uri("https://1.1.1.1/hello.example.com")
            assert False

    def test_unit_util_get_name_from_dns_uri_raise_2(self):
        """Make sure a bad URI fails the right way."""
        with pytest.raises(ValueError):
            Util.get_name_from_dns_uri("dns:hello.example.com")
            assert False

    def test_unit_util_build_dns_uri(self):
        """Make sure we're building DNS URIs correctly."""
        dnsname = "device.helloworld.example.com"
        expected = "dns://{}?type=TLSA".format(dnsname)
        assert Util.build_dns_uri(dnsname) == expected
