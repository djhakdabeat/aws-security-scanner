# Setting Up on GitHub

Follow these steps to set up this project on GitHub.

## 1. Create a New Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right and select "New repository"
3. Name your repository (e.g., `aws-security-scanner`)
4. Add a description: "Python-based AWS security vulnerability scanner"
5. Choose "Public" or "Private"
6. **Do NOT** initialize with README (we already have one)
7. Click "Create repository"

## 2. Push Your Code

```bash
# Navigate to your project directory
cd aws-security-scanner

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: AWS Security Scanner"

# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/aws-security-scanner.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 3. Configure GitHub Actions (Optional)

To enable automated scanning via GitHub Actions:

### Set Up AWS Credentials

1. Go to your repository on GitHub
2. Click "Settings" → "Secrets and variables" → "Actions"
3. Click "New repository secret"
4. Add these secrets:
   - `AWS_ACCESS_KEY_ID`: Your AWS access key
   - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key

⚠️ **Security Note**: Create a dedicated IAM user with minimal permissions (see `iam-policy.json`)

### Enable GitHub Actions

1. Go to the "Actions" tab in your repository
2. Click "I understand my workflows, go ahead and enable them"
3. The workflow will now run:
   - On every push to `main` or `develop`
   - On pull requests to `main`
   - Daily at 2 AM UTC (scheduled)

## 4. Add Topics (Optional but Recommended)

1. Go to your repository homepage
2. Click the gear icon next to "About"
3. Add topics:
   - `aws`
   - `security`
   - `vulnerability-scanner`
   - `python`
   - `cloud-security`
   - `aws-security`
   - `security-tools`

## 5. Enable GitHub Features

### Issues
1. Go to Settings → Features
2. Make sure "Issues" is checked
3. Users can now report bugs and request features

### Discussions (Optional)
1. Go to Settings → Features
2. Enable "Discussions"
3. Great for Q&A and community engagement

### Security
1. Go to Settings → Security
2. Enable "Dependabot alerts"
3. Enable "Code scanning" (if available for your account)

## 6. Add Badges to README (Optional)

Add status badges to your README.md:

```markdown
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![GitHub Stars](https://img.shields.io/github/stars/YOUR_USERNAME/aws-security-scanner)
![GitHub Issues](https://img.shields.io/github/issues/YOUR_USERNAME/aws-security-scanner)
```

## 7. Create a Release

Once your code is stable:

```bash
# Tag a version
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

Then on GitHub:
1. Go to "Releases"
2. Click "Create a new release"
3. Select the tag you just created
4. Add release notes
5. Publish release

## 8. Share Your Project

Share your scanner with the community:

- Tweet about it with #AWS #CloudSecurity
- Post on Reddit (r/aws, r/netsec)
- Share on LinkedIn
- Write a blog post explaining your findings

## Repository Best Practices

### Branch Protection
1. Settings → Branches
2. Add rule for `main` branch:
   - Require pull request reviews
   - Require status checks to pass
   - Require branches to be up to date

### Issue Templates
Create `.github/ISSUE_TEMPLATE/` with:
- `bug_report.md`
- `feature_request.md`

### Pull Request Template
Create `.github/pull_request_template.md`

## Maintenance

Regular tasks:
- Review and respond to issues
- Merge pull requests
- Update dependencies: `pip list --outdated`
- Tag new releases
- Update documentation

## Getting Stars ⭐

Encourage users to star your repository if they find it useful!

---

**Ready to go?** Push your code and start helping others secure their AWS environments!
