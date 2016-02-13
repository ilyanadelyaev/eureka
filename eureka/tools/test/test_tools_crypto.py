import pytest

import eureka.tools.crypto


class TestCrypto:
    def test__passphrase(self, password):
        hashed, salt = eureka.tools.crypto.Crypto.hash_passphrase(password)
        #
        assert len(hashed) == eureka.tools.crypto.Crypto.hashed_length
        assert len(salt) == eureka.tools.crypto.Crypto.salt_length
        #
        assert eureka.tools.crypto.Crypto.validate_passphrase(
            password, hashed, salt)

    def test__passphrase__empty(self):
        password = ''
        #
        hashed, salt = eureka.tools.crypto.Crypto.hash_passphrase(password)
        #
        assert len(hashed) == eureka.tools.crypto.Crypto.hashed_length
        assert len(salt) == eureka.tools.crypto.Crypto.salt_length
        #
        assert eureka.tools.crypto.Crypto.validate_passphrase(
            password, hashed, salt)

    def test__passphrase__short(self):
        password = 'qwer'
        #
        hashed, salt = eureka.tools.crypto.Crypto.hash_passphrase(password)
        #
        assert len(hashed) == eureka.tools.crypto.Crypto.hashed_length
        assert len(salt) == eureka.tools.crypto.Crypto.salt_length
        #
        assert eureka.tools.crypto.Crypto.validate_passphrase(
            password, hashed, salt)

    def test__passphrase__long(self, password):
        password *= 8
        #
        hashed, salt = eureka.tools.crypto.Crypto.hash_passphrase(password)
        #
        assert len(hashed) == eureka.tools.crypto.Crypto.hashed_length
        assert len(salt) == eureka.tools.crypto.Crypto.salt_length
        #
        assert eureka.tools.crypto.Crypto.validate_passphrase(
            password, hashed, salt)

    def test__generate_auth_token(self):
        assert len(eureka.tools.crypto.Crypto.generate_auth_token()) == \
            eureka.tools.crypto.Crypto.auth_token_length
