#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

import sys
import socket
import os
import time
import subprocess
import signal
import argparse
import importlib.util
from typing import List

if importlib.util.find_spec("iob_colors") is not None:
    import iob_colors
else:
    print(
        "Module `iob_colors.py` not found. Please set the `PYTHONPATH` environment variable with the location of this module."
    )
    print("For example: `export PYTHONPATH=<Path to iob-lib>/scripts`")
    sys.exit(1)

DEBUG = False

HOST = "localhost"
PORT = 50007
VERSION = "V0.3"

USER = os.environ["USER"]
DURATION = "15"

proc_list: List = []
console_command = None
fpga_prog_command = None
simulator_run_command = None

CPREFIX = "[board_client]: "
BOARD = None


def perror():
    print(
        f"""
Usage: ./{sys.argv[0]} [grab [duration] | release] -b BOARD [-c console_cmd] [-p prog_cmd | -s sim_cmd]
    -b, --board BOARD          Board name (required for 'grab' and 'release').
    -c, --console CMD          Command to launch the console.
    -p, --program CMD          Command to program the FPGA.
    -s, --simulate CMD         Command to run the simulator.
    If -p is given then -c is required. If -s is given then -c is optional.
    On fpga program (-p) mode, it contacts the server to grab the board, runs the program
        command, then launches the console.
    On simulator run (-s) mode, grab duration is the simulation timeout; server is not used.
"""
    )
    sys.exit(1)


def form_request(command):
    request = ""
    if command == "grab":
        request += f"{command} {BOARD} {USER} {DURATION} {VERSION}"
    elif command == "release":
        request += f"{command} {BOARD} {USER} {VERSION}"
    elif command == "query":
        request += f"{command} {VERSION}"
    return request


def send_request(request):
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)

        try:
            s.connect((HOST, PORT))
        except Exception:
            print(
                f"{CPREFIX}{iob_colors.WARNING}Could not connect to board server{iob_colors.ENDC}"
            )
            return

        s.sendall(request.encode("utf-8"))

        response = s.recv(1024).decode()
        s.close()
        print(CPREFIX + "Server response: " + response)

        if "ERROR" in response:
            sys.exit(1)

        if "grab" in request and "Failure" in response:
            time_remaining = float(response.split(" ")[-2])
            print(
                f"{CPREFIX}{iob_colors.WARNING}Trying again in",
                time_remaining,
                f"seconds{iob_colors.ENDC}",
            )
            time.sleep(time_remaining)
        else:
            break


def release_board(signal=None, frame=None):
    request = form_request("release")
    send_request(request)


def exit_program(exit_code):
    if fpga_prog_command:
        release_board()
    sys.exit(exit_code)


def kill_processes(sig=None, frame=None):
    for proc in proc_list:
        if proc.poll() is None:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            try:
                proc.wait(2)
            except subprocess.TimeoutExpired:
                print(
                    "Timeout waiting for process to terminate gracefully! Forcing process kill..."
                )
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    if sig is None:
        exit_program(1)
    else:
        exit_program(0)


