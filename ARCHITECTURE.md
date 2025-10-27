# AWS Security Scanner - Architecture

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     User / CI/CD Pipeline                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ 1. Execute Scanner
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              AWS Security Scanner (Python)                  │
│  ┌────────────────────────────────────────────────────┐    │
│  │  AWSSecurityScanner Class                          │    │
│  │  ┌──────────────────────────────────────────────┐ │    │
│  │  │  Initialize AWS Clients                      │ │    │
│  │  │  - boto3.client('s3')                        │ │    │
│  │  │  - boto3.client('ec2')                       │ │    │
│  │  │  - boto3.client('iam')                       │ │    │
│  │  │  - boto3.client('rds')                       │ │    │
│  │  └──────────────────────────────────────────────┘ │    │
│  └────────────────────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ 2. API Calls
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    AWS API Gateway                          │
│                  (via boto3 SDK)                            │
└─┬──────────┬──────────┬──────────┬───────────────────────────┘
  │          │          │          │
  │ 3a       │ 3b       │ 3c       │ 3d
  ▼          ▼          ▼          ▼
┌────┐    ┌────┐    ┌────┐    ┌─────┐
│ S3 │    │EC2 │    │IAM │    │ RDS │
└────┘    └────┘    └────┘    └─────┘
  │          │          │          │
  │          │          │          │
  ▼          ▼          ▼          ▼
┌──────────────────────────────────────┐
│    AWS Services Return Data          │
│  • Bucket configurations             │
│  • Security group rules              │
│  • IAM user details                  │
│  • RDS instance settings             │
└──────────────┬───────────────────────┘
               │
               │ 4. Process Results
               ▼
┌─────────────────────────────────────────┐
│      Vulnerability Detection Logic      │
│  ┌────────────────────────────────┐    │
│  │ Check Against Security Rules:  │    │
│  │ • Public S3 buckets            │    │
│  │ • Open security groups         │    │
│  │ • Missing MFA                  │    │
│  │ • Old access keys              │    │
│  │ • Public databases             │    │
│  │ • Unencrypted storage          │    │
│  └────────────────────────────────┘    │
└──────────────┬──────────────────────────┘
               │
               │ 5. Generate Reports
               ▼
┌─────────────────────────────────────────┐
│         Report Generation               │
│  ┌────────────────────────────────┐    │
│  │ Vulnerability List:            │    │
│  │ • Severity classification      │    │
│  │ • Resource identification      │    │
│  │ • Issue description            │    │
│  │ • Recommendations              │    │
│  └────────────────────────────────┘    │
└─────────┬──────────────────┬────────────┘
          │                  │
          │ 6a. Console      │ 6b. JSON File
          ▼                  ▼
    ┌──────────┐      ┌─────────────────┐
    │ Terminal │      │ aws_security_   │
    │  Output  │      │ report_*.json   │
    └──────────┘      └─────────────────┘
```

## Component Details

### 1. Scanner Initialization
```python
scanner = AWSSecurityScanner(region='us-east-1')
- Creates AWS service clients
- Initializes vulnerability list
- Sets up error handling
```

### 2. Scanning Modules

#### S3 Bucket Scanner
```
scan_s3_buckets()
├── List all buckets
├── Check public access block config
├── Review bucket ACLs
└── Identify public buckets
```

#### Security Group Scanner
```
scan_security_groups()
├── Describe all security groups
├── Analyze inbound rules
├── Check for 0.0.0.0/0 access
└── Flag dangerous open ports
```

#### IAM User Scanner
```
scan_iam_users()
├── List all IAM users
├── Check access key age
├── Verify MFA status
└── Identify security gaps
```

#### RDS Instance Scanner
```
scan_rds_instances()
├── Describe DB instances
├── Check public accessibility
├── Verify encryption status
└── Report vulnerabilities
```

### 3. Vulnerability Structure

```json
{
  "severity": "CRITICAL|HIGH|MEDIUM|LOW",
  "resource": "Resource Type: Resource Name",
  "issue": "Description of the security issue",
  "recommendation": "How to fix the issue"
}
```

### 4. Report Generation Flow

```
Vulnerabilities List
        ↓
