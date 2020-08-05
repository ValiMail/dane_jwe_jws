"""Test the DANE object."""
import os

from unittest.mock import MagicMock

import dane_discovery
from dane_discovery.dane import DANE
from dane_jwe_jws.encryption import Encryption

here_dir = os.path.dirname(os.path.abspath(__file__))
dyn_assets_dir = os.path.join(here_dir, "../fixtures/dynamic/")
identity_name = "abc123.air-quality-sensor._device.example.net"


class TestIntegrationEncryption:
    """Integration tests for Encryption."""

    def get_dyn_asset(self, asset_name):
        """Return the contents of a file from the dynamic assets dir."""
        asset_path = os.path.join(dyn_assets_dir, asset_name)
        with open(asset_path, "rb") as asset:
            return asset.read()

    def test_integration_encryption_encrypt_and_decrypt(self):
        """Test encryption and decryption."""
        test_message = "hello world!!"
        prikey_name = "{}.key.pem".format(identity_name)
        prikey_path = os.path.join(dyn_assets_dir, prikey_name)
        pubkey_name = "{}.cert.pem".format(identity_name)
        encrypted = Encryption.encrypt(test_message, identity_name)
        premock = DANE.generate_tlsa_record(3, 0, 0,
                                            self.get_dyn_asset(pubkey_name))
        mocked = DANE.process_response(premock)
        mock_dane = dane_discovery.dane.DANE
        mock_dane.get_first_leaf_certificate = MagicMock(return_value=mocked)
        decrypted = Encryption.decrypt(encrypted, prikey_path)
        assert decrypted == test_message
