#!/bin/bash
# Start MercuryBot with comprehensive logging

# Set DEBUG mode for detailed Epic Games scheduler logs
export DEBUG=True

# Create logs directory if it doesn't exist
mkdir -p logs

# Get current timestamp for log file
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOGFILE="logs/bot_${TIMESTAMP}.log"

echo "Starting MercuryBot with logging to: $LOGFILE"
echo "Press Ctrl+C to stop"
echo ""
echo "To monitor Epic Games scheduler in real-time, run:"
echo "  tail -f $LOGFILE | grep -i epic"
echo ""

# Start bot and tee output to both console and file
python3 main.py 2>&1 | tee "$LOGFILE"
