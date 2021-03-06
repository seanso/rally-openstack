# Copyright 2018 Red Hat, Inc. <http://www.redhat.com>
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from rally.task import atomic
from rally.task import service


class BarbicanService(service.Service):

    @atomic.action_timer("barbican.list_secrets")
    def list_secrets(self):
        """List Secret"""
        return self._clients.barbican().secrets.list()

    @atomic.action_timer("barbican.create_secret")
    def create_secret(self):
        """Create Secret"""
        secret_name = self.generate_random_name()
        val = self._clients.barbican().secrets.create(name=secret_name,
                                                      payload="rally_data")
        val.store()
        return val

    @atomic.action_timer("barbican.get_secret")
    def get_secret(self, secret_ref):
        """Get the secret.

        :param secret_name: The name of the secret.
        """
        return self._clients.barbican().secrets.get(secret_ref)

    @atomic.action_timer("barbican.delete_secret")
    def delete_secret(self, secret_name):
        """Delete the secret

        :param secret_name: The name of the secret to delete
        """
        return self._clients.barbican().secrets.delete(secret_name)

    @atomic.action_timer("barbican.list_container")
    def list_container(self):
        """List containers"""
        return self._clients.barbican().containers.list()

    @atomic.action_timer("barbican.container_delete")
    def container_delete(self, container_href):
        """Delete the container

        :param container_href: the container reference
        """
        return self._clients.barbican().containers.delete(container_href)

    @atomic.action_timer("barbican.container_create")
    def container_create(self, name=None, secrets=None):
        """Create a generic container

        :param name: the name of the container
        :param secrets: secrets to populate when creating a container
        """
        name = name or self.generate_random_name()
        val = self._clients.barbican().containers.create(
            name=name, secrets=secrets)
        val.store()
        return val

    @atomic.action_timer("barbican.create_rsa_container")
    def create_rsa_container(self, name=None, public_key=None,
                             private_key=None, private_key_passphrase=None):
        """Create a RSA container

        :param name: a friendly name for the container
        :param public_key: Secret object containing a Public Key
        :param private_key: Secret object containing a Private Key
        :param private_key_passphrase: Secret object containing
            a passphrase
        :returns: RSAContainer
        """
        name = name or self.generate_random_name()
        val = self._clients.barbican().containers.create_rsa(
            name=name, public_key=public_key, private_key=private_key,
            private_key_passphrase=private_key_passphrase)
        val.store()
        return val

    @atomic.action_timer("barbican.create_certificate_container")
    def create_certificate_container(self, name=None, certificate=None,
                                     intermediates=None, private_key=None,
                                     private_key_passphrase=None):
        """Create a certificate container

        :param name: A friendly name for the CertificateContainer
        :param certificate: Secret object containing a Certificate
        :param intermediates: Secret object containing
            Intermediate Certs
        :param private_key: Secret object containing a Private Key
        :param private_key_passphrase: Secret object containing a passphrase
        :returns: CertificateContainer
        """
        name = name or self.generate_random_name()
        val = self._clients.barbican().containers.create_certificate(
            name=name, certificate=certificate, intermediates=intermediates,
            private_key=private_key, private_key_passphrase=None)
        val.store()
        return val
