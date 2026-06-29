#!/usr/bin/env bash
# start-harnesses.sh
#
# Legacy compatibility wrapper for the documented koios harness CLI.
#
# Usage:
#   ./scripts/start-harnesses.sh
#
# Equivalent to:
#   ./scripts/koios harnesses start

set -euo pipefail

exec "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/koios" harnesses start
