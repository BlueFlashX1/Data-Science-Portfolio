#!/usr/bin/env bash
# setup.sh — One-command end-to-end reproduction of the Final_Project database
# using Docker. No MySQL installation needed on the host machine.
#
# What this does:
#   1. Starts MySQL 8 in a Docker container (port 33060)
#   2. Waits for MySQL to be ready
#   3. Installs Python dependencies
#   4. Loads the 6 Synthea CSVs into the 8 base tables (~20 sec)
#   5. Runs the 6 analytical reports to materialize rpt_* tables
#
# Prerequisites: Docker Desktop + Python 3.9+ (with pip).
#
# After this completes you can:
#   - Connect with any MySQL client at 127.0.0.1:33060 (user: root, pw: portfolio_demo_pw)
#   - Stop with `docker compose down` (keeps data)
#   - Reset with `docker compose down -v` (deletes volume)

set -e

# Move into the script's directory so relative paths work regardless of cwd
cd "$(dirname "$0")"

DB=Final_Project
HOST=127.0.0.1
PORT=33060
USER=root
PW=portfolio_demo_pw

# 1. Start MySQL container -----------------------------------------------------

echo "==> [1/4] Starting MySQL 8 container..."
docker compose up -d

# 2. Wait for MySQL to be ready ------------------------------------------------

echo "==> [2/4] Waiting for MySQL to accept connections..."
attempts=0
max_attempts=60
until docker compose exec -T mysql mysqladmin ping -h 127.0.0.1 -u root -p"$PW" --silent 2>/dev/null; do
  attempts=$((attempts + 1))
  if [ "$attempts" -ge "$max_attempts" ]; then
    echo ""
    echo "ERROR: MySQL did not become ready within ${max_attempts} seconds."
    echo "Check container logs with: docker compose logs mysql"
    exit 1
  fi
  printf "."
  sleep 1
done
echo " ready."

# 3. Install Python deps + load CSVs -------------------------------------------

echo "==> [3/4] Installing Python deps + loading CSVs..."

# Try a normal pip install first; fall back to --user if the system is
# PEP-668-managed (newer macOS / Linux distros). Suppress noise.
if ! pip install -r requirements.txt > /tmp/setup_pip.log 2>&1; then
  echo "  (system pip refused; retrying with --user)"
  pip install --user -r requirements.txt > /tmp/setup_pip.log 2>&1 || {
    echo "ERROR: pip install failed. See /tmp/setup_pip.log"
    exit 1
  }
fi

MYSQL_PASSWORD="$PW" python3 scripts/load_csvs.py \
  --host "$HOST" --port "$PORT" --user "$USER" --database "$DB"

# 4. Run analytical reports ----------------------------------------------------

echo ""
echo "==> [4/4] Running analytical reports..."
for f in sql/analytical_reports/*.sql; do
  name="$(basename "$f")"
  printf "  %-50s" "$name"
  # Pipe the SQL file from the host into mysql running inside the container.
  if cat "$f" | docker compose exec -T mysql mysql -u root -p"$PW" "$DB" 2>/dev/null; then
    echo " ✓"
  else
    echo " ✗ FAILED"
  fi
done

# Done ------------------------------------------------------------------------

echo ""
echo "==========================================================="
echo "Done. Final_Project database is populated and report tables"
echo "are materialized."
echo ""
echo "Connect with any MySQL client:"
echo "  host=$HOST  port=$PORT  user=$USER  password=$PW"
echo ""
echo "Stop:        docker compose down"
echo "Full reset:  docker compose down -v"
echo "==========================================================="
