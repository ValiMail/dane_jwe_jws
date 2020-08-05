Getting Started
===============

.. toctree::

Create a signed JWS object
--------------------------

.. code-block:: python

    from dane_jwe_jws.authentication import Authentication
    test_message = "hello world!!"
    prikey_path = "/path/to/private/key"
    identity_name = "dns.name.where.cert.lives.in.a.tlsa.record"
    signed = Authentication.sign(test_message, prikey_path, identity_name)
    print(signed)



Validate a signed JWS object
----------------------------

.. code-block:: python

    from dane_jwe_jws.authentication import Authentication
    signed = "signed_and_serialized_jws"
    validated = Authentication.verify(signed)
    print(validated)


Create an encrypted JWE object
------------------------------

.. code-block:: python

    from dane_jwe_jws.encryption import Encryption
    test_message = "hello world!!"
    identity_name = "dns.name.where.cert.lives.in.a.tlsa.record"
    encrypted = Encryption.encrypt(test_message, identity_name)
    print(encrypted)



Decrypt an encrypted JWE object
-------------------------------

.. code-block:: python

    from dane_jwe_jws.encryption import Encryption
    prikey_path = "/path/to/private/key"
    decrypted = Encryption.decrypt(encrypted, prikey_path)
    print(decrypted)
