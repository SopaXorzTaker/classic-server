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

from classicserver.packet.packet import MessagePacket, PositionAndOrientationPacket

HELP_TEXT = """
&aClassic-Server Help
&4 Commands:
&e /help &b - this help
&e /tp &2<x> <y> <z> &b - teleport to coordinates
&e /tp &2<playerName> &b - teleport to player
&e /kick &2<playerName> [reason] &b - kick a player
"""


class CommandHandler(object):
    @staticmethod
    def handle_command(server, player, command, args):
        """
        Handles the in-game commands.
        :param server: The parent server object.
        :type server: ClassicServer
        :param player: The player who issued the command.
        :type player: Player
        :param command: The command issued, without the leading slash.
        :type command: str
        :param args: The arguments for the command
        :type args: list
        """
        if command == "tp":
            if len(args) == 3:
                try:
                    player.coordinates = [float(args[0]), float(args[1]), float(args[2])]
                    player.connection.send(PositionAndOrientationPacket.make({"player_id": -1,
                                                                              "frac_x": int(player.coordinates[0] * 32),
                                                                              "frac_y": int(player.coordinates[1] * 32),
                                                                              "frac_z": int(player.coordinates[2] * 32),
                                                                              "yaw": player.yaw,
                                                                              "pitch": player.pitch
                                                                              }))
                    server.broadcast(PositionAndOrientationPacket.make({"player_id": player.player_id,
                                                                        "frac_x": int(player.coordinates[0] * 32),
                                                                        "frac_y": int(player.coordinates[1] * 32),
                                                                        "frac_z": int(player.coordinates[2] * 32),
                                                                        "yaw": player.yaw,
                                                                        "pitch": player.pitch
                                                                        }))
                except ValueError:
                    player.connection.send(MessagePacket.make({"player_id": 0, "message": "&4Invalid coordinates,"}))
                    player.connection.send(MessagePacket.make({"player_id": 0,
                                                               "message": "&4please use /tp <x> <y> <z> or"}))
                    player.connection.send(MessagePacket.make({"player_id": 0, "message": "&4/tp <playerName>"}))
            elif len(args) == 1:
                for target_player in server.get_players().values():
                    if target_player.name == args[0]:
                        player.coordinates = target_player.coordinates
                        player.connection.send(PositionAndOrientationPacket.make({"player_id": -1,
                          "frac_x": int(player.coordinates[0] * 32),
                          "frac_y": int(player.coordinates[1] * 32),
                          "frac_z": int(player.coordinates[2] * 32),
                          "yaw": player.yaw,
                          "pitch": player.pitch
                        }))
                        server.broadcast(PositionAndOrientationPacket.make({"player_id": player.player_id,
                            "frac_x": int(player.coordinates[0] * 32),
                            "frac_y": int(player.coordinates[1] * 32),
                            "frac_z": int(player.coordinates[2] * 32),
                            "yaw": player.yaw,
                            "pitch": player.pitch
                        }))
                        break
                else:
                    player.connection.send(MessagePacket.make({"player_id": 0,
                                                               "message": "&4Target player not found."}))
            else:
                player.connection.send(MessagePacket.make({
                    "player_id": 0,
                    "message": "&4Invalid arguments, please use /tp <x> <y> <z> or"
                }))
                player.connection.send(MessagePacket.make({"player_id": 0, "message": "&4/tp <playerName>"}))
        elif command == "kick":
            if server.is_op(player.name):
                if len(args) >= 1:
                    player_name = args[0]
                    reason = " ".join(args[1:]) if len(args) > 1 else "No reason specified"
                    for target_player in server.get_players().values():
                        if target_player.name == player_name:
                            server.kick_player(target_player.player_id, reason)
                            break
                    else:
                        player.connection.send(MessagePacket.make({"player_id": 0,
                                                                  "message": "&4Couldn't find the player specified."}))
                else:
                    player.connection.send(MessagePacket.make({"player_id": 0,
                                                               "message": "&4Usage: /kick <playerName> [reason]"}))
            else:
                player.connection.send(MessagePacket.make({"player_id": 0,
                    "message": "&4You need to be an op to do that!"}))
        elif command == "help":
            for line in HELP_TEXT.split("\n"):
                line = line.strip()
                player.connection.send(MessagePacket.make({"player_id": 0,
                                                           "message": "%s" % line}))