def proc_wait(proc, timeout):
    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        print(
            f"{CPREFIX}{iob_colors.FAIL}Board grab duration expired!{iob_colors.ENDC}"
        )
        kill_processes()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="board_client.py",
        description="Client to grab FPGA board and manage simulation and console processes.",
        epilog="If -p is given then -c is required. If -s is given then -c is optional.",
    )

    parser.add_argument(
        "command",
        nargs="?",
        default="query",
        help='Command to send to server. Can be "grab", "release" or "query".',
    )

    parser.add_argument(
        "duration",
        nargs="?",
        default=DURATION,
        help="Duration in seconds to grab the board.",
    )

    parser.add_argument(
        "-c", "--console", default=None, help="Command to launch the console."
    )

    parser.add_argument(
        "-p",
        "--program",
        default=None,
        help="Command to program the FPGA. Cannot be used with `-s` argument. Requires `-c` argument aswell.",
    )

    parser.add_argument(
        "-s",
        "--simulate",
        default=None,
        help="Command to run the simulator. Cannot be used with `-p` argument.",
    )

    parser.add_argument(
        "-b",
        "--board",
        default=None,
        help="Board name to grab/release/query (required for grab and release).",
    )

    args = parser.parse_args()
    command = args.command
    DURATION = args.duration
    console_command = args.console
    fpga_prog_command = args.program
    simulator_run_command = args.simulate
    BOARD = args.board

    if command == "grab" and not args.board and fpga_prog_command:
        print(
            f"{iob_colors.FAIL}Error: argument `-b`/`--board` is required for FPGA grab.{iob_colors.ENDC}"
        )
        sys.exit(1)
    if command == "release" and not args.board:
        print(
            f"{iob_colors.FAIL}Error: argument `-b`/`--board` is required for 'release' command.{iob_colors.ENDC}"
        )
        sys.exit(1)

    assert command != "grab" or bool(fpga_prog_command) != bool(
        simulator_run_command
    ), f"{iob_colors.FAIL}Either `-p` or `-s` must be present with 'grab' command. (Cannot be both){iob_colors.ENDC}"

    assert (
        not fpga_prog_command or console_command
    ), f"{iob_colors.FAIL}Argument `-c` must be present with `-p`.{iob_colors.ENDC}"

    request = form_request(command)
    if DEBUG:
        print(
            f'{CPREFIX}{iob_colors.OKBLUE}DEBUG: Request is "{request}"{iob_colors.ENDC}'
        )

    if command != "grab" or fpga_prog_command:
        send_request(request)

    if command == "grab":
        signal.signal(signal.SIGINT, kill_processes)
        signal.signal(signal.SIGTERM, kill_processes)
    else:
        sys.exit(0)

    if simulator_run_command:
        print(f"{CPREFIX}{iob_colors.INFO}Running simulator{iob_colors.ENDC}")
        sim_proc = subprocess.Popen(
            simulator_run_command,
            stdout=sys.stdout,
            stderr=sys.stderr,
            shell=True,
            start_new_session=True,
        )
        proc_list.append(sim_proc)

    start_time = time.time()

    if fpga_prog_command:
        print(f"{CPREFIX}{iob_colors.INFO}Programming FPGA{iob_colors.ENDC}")
        fpga_prog_proc = subprocess.Popen(
            fpga_prog_command,
            stdout=sys.stdout,
            stderr=sys.stderr,
            shell=True,
            start_new_session=True,
        )
        proc_list.append(fpga_prog_proc)
        proc_wait(fpga_prog_proc, int(DURATION))
        if fpga_prog_proc.returncode != 0:
            print(
                f"{CPREFIX}{iob_colors.FAIL}FPGA programmer exited with non-zero code.{iob_colors.ENDC}"
            )
            kill_processes()

    remaining_duration = int(DURATION) - (time.time() - start_time)

    if console_command:
        print(f"{CPREFIX}{iob_colors.INFO}Running console{iob_colors.ENDC}")
        console_proc = subprocess.Popen(
            console_command,
            stdout=sys.stdout,
            stderr=sys.stderr,
            shell=True,
            start_new_session=True,
        )
        proc_list.append(console_proc)
        proc_wait(console_proc, remaining_duration)
        if console_proc.returncode != 0:
            print(
                f"{CPREFIX}{iob_colors.FAIL}Console exited with non-zero code.{iob_colors.ENDC}"
            )
            kill_processes()

        remaining_duration = int(DURATION) - (time.time() - start_time)

    if simulator_run_command:
        print(
            f"{CPREFIX}{iob_colors.INFO}Waiting for simulator to finish{iob_colors.ENDC}"
        )
        proc_wait(sim_proc, remaining_duration)
        if sim_proc.returncode != 0:
            print(
                f"{CPREFIX}{iob_colors.FAIL}Simulator exited with non-zero code.{iob_colors.ENDC}"
            )
            kill_processes()

    exit_program(0)
