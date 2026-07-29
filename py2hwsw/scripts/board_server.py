#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

import time
import socket


DEBUG = False

HOST = "localhost"
PORT = 50007
VERSION = "V0.3"

# Dynamically tracks boards as clients grab them.
# board_name -> {"user": str, "grab_time": float, "duration": str}
boards = {}


def get_remaining_time(grab_time, duration):
    return int(duration) - (time.time() - grab_time)


def get_response(request):
    global boards

    if VERSION not in request:
        return "ERROR: Wrong version"

    # Clean up expired grabs
    now = time.time()
    expired = [
        b
        for b in list(boards.keys())
        if int(boards[b]["duration"]) - (now - boards[b]["grab_time"]) <= 0.1
    ]
    for b in expired:
        if DEBUG:
            print(f"Board {b} released due to timeout")
        del boards[b]

    parts = request.split()
    command = parts[0]

    if command == "query":
        if len(parts) >= 3:
            # query BOARD VERSION
            board = parts[1]
            if board in boards:
                b = boards[board]
                time_remaining = get_remaining_time(b["grab_time"], b["duration"])
                response = f"Board {board} is grabbed by user {b['user']} for {time_remaining} seconds"
            else:
                response = f"Board {board} is idle"
        else:
            # query VERSION -> report all tracked boards
            if not boards:
                response = "All boards are idle"
            else:
                board_strs = []
                for b, info in boards.items():
                    time_remaining = get_remaining_time(
                        info["grab_time"], info["duration"]
                    )
                    board_strs.append(
                        f"Board {b} grabbed by {info['user']} for {time_remaining}s"
                    )
                response = " | ".join(board_strs)

    elif command == "grab":
        # grab BOARD USER DURATION VERSION
        board = parts[1]
        user = parts[2]
        duration = parts[3]

        if board not in boards:
            boards[board] = {
                "user": user,
                "grab_time": time.time(),
                "duration": duration,
            }
            response = (
                f"Success: board {board} grabbed by {user} for {duration} seconds."
            )
        else:
            b = boards[board]
            time_remaining = get_remaining_time(b["grab_time"], b["duration"])
            response = f"Failure: board {board} grabbed by {b['user']} for {time_remaining} seconds."

    elif command == "release":
        # release BOARD USER VERSION
        board = parts[1]
        requesting_user = parts[2]

        if board not in boards:
            response = f"ERROR: board {board} already idle."
        elif requesting_user == boards[board]["user"]:
            del boards[board]
            response = f"Success: board {board} released."
        else:
            response = f"ERROR: cannot release board {board} in use by another user ({boards[board]['user']})"

    if DEBUG:
        print(f'Returning response: "{response}"')
    return response


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()

    while True:
        conn, addr = s.accept()
        request = conn.recv(1024).decode("utf-8")
        if DEBUG:
            print(f"Received request: {request}")
        response = get_response(request)
        if DEBUG:
            print(f"Got response: {response}")
        conn.sendall(response.encode("utf-8"))
