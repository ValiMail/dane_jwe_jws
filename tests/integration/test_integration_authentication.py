"""Test the DANE object."""
import os

from unittest.mock import MagicMock

import dane_discovery
from dane_discovery.dane import DANE
from dane_jwe_jws.authentication import Authentication

here_dir = os.path.dirname(os.path.abspath(__file__))
dyn_assets_dir = os.path.join(here_dir, "../fixtures/dynamic/")
identity_name = "abc123.air-quality-sensor._device.example.net"


class TestIntegrationAuthentication:
    """Integration tests for Authentication."""

    def get_dyn_asset(self, asset_name):
        """Return the contents of a file from the dynamic assets dir."""
        asset_path = os.path.join(dyn_assets_dir, asset_name)
        with open(asset_path, "rb") as asset:
            return asset.read()

    def test_integration_authentication_sign_and_verify(self):
        """Test signing and verification of JWS."""
        test_message = "hello world!!"
        prikey_name = "{}.key.pem".format(identity_name)
        prikey_path = os.path.join(dyn_assets_dir, prikey_name)
        pubkey_name = "{}.cert.pem".format(identity_name)
        signed = Authentication.sign(test_message, prikey_path, identity_name)
        premock = DANE.generate_tlsa_record(3, 0, 0,
                                            self.get_dyn_asset(pubkey_name))
        mocked = DANE.process_response(premock)
        mock_dane = dane_discovery.dane.DANE
        mock_dane.get_first_leaf_certificate = MagicMock(return_value=mocked)
        assert Authentication.verify(signed)
