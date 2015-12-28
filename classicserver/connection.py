"""
    classic-server - A basic Minecraft Classic server.
    Copyright (C) 2015  SopaXorzTaker

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


class Connection(object):
    _address = None
    _sock = None
    _buffer = None

    def __init__(self, server, address, sock):
        """
        Creates a connection object.

        :param server: A server object, which should contain tne data_hook(connection, buf) method.
        :type server: server
        :param address: The address.
        :type address tuple
        :param sock: The socket that the connection uses.
        :type sock socket.socket
        """
        self._address = address
        self._sock = sock
        self.server = server

        self._sock.setblocking(0)

    def send(self, data):
        """
        Sends the data via the connection.
        :param data: The data to be sent
        :type data: buffer
        """
        self._sock.send(data)

    def flush(self):
        """
        Fetches the new data if available and calls the server hook if the receive was successful.
        """

        success = False
        buf = b""

        while True:
            try:
                data = self._sock.recv(1024)
                if not data:
                    break

                buf += data
                success = True
            except BlockingIOError:
                break

        if success:
            self.server.data_hook(self, buf)

    def get_address(self):
        """
        Gets the address of the connection.

        :return: The address.
        :rtype: tuple
        """
        return self._address

    def close(self):
        """
        Closes the connection socket.
        """

        self._sock.close()
