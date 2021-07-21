"""Test the DANE object."""
import os

from unittest.mock import MagicMock

from dane_discovery.dane import DANE
from dane_discovery.identity import Identity
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
    
    def tlsa_for_cert(self, id_name):
        """Return a PKIX-CD TLSA record for identity name."""
        file_name = "{}.cert.pem".format(id_name)
        file_contents = self.get_dyn_asset(file_name)
        tlsa = DANE.generate_tlsa_record(4, 0, 0, file_contents)
        return "name.example.com 123 IN TLSA {}".format(tlsa)

    def generate_identity(self, identity_name):
        """Return a PKIX-CD Identity object."""
        mocked = Identity
        mocked.set_dane_credentials = MagicMock(return_value=[])
        identity = Identity(identity_name)
        print("Identity: {}".format(identity_name))
        tlsa_dict = DANE.process_response(self.tlsa_for_cert(identity_name))
        print("TLSA: {}".format(tlsa_dict))
        identity.dane_credentials = [DANE.process_tlsa(record) for record
                                       in [tlsa_dict]]
        identity.dnssec = True
        identity.tls = True
        identity.tcp = True
        return identity

    def test_integration_authentication_sign_and_verify(self):
        """Test signing and verification of JWS."""
        test_message = "hello world!!"
        prikey_name = "{}.key.pem".format(identity_name)
        prikey_path = os.path.join(dyn_assets_dir, prikey_name)
        identity = self.generate_identity(identity_name)
        mocked = identity.get_first_entity_certificate()
        signed = Authentication.sign(test_message, prikey_path, identity_name)
        mock_id = Identity
        mock_id.get_first_entity_certificate = MagicMock(return_value=mocked)
        assert Authentication.verify(signed)
