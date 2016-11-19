import datetime
import ftputil
import hashlib
from io import BytesIO
import os
import random
import string

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography import utils
from ftplib import FTP


def random_serial_number():
    """taken from future version of Cryptography, current stable version
    does not include it (currnt version is 1.5.3, re-visit this in 1.6"""
    return utils.int_from_bytes(os.urandom(20), "big") >> 1

def generate_password(pass_len=8, uppercase=True, lowercase=True, digits=True,
                      special_chars=True):
    allowed = ''
    if lowercase:
        allowed = allowed + string.ascii_lowercase
    if uppercase:
        allowed = allowed + string.ascii_uppercase
    if digits:
        allowed = allowed + string.digits
    if special_chars:
        allowed = allowed + string.punctuation

    password = ''.join(random.SystemRandom().choice(allowed)
                       for _ in range(pass_len))
    md5 = hashlib.md5()
    md5.update(password.encode())

    return password, md5.hexdigest()



def create_public_key(size=2048, public_exponent=65537):
    """
    Pure python creation of SSL certificates

    Taken from https://cryptography.io/en/stable/x509/tutorial/
    """
    key = rsa.generate_private_key(
        public_exponent=public_exponent,
        key_size=size,
        backend=default_backend()
    )

    return key


def create_certificate(key, country, state_province, locality, orga, name):
    # Various details about who we are. For a self-signed certificate the
    # subject and issuer are always the same.
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, country),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state_province),
        x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, orga),
        x509.NameAttribute(NameOID.COMMON_NAME, name),
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).serial_number(
        random_serial_number()
    ).not_valid_after(
        # Our certificate will be valid for 10 days
        datetime.datetime.utcnow() + datetime.timedelta(days=10)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(name)]),
        critical=False,
        # Sign our certificate with our private key
    ).sign(key, hashes.SHA256(), default_backend())

    return cert


def write_key(key, passwd=None, filename="key.pem"):
    if passwd:
        enc_algo = serialization.BestAvailableEncryption(passwd.encode())
    else:
        enc_algo = serialization.NoEncryption()

    # Write our key to disk for safe keeping
    with open(filename, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=enc_algo,))


def write_cert(cert, filename):

    # Write our certificate out to disk.
    with open(filename, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))


def create_config_bundle(site, name, secret=None):
    """create all the files needed for the configuration"""
    key = create_public_key()
    cert = create_certificate(key, u"DE", u"Bayern", u"Munich",
                              u"The Mobility House", u"tmh.tech")
    write_key(key, passwd=secret, filename="/".join((os.getcwd(), "configuration", site, name + ".pem")))
    write_cert(cert, "/".join(("configuration", site, name + ".crt")))

    secrets = "/".join(("configuration", site, "secrets_{}.txt".format(name)))

    with open(secrets, "w") as secrets:
        password, hash = generate_password()
        secrets.write("password: {} hash: {}".format(password, hash))


def initiate_logging(host, user, passwd, port=21):
    with FTP() as f:
        f.connect(host, port=port)
        f.login(user, passwd)
        f.cwd("/")
        f.mkd("BCM-LOGFILES")
        f.quit()
