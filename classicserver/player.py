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

DEFAULT_COORDINATES = [127.0, 35.0, 127.0]


class Player(object):
    player_id = None
    coordinates = DEFAULT_COORDINATES
    yaw = 0
    pitch = 0
    name = ""
    connection = None
    user_type = None

    def __init__(self, player_id, connection, coordinates, name, user_type):
        """
        Creates the Player object.
        :param player_id: The ID of the player to be created
        :type player_id: int
        :param connection: The connection of the player
        :type connection: Connection
        :param coordinates: The coordinates that the player will have
        :type coordinates: list
        :param name: The name of the player
        :type name: str
        :param user_type: The user type of the player.
        :type user_type: int
        """

        self.player_id = player_id
        self.connection = connection
        if coordinates:
            self.coordinates = coordinates
        self.name = name
        self.user_type = user_type
