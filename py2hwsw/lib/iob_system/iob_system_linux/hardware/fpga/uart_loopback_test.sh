#!/bin/sh

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#!/bin/sh
echo "Verify current UART 1 and 2 interrupt count (may be none if no interrupts triggered)"
cat /proc/interrupts | grep -E 'CPU0|3 Edge|4 Edge'

# UART1 connected to UART2 in loopback mode
echo "Writing to UART1 and reading from UART2..."
cat /dev/ttyS1 & sleep 1; echo "Example UART1 to UART2 message." > /dev/ttyS2; kill %

echo "Writing to UART2 and reading from UART1..."
cat /dev/ttyS2 & sleep 1; echo "Example UART2 to UART1 message." > /dev/ttyS1; kill %

echo "Verify UART 1 and 2 interrupt count increased"
cat /proc/interrupts | grep -E 'CPU0|3 Edge|4 Edge'

