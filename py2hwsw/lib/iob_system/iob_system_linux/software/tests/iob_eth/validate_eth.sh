#!/bin/sh

# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

# IOb-ETH ethoc Driver Automated Validation Script
#
# This script orchestrates the full validation of the IOb-Eth core
# against the Linux ethoc driver. It runs on the host machine and
# coordinates the SoC-side test and host-side companion script.
#
# Usage:
#   sh validate_eth.sh [options]
#
# Options:
#   -s <soc_ip>      SoC IP address (default: 192.168.1.10)
#   -c <host_ip>     Host IP address (default: auto-detect)
#   -i <interface>   Host Ethernet interface (default: auto-detect)
#   -S <ssh_user>    SSH user for SoC (enables remote execution)
#   -p <password>    SSH password for SoC (requires sshpass on host)
#   -v               Verbose output
#   -h               Show this help
#
# If -S is provided, the script will:
#   1. Build the test binary
#   2. Copy it to the SoC via scp
#   3. Run the test remotely via ssh
#   4. Run the host companion script locally
#   5. Collect and display results
#
# If -S is not provided, the script assumes:
#   1. The test binary is already on the SoC
#   2. You will run iob_eth_test manually on the SoC
#   3. This script only starts the host companion

SOC_IP="192.168.1.10"
HOST_IP=""
INTERFACE=""
SSH_USER=""
SSH_PASS=""
SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=120 -o ServerAliveInterval=15 -o ServerAliveCountMax=10"
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
HOST_SCRIPT="$SCRIPT_DIR/iob_eth_host.py"
TEST_BIN="$SCRIPT_DIR/iob_eth_test"
PORT=9000
HOST_PID=""
VERBOSE=""

usage() {
    sed -n '3,/^$/s/^#//p' "$0"
    exit 0
}

# Parse arguments
while [ $# -gt 0 ]; do
    case "$1" in
        -s) SOC_IP="$2"; shift 2 ;;
        -c) HOST_IP="$2"; shift 2 ;;
        -i) INTERFACE="$2"; shift 2 ;;
        -S) SSH_USER="$2"; shift 2 ;;
        -p) SSH_PASS="$2"; shift 2 ;;
        -v) VERBOSE="-v"; shift ;;
        -h) usage ;;
        *) echo "Unknown option: $1"; usage ;;
    esac
done

# Setup sshpass prefix if password was provided
SSH_PASS_CMD=""
if [ -n "$SSH_PASS" ]; then
    if command -v sshpass >/dev/null 2>&1; then
        SSH_PASS_CMD="sshpass -p $SSH_PASS"
        echo "Using sshpass for SSH authentication"
    else
        echo "ERROR: sshpass is required when using -p <password> but is not installed."
        echo "       Install it with: sudo apt install sshpass"
        echo "       Or use SSH keys instead of a password."
        exit 1
    fi
fi

# Auto-detect host interface if not specified
if [ -z "$INTERFACE" ]; then
    # Find the non-loopback interface with a default route
    INTERFACE=$(ip route show default | awk '{print $5}' | head -n1)
    if [ -z "$INTERFACE" ]; then
        # Fallback: first non-lo interface
        INTERFACE=$(ls /sys/class/net/ | grep -v lo | head -n1)
    fi
    if [ -z "$INTERFACE" ]; then
        echo "ERROR: Could not auto-detect host interface"
        exit 1
    fi
fi

# Auto-detect host IP if not specified
if [ -z "$HOST_IP" ]; then
    HOST_IP=$(ip -4 addr show dev "$INTERFACE" | awk '/inet /{print $2}' | cut -d/ -f1 | head -n1)
    if [ -z "$HOST_IP" ]; then
        echo "ERROR: Could not auto-detect host IP for $INTERFACE"
        exit 1
    fi
fi

echo "=== IOb-ETH ethoc Driver Automated Validation ==="
echo ""
echo "Host interface: $INTERFACE"
echo "Host IP:        $HOST_IP"
echo "SoC IP:         $SOC_IP"
echo ""

# Function to cleanup on exit
cleanup() {
    if [ -n "$HOST_PID" ]; then
        echo ""
        echo "Stopping host companion script (PID=$HOST_PID)..."
        kill "$HOST_PID" 2>/dev/null
        wait "$HOST_PID" 2>/dev/null
    fi
}
trap cleanup EXIT

# Step 1: Build if source exists and binary is older
if [ -f "$SCRIPT_DIR/iob_eth_test.c" ] && [ ! -f "$TEST_BIN" ]; then
    echo "Building test binary..."
    make -C "$SCRIPT_DIR" || {
        echo "ERROR: Build failed"
        exit 1
    }
    echo ""
fi

if [ ! -f "$TEST_BIN" ] && [ -z "$SSH_USER" ]; then
    echo "WARNING: Test binary not found at $TEST_BIN"
    echo "         Build with 'make' or run test manually on SoC."
    echo ""
fi

# Step 2: Check ARP entry for SoC on host
echo "Checking ARP entry for SoC..."
SOC_MAC=$(arp -n "$SOC_IP" 2>/dev/null | awk '/ether/{print $3}')
if [ -n "$SOC_MAC" ]; then
    echo "  ARP: $SOC_IP -> $SOC_MAC"
