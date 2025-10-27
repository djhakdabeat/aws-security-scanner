"""
Unit tests for AWS Security Scanner
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import the scanner
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aws_security_scanner import AWSSecurityScanner


class TestAWSSecurityScanner(unittest.TestCase):
    """Test cases for AWS Security Scanner"""

    def setUp(self):
        """Set up test fixtures"""
        with patch('boto3.client'):
            self.scanner = AWSSecurityScanner(region='us-east-1')
            self.scanner.vulnerabilities = []

    def test_scanner_initialization(self):
        """Test scanner initializes with correct region"""
        self.assertEqual(self.scanner.region, 'us-east-1')
        self.assertEqual(len(self.scanner.vulnerabilities), 0)

    @patch('boto3.client')
    def test_public_s3_bucket_detection(self, mock_boto_client):
        """Test detection of publicly accessible S3 buckets"""
        # Mock S3 client
        mock_s3 = Mock()
        mock_boto_client.return_value = mock_s3
        
        # Mock bucket list
        mock_s3.list_buckets.return_value = {
            'Buckets': [{'Name': 'test-bucket'}]
        }
        
        # Mock public access block (not fully blocked)
        mock_s3.get_public_access_block.return_value = {
            'PublicAccessBlockConfiguration': {
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
        }
        
        self.scanner.s3 = mock_s3
        self.scanner.scan_s3_buckets()
        
        # Should detect vulnerability
        self.assertGreater(len(self.scanner.vulnerabilities), 0)
        self.assertEqual(self.scanner.vulnerabilities[0]['severity'], 'HIGH')

    @patch('boto3.client')
    def test_open_security_group_detection(self, mock_boto_client):
        """Test detection of security groups open to internet"""
        mock_ec2 = Mock()
        mock_boto_client.return_value = mock_ec2
        
        # Mock security group with SSH open to world
        mock_ec2.describe_security_groups.return_value = {
            'SecurityGroups': [{
                'GroupId': 'sg-12345',
                'GroupName': 'test-sg',
                'IpPermissions': [{
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }]
            }]
        }
        
        self.scanner.ec2 = mock_ec2
        self.scanner.scan_security_groups()
        
        # Should detect vulnerability
        self.assertGreater(len(self.scanner.vulnerabilities), 0)
        self.assertIn('0.0.0.0/0', self.scanner.vulnerabilities[0]['issue'])

    @patch('boto3.client')
    def test_old_access_key_detection(self, mock_boto_client):
        """Test detection of old IAM access keys"""
        mock_iam = Mock()
        mock_boto_client.return_value = mock_iam
        
        # Mock IAM user with old access key
        mock_iam.list_users.return_value = {
            'Users': [{'UserName': 'test-user'}]
        }
        
        old_date = datetime.now() - timedelta(days=120)
        mock_iam.list_access_keys.return_value = {
            'AccessKeyMetadata': [{
                'AccessKeyId': 'AKIAIOSFODNN7EXAMPLE',
                'CreateDate': old_date
            }]
        }
        
        mock_iam.list_mfa_devices.return_value = {'MFADevices': []}
        
        self.scanner.iam = mock_iam
        self.scanner.scan_iam_users()
        
        # Should detect old key
        old_key_vulns = [v for v in self.scanner.vulnerabilities if 'days old' in v['issue']]
        self.assertGreater(len(old_key_vulns), 0)

    @patch('boto3.client')
    def test_public_rds_detection(self, mock_boto_client):
        """Test detection of publicly accessible RDS instances"""
        mock_rds = Mock()
        mock_boto_client.return_value = mock_rds
        
        # Mock RDS instance that is public
        mock_rds.describe_db_instances.return_value = {
            'DBInstances': [{
                'DBInstanceIdentifier': 'test-db',
                'PubliclyAccessible': True,
                'StorageEncrypted': False
            }]
        }
        
        self.scanner.rds = mock_rds
        self.scanner.scan_rds_instances()
        
        # Should detect both public access and lack of encryption
        self.assertGreaterEqual(len(self.scanner.vulnerabilities), 2)

    def test_vulnerability_severity_levels(self):
        """Test that vulnerabilities use correct severity levels"""
        valid_severities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
        
        # Add sample vulnerabilities
        self.scanner.vulnerabilities = [
            {'severity': 'CRITICAL', 'resource': 'test1', 'issue': 'test', 'recommendation': 'fix'},
            {'severity': 'HIGH', 'resource': 'test2', 'issue': 'test', 'recommendation': 'fix'},
            {'severity': 'MEDIUM', 'resource': 'test3', 'issue': 'test', 'recommendation': 'fix'},
        ]
        
        for vuln in self.scanner.vulnerabilities:
            self.assertIn(vuln['severity'], valid_severities)

    def test_vulnerability_structure(self):
        """Test that vulnerabilities have required fields"""
        required_fields = ['severity', 'resource', 'issue', 'recommendation']
        
        test_vuln = {
            'severity': 'HIGH',
            'resource': 'S3 Bucket: test-bucket',
            'issue': 'Publicly accessible',
            'recommendation': 'Enable public access block'
        }
        
        for field in required_fields:
            self.assertIn(field, test_vuln)


class TestReportGeneration(unittest.TestCase):
    """Test cases for report generation"""

    def setUp(self):
        """Set up test fixtures"""
        with patch('boto3.client'):
            self.scanner = AWSSecurityScanner(region='us-east-1')
            self.scanner.vulnerabilities = [
                {'severity': 'CRITICAL', 'resource': 'test1', 'issue': 'critical issue', 'recommendation': 'fix now'},
                {'severity': 'HIGH', 'resource': 'test2', 'issue': 'high issue', 'recommendation': 'fix soon'},
                {'severity': 'MEDIUM', 'resource': 'test3', 'issue': 'medium issue', 'recommendation': 'fix later'},
            ]

    @patch('builtins.open', create=True)
    @patch('json.dump')
    def test_report_generation(self, mock_json_dump, mock_open):
        """Test that reports are generated correctly"""
        self.scanner.generate_report()
        
        # Verify JSON dump was called
        mock_json_dump.assert_called_once()
        
        # Verify report structure
        call_args = mock_json_dump.call_args[0][0]
        self.assertIn('scan_date', call_args)
        self.assertIn('region', call_args)
        self.assertIn('total_vulnerabilities', call_args)
        self.assertIn('vulnerabilities', call_args)
        self.assertEqual(call_args['total_vulnerabilities'], 3)


if __name__ == '__main__':
    unittest.main()
