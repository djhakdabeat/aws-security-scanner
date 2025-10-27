# Quick Start Guide

Get started with AWS Security Scanner in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- AWS account with active credentials
- Basic familiarity with AWS services

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Configure AWS Credentials

### Option A: Using AWS CLI
```bash
aws configure
```

Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., us-east-1)
- Output format (json)

### Option B: Using Environment Variables
```bash
export AWS_ACCESS_KEY_ID=your_access_key_here
export AWS_SECRET_ACCESS_KEY=your_secret_key_here
export AWS_DEFAULT_REGION=us-east-1
```

### Option C: Using AWS Credentials File
Create `~/.aws/credentials`:
```ini
[default]
aws_access_key_id = your_access_key_here
aws_secret_access_key = your_secret_key_here
```

## Step 3: Run Your First Scan

```bash
python aws_security_scanner.py
```

That's it! The scanner will check your AWS resources and generate a report.

## Step 4: Review Results

The scanner will:
1. Display findings in your terminal
2. Save a detailed JSON report: `aws_security_report_YYYYMMDD_HHMMSS.json`

## Understanding Results

### Severity Levels
- **CRITICAL**: Immediate action required (e.g., public S3 buckets)
- **HIGH**: Should be addressed soon (e.g., SSH open to internet)
- **MEDIUM**: Should be reviewed (e.g., old access keys)

### Sample Output
```
[CRITICAL] S3 Bucket: my-data-bucket
  Issue: Bucket is publicly accessible via ACL
  Recommendation: Remove public ACL grants

[HIGH] Security Group: web-sg (sg-12345)
  Issue: Port 22 open to 0.0.0.0/0
  Recommendation: Restrict access to specific IP ranges
```

## Common Issues

### "NoCredentialsError"
- Your AWS credentials are not configured
- Run `aws configure` or set environment variables

### "Access Denied" errors
- Your IAM user/role lacks required permissions
- Apply the IAM policy from `iam-policy.json`

### "Region not found"
- Specify a valid AWS region:
  ```bash
  python aws_security_scanner.py --region us-west-2
  ```

## Next Steps

1. **Address Critical Findings**: Fix any CRITICAL vulnerabilities first
2. **Run Regular Scans**: Schedule daily scans via cron or CI/CD
3. **Customize**: Modify the scanner for your specific needs
4. **Contribute**: Check out CONTRIBUTING.md to improve the tool

## Scanning Multiple Regions

```bash
# Scan different regions
python aws_security_scanner.py --region us-west-2
python aws_security_scanner.py --region eu-west-1
python aws_security_scanner.py --region ap-southeast-1
```

## Production Tips

1. **Use IAM Roles**: Prefer IAM roles over access keys in production
2. **Least Privilege**: Grant only required permissions (see iam-policy.json)
3. **Secure Reports**: Store scan reports securely with restricted access
4. **Automate**: Set up scheduled scans in your CI/CD pipeline
5. **Alert**: Configure notifications for critical findings

## Need Help?

- Read the full [README.md](README.md)
- Check [CONTRIBUTING.md](CONTRIBUTING.md) for development setup
- Open an issue on GitHub for bugs or questions

---

**Pro Tip**: Run the scanner in a test AWS account first to understand the findings before running in production!
