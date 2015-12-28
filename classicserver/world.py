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
import logging

import struct
import gzip

WORLD_WIDTH = 256
WORLD_HEIGHT = 64
WORLD_DEPTH = 256


class World(object):
    def __init__(self, blocks=None):
        self.blocks = blocks if blocks else self._generate()

    @staticmethod
    def _generate():
        logging.info("Generating the world...")
        blocks = bytearray(WORLD_WIDTH * WORLD_HEIGHT * WORLD_DEPTH)

        for x in range(WORLD_WIDTH):
            for y in range(WORLD_HEIGHT):
                for z in range(WORLD_DEPTH):
                    blocks[x + WORLD_DEPTH * (z + WORLD_WIDTH * y)] = 0 if y > 32 else (2 if y == 32 else 3)

        logging.info("World generation done.")
        return blocks

    def get_block(self, x, y, z):
        """
        Gets the block from the level.

        :param x: the X coordinate.
        :type x: int
        :param y: the Y coordinate.
        :type y: int
        :param z: the Z coordinate.
        :type z: int
        :return: The block ID at the given coordinates.
        :rtype: int
        """

        return self.blocks[x + WORLD_DEPTH * (z + WORLD_WIDTH * y)]

    def set_block(self, x, y, z, block):
        """
        Sets the block in the level.

        :param x: The X coordinate.
        :type x: int
        :param y: The Y coordinate.
        :type y: int
        :param z: The Z coordinate.
        :type z: int
        :param block: The block ID to be set
        :type block: int
        """

        self.blocks[x + WORLD_DEPTH * (z + WORLD_WIDTH * y)] = block

    def encode(self):
        """
        Encodes the level into the network format.

        :return: The network-encoded level.
        :rtype: buffer
        """
        return gzip.compress(struct.pack("!I", len(self.blocks)) + bytes(self.blocks))

    @staticmethod
    def from_save(data):
        """
        Creates the World object from network-encoded buffer.

        :param data: The encoded level.
        :type data: buffer
        :return: The World object from the data.
        :rtype: World
        """

        # TODO check the unpacked length against the preceding field
        return World(bytearray(gzip.decompress(data)[4:]))
