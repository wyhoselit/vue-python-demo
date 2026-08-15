#!/bin/bash
# Security Test Scripts for vue-python-demo

set -e

echo "=== Security Testing Suite ==="

# 1. Check for secrets in code
echo "1. Checking for secrets in code..."
if command -v trufflehog &> /dev/null; then
    trufflehog filesystem . --fail
else
    echo "  trufflehog not installed, skipping secret scan"
fi

# 2. Check for vulnerable dependencies
echo "2. Checking for vulnerable Python dependencies..."
if command -v pip-audit &> /dev/null; then
    pip-audit
else
    echo "  pip-audit not installed, skipping Python dependency audit"
fi

# 3. Check for vulnerable Node dependencies
echo "3. Checking for vulnerable Node dependencies..."
if [ -f "frontend/package.json" ]; then
    cd frontend && npm audit --audit-level=high && cd ..
else
    echo "  frontend/package.json not found, skipping Node audit"
fi

# 4. Check Docker images for vulnerabilities
echo "4. Checking Docker images for vulnerabilities..."
if command -v trivy &> /dev/null; then
    trivy image --severity HIGH,CRITICAL $(docker images --format "{{.Repository}}:{{.Tag}}" | grep -v "<none>")
else
    echo "  trivy not installed, skipping Docker image scan"
fi

# 5. Run OWASP ZAP scan (requires running app)
echo "5. OWASP ZAP scan..."
echo "  Run manually with: zap-api-scan.py -t http://localhost:8000/openapi.json -f openapi"

# 6. Check for security headers
echo "6. Checking security headers..."
if command -v curl &> /dev/null; then
    echo "  Run manually: curl -I http://localhost:8000"
fi

# 7. Run bandit for Python security issues
echo "7. Running bandit on Python code..."
if command -v bandit &> /dev/null; then
    bandit -r backend/ -ll
else
    echo "  bandit not installed, skipping Python security scan"
fi

echo "=== Security Testing Complete ==="
echo ""
echo "Manual checks required:"
echo "  - OWASP ZAP API scan"
echo "  - Security header verification"
echo "  - CORS configuration review"
echo "  - Authentication/authorization testing"