Group by Severity
        ↓
    ┌───┴───┐
    ↓       ↓
Console   JSON
Output    File
    ↓       ↓
 User    Archive
Review   Storage
```

## Data Flow Example

### Example: S3 Public Bucket Detection

```
1. User runs scanner
   └─→ python aws_security_scanner.py

2. Scanner calls AWS API
   └─→ s3.list_buckets()
       └─→ Returns: ['bucket1', 'bucket2', 'bucket3']

3. For each bucket, check access
   └─→ s3.get_public_access_block(Bucket='bucket1')
       └─→ Returns: {BlockPublicAcls: False, ...}

4. Detect vulnerability
   └─→ IF NOT all(config.values())
       └─→ ADD to vulnerabilities list
           └─→ {
                 severity: 'HIGH',
                 resource: 'S3 Bucket: bucket1',
                 issue: 'Public access not fully blocked',
                 recommendation: 'Enable all public access block settings'
               }

5. Generate report
   └─→ Console: [!] Vulnerability found in bucket: bucket1
   └─→ JSON: Save to aws_security_report_20251026_143000.json
```

## Security Model

```
┌──────────────────────────────┐
│   AWS Credentials            │
│   (Environment Variables,    │
│    AWS CLI, IAM Role)        │
└──────────────┬───────────────┘
               │
               │ Read-Only Access
               ▼
┌──────────────────────────────┐
│   IAM Permissions            │
│   • List resources           │
│   • Describe configurations  │
│   • Get metadata             │
│   ✗ NO write permissions     │
└──────────────┬───────────────┘
               │
               │ API Calls
               ▼
┌──────────────────────────────┐
│   AWS Services               │
│   • S3                       │
│   • EC2                      │
│   • IAM                      │
│   • RDS                      │
└──────────────────────────────┘
```

## CI/CD Integration

```
GitHub Repository
        ↓
   Push to main
        ↓
GitHub Actions Trigger
        ↓
    ┌───┴────────────────┐
    │                    │
    ↓                    ↓
Run Tests         Run Scanner
    │                    │
    │           ┌────────┴────────┐
    │           │                 │
    │           ↓                 ↓
    │    Scan AWS         Generate Report
    │                            │
    └────────────┬───────────────┘
                 │
                 ↓
         Upload Artifact
                 │
                 ↓
          Check Results
                 │
         ┌───────┴────────┐
         │                │
         ↓                ↓
  No Critical       Critical Found
     Issues               │
         │                ↓
         ↓           Fail Build
     Success         Send Alert
```

## Error Handling Flow

```
Scanner Operation
        ↓
    Try Block
        │
        ├─→ Success → Continue
        │
        └─→ Exception
              │
              ├─→ NoCredentialsError
              │     └─→ Exit with message
              │
              ├─→ ClientError
              │     └─→ Log error, continue
              │
              └─→ Other Exception
                    └─→ Handle gracefully
```

## Scaling Architecture

For large AWS environments:

```
                    Main Scanner
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ↓               ↓               ↓
    Region 1        Region 2        Region 3
    Scanner         Scanner         Scanner
         │               │               │
         └───────────────┴───────────────┘
                         │
                  Aggregate Results
                         │
                  Combined Report
```

## Performance Considerations

- **API Rate Limits**: Scanner includes delay handling
- **Parallel Scanning**: Can be extended for multi-threading
- **Resource Pagination**: Handles large resource lists
- **Timeout Handling**: Graceful degradation on errors

---

This architecture ensures:
✅ Security (read-only access)
✅ Reliability (error handling)
✅ Scalability (region support)
✅ Maintainability (modular design)
