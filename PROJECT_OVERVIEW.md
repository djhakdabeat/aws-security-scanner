# AWS Security Scanner - Project Overview

## 📁 Project Structure

```
aws-security-scanner/
├── .github/
│   └── workflows/
│       └── security-scan.yml      # GitHub Actions CI/CD pipeline
├── tests/
│   └── test_scanner.py           # Unit tests for the scanner
├── .gitignore                    # Git ignore rules
├── aws_security_scanner.py       # Main scanner script
├── requirements.txt              # Python dependencies
├── iam-policy.json              # Required IAM permissions
├── config.ini.example           # Sample configuration file
├── LICENSE                      # MIT License
├── README.md                    # Main documentation
├── QUICKSTART.md               # 5-minute quick start guide
├── GITHUB_SETUP.md             # GitHub repository setup guide
└── CONTRIBUTING.md             # Contribution guidelines
```

## 🎯 What This Project Does

This is a **production-ready GitHub project** that includes:

1. **Security Scanner** - Python script that scans AWS infrastructure for:
   - Publicly accessible S3 buckets
   - Overly permissive security groups
   - IAM users without MFA or with old access keys
   - Publicly accessible RDS databases
   - Unencrypted resources

2. **Complete Documentation** - Everything needed to:
   - Get started in 5 minutes
   - Set up on GitHub
   - Contribute to the project
   - Deploy in production

3. **CI/CD Pipeline** - Automated workflows for:
   - Code quality checks (linting)
   - Automated security scanning
   - Scheduled daily scans
   - Report generation and storage

4. **Testing Framework** - Unit tests to ensure reliability

## 🚀 Key Features

### Scanner Capabilities
- ✅ S3 bucket security analysis
- ✅ EC2 security group auditing
- ✅ IAM user security checks
- ✅ RDS database security review
- ✅ JSON report generation
- ✅ Severity-based findings (CRITICAL, HIGH, MEDIUM)
- ✅ Command-line interface
- ✅ Multi-region support

### Security Checks Performed

| Resource Type | Checks |
|--------------|---------|
| **S3 Buckets** | Public access configuration, ACL permissions, bucket policies |
| **Security Groups** | Open ports to 0.0.0.0/0, dangerous port exposure (22, 3389, 3306, etc.) |
| **IAM Users** | Access key age, MFA status, credential rotation |
| **RDS Instances** | Public accessibility, storage encryption |

## 📊 Report Format

The scanner generates two types of output:

### 1. Console Output (Real-time)
```
[*] Scanning S3 Buckets...
  [!!] CRITICAL: Bucket my-data-bucket is publicly accessible!
  [!] Vulnerability found in bucket: my-logs-bucket

[*] Scanning Security Groups...
  [!] web-sg: Port 22 open to internet
```

### 2. JSON Report (Saved to file)
```json
{
  "scan_date": "2025-10-26T14:30:00",
  "region": "us-east-1",
  "total_vulnerabilities": 5,
  "vulnerabilities": [
    {
      "severity": "CRITICAL",
      "resource": "S3 Bucket: my-data-bucket",
      "issue": "Bucket is publicly accessible via ACL",
      "recommendation": "Remove public ACL grants"
    }
  ]
}
```

## 🔧 How to Use

### Basic Usage
```bash
# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials
aws configure

# Run the scanner
python aws_security_scanner.py
```

### Advanced Usage
```bash
# Scan specific region
python aws_security_scanner.py --region us-west-2

# Run tests
python -m pytest tests/

# Lint code
flake8 aws_security_scanner.py
```

## 🎓 Educational Value

This project is excellent for:
- **Learning AWS Security** - Understand common misconfigurations
- **Python Practice** - Well-structured, documented code
- **CI/CD Experience** - Complete GitHub Actions setup
- **Open Source Contribution** - Contribution guidelines included
- **Portfolio Projects** - Professional-grade repository

## 🔐 Security Considerations

### Safe to Use
- ✅ Read-only permissions (no modifications)
- ✅ Uses AWS SDK best practices
- ✅ No credentials stored in code
- ✅ Open source and transparent

### Important Notes
- Requires appropriate IAM permissions (see `iam-policy.json`)
- Test in non-production environment first
- Not a replacement for comprehensive tools like AWS Security Hub
- Educational and testing purposes

## 🛠 Customization Options

The scanner can be extended to check:
- CloudTrail logging status
- VPC flow logs
- Lambda function configurations
- EBS encryption
- CloudWatch alarms
- Config rules compliance
- And much more!

## 📈 Future Enhancements

Potential additions (see CONTRIBUTING.md):
- [ ] HTML report generation
- [ ] Multi-region parallel scanning
- [ ] Custom rule configuration
- [ ] Email/Slack notifications
- [ ] Cost analysis integration
- [ ] Compliance framework checks (CIS, PCI-DSS)
- [ ] Historical trend tracking
- [ ] Remediation automation

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to report bugs
- How to suggest features
- Code style guidelines
- Pull request process

## 📜 License

MIT License - Free to use, modify, and distribute

## 🌟 Getting Started

1. **Read**: [QUICKSTART.md](QUICKSTART.md) - Get running in 5 minutes
2. **Deploy**: [GITHUB_SETUP.md](GITHUB_SETUP.md) - Put it on GitHub
3. **Learn**: [README.md](README.md) - Deep dive into features
4. **Contribute**: [CONTRIBUTING.md](CONTRIBUTING.md) - Make it better

## 💡 Use Cases

- **DevOps Teams**: Integrate into CI/CD for continuous security checks
- **Security Audits**: Quick assessment of AWS infrastructure
- **Learning Tool**: Understand AWS security best practices
- **Compliance**: Regular scanning for policy compliance
- **Cost Savings**: Identify unused resources and security risks

## 📞 Support

- Open an issue for bugs
- Start a discussion for questions
- Read the documentation for guidance
- Check existing issues before creating new ones

---

**Ready to scan?** Start with [QUICKSTART.md](QUICKSTART.md) and secure your AWS environment in minutes!
