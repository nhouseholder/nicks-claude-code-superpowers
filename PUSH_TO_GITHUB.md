# Push to GitHub

The repository is ready at: `~/tmp/nicks-claude-code-superpowers`

## Option 1: GitHub CLI (recommended if installed)

```bash
cd ~/tmp/nicks-claude-code-superpowers
gh repo create nicks-claude-code-superpowers --public --source=. --push
```

## Option 2: Manual GitHub setup

### 1. Create the repo on GitHub
1. Go to https://github.com/new
2. Repository name: `nicks-claude-code-superpowers`
3. Set to Public or Private (your choice)
4. Don't initialize with README (we have one)
5. Click "Create repository"

### 2. Push to GitHub

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
cd ~/tmp/nicks-claude-code-superpowers
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/nicks-claude-code-superpowers.git
git push -u origin main
```

## Option 3: SSH (if you use SSH keys)

```bash
cd ~/tmp/nicks-claude-code-superpowers
git branch -M main
git remote add origin git@github.com:YOUR_USERNAME/nicks-claude-code-superpowers.git
git push -u origin main
```

---

## After Pushing

Update the INSTALL.sh file with your actual repo URL:

```bash
cd ~/tmp/nicks-claude-code-superpowers
sed -i '' 's|https://github.com/yourusername/nicks-claude-code-superpowers.git|https://github.com/YOUR_USERNAME/nicks-claude-code-superpowers.git|' INSTALL.sh
git add INSTALL.sh
git commit -m "Update install script with correct repo URL"
git push
```

---

## Quick Test

Once pushed, test installation on a new machine:

```bash
curl -sL https://raw.githubusercontent.com/YOUR_USERNAME/nicks-claude-code-superpowers/main/INSTALL.sh | bash
```