else
    echo "  Note: SoC ARP entry will be learned from first packet"
fi
echo ""

# Step 3: Copy binary and run on SoC (if SSH configured)
if [ -n "$SSH_USER" ]; then
    echo "Copying test binary to SoC..."
    $SSH_PASS_CMD scp $SSH_OPTS "$TEST_BIN" "${SSH_USER}@${SOC_IP}:/tmp/iob_eth_test" || {
        echo "ERROR: SCP failed"
        exit 1
    }

    echo "Making binary executable on SoC..."
    $SSH_PASS_CMD ssh $SSH_OPTS "${SSH_USER}@${SOC_IP}" "chmod +x /tmp/iob_eth_test" || {
        echo "ERROR: chmod failed"
        exit 1
    }
    echo ""
fi

# Step 4: Start host companion script in background
echo "Starting host companion script on $INTERFACE..."
python3 "$HOST_SCRIPT" "$INTERFACE" --soc-ip "$SOC_IP" --port "$PORT" &
HOST_PID=$!
echo "  Host PID: $HOST_PID"

# Give host script time to start
sleep 2

# Verify host script is running
if ! kill -0 "$HOST_PID" 2>/dev/null; then
    echo "ERROR: Host companion script failed to start"
    exit 1
fi
echo "  Host script is running"
echo ""

# Step 5: Run test on SoC
echo "Running test on SoC..."
echo "-------------------------------------------"

if [ -n "$SSH_USER" ]; then
    # Run remotely
    $SSH_PASS_CMD ssh $SSH_OPTS "${SSH_USER}@${SOC_IP}" \
        "/tmp/iob_eth_test -s $SOC_IP -c $HOST_IP -v" 2>&1
    TEST_EXIT=$?
else
    # Run locally (assume we're on the SoC or have access)
    if [ -x "$TEST_BIN" ]; then
        "$TEST_BIN" -s "$SOC_IP" -c "$HOST_IP" $VERBOSE 2>&1
        TEST_EXIT=$?
    else
        echo "Test binary not found. Please run manually on the SoC:"
        echo "  $TEST_BIN -s $SOC_IP -c $HOST_IP $VERBOSE"
        echo ""
        echo "Press Enter when the test is complete, or Ctrl+C to abort."
        read -r
        TEST_EXIT=0
    fi
fi

echo "-------------------------------------------"
echo ""

# Step 6: Check kernel error counters
echo "Checking kernel error counters..."

if [ -n "$SSH_USER" ]; then
    $SSH_PASS_CMD ssh $SSH_OPTS "${SSH_USER}@${SOC_IP}" "
        SOC_IF=\$(ls /sys/class/net/ | grep -v lo | head -n1)
        echo '--- /proc/net/dev ---'
        head -2 /proc/net/dev 2>/dev/null || true
        grep \"\$SOC_IF\" /proc/net/dev 2>/dev/null || echo '(interface not found in /proc/net/dev)'

        echo ''
        echo '--- Error counters ---'
        RX_ERRS=\$(grep \"\$SOC_IF\" /proc/net/dev 2>/dev/null | awk '{print \$4}')
        TX_ERRS=\$(grep \"\$SOC_IF\" /proc/net/dev 2>/dev/null | awk '{print \$12}')
        echo \"rx_errors: \$RX_ERRS\"
        echo \"tx_errors: \$TX_ERRS\"
    " 2>&1
else
    echo "--- /proc/net/dev ---"
    head -1 /proc/net/dev 2>/dev/null || true
    grep "$INTERFACE" /proc/net/dev 2>/dev/null || echo "(interface not found in /proc/net/dev)"

    echo ""
    echo "--- Error counters ---"
    RX_ERRS=$(grep "$INTERFACE" /proc/net/dev 2>/dev/null | awk '{print $4}')
    TX_ERRS=$(grep "$INTERFACE" /proc/net/dev 2>/dev/null | awk '{print $12}')
    echo "rx_errors: $RX_ERRS"
    echo "tx_errors: $TX_ERRS"
fi

echo ""

# Step 7: Check interrupts
echo "Checking interrupt activity..."
if [ -n "$SSH_USER" ]; then
    $SSH_PASS_CMD ssh $SSH_OPTS "${SSH_USER}@${SOC_IP}" "
        SOC_IF=\$(ls /sys/class/net/ | grep -v lo | head -n1)
        echo '--- /proc/interrupts (ethoc) ---'
        grep -i \"ethoc\|\$SOC_IF\" /proc/interrupts 2>/dev/null || echo '(no ethoc interrupts found)'
    " 2>&1
else
    echo "--- /proc/interrupts (ethoc) ---"
    grep -i "ethoc\|$INTERFACE" /proc/interrupts 2>/dev/null || echo "(no ethoc interrupts found)"
fi

echo ""

# Step 8: Final verdict
echo "============================================"

if [ $TEST_EXIT -eq 0 ]; then
    echo "OVERALL VALIDATION: PASS"
else
    echo "OVERALL VALIDATION: FAIL"
fi

exit $TEST_EXIT
