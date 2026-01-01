#!/bin/bash
# Check Epic Games related logs

echo "=== Epic Games Log Analyzer ==="
echo ""

# Check if there are any log files
if [ -d "logs" ] && [ "$(ls -A logs/*.log 2>/dev/null)" ]; then
    LATEST_LOG=$(ls -t logs/*.log | head -1)
    echo "📁 Latest log file: $LATEST_LOG"
    echo ""

    echo "🕐 Epic Games Scheduler Activity:"
    echo "─────────────────────────────────"
    grep -i "EPIC ->" "$LATEST_LOG" | tail -20
    echo ""

    echo "📢 Epic Games Notifications Sent:"
    echo "─────────────────────────────────"
    grep -i "epic.*notification\|epic games" "$LATEST_LOG" | grep -i "send\|notif" | tail -10
    echo ""

    echo "⚠️  Epic Games Errors:"
    echo "─────────────────────────────────"
    grep -i "epic" "$LATEST_LOG" | grep -i "error\|fail\|exception" | tail -10

else
    echo "❌ No log files found in logs/ directory"
    echo ""
    echo "Options to find logs:"
    echo "1. Check if bot is running: ps aux | grep main.py"
    echo "2. Check systemd logs: sudo journalctl -u mercurybot | grep -i epic"
    echo "3. Check docker logs: docker logs mercurybot | grep -i epic"
    echo "4. Start bot with logging: ./start_with_logging.sh"
fi
