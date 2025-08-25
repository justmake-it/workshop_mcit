#!/usr/bin/env python3
"""Setup verification script for MCIT AI Agents Workshop."""

import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check Python version >= 3.9"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (need 3.9+)")
        return False

def check_command(command, version_flag='--version'):
    """Check if command exists"""
    try:
        result = subprocess.run([command, version_flag], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            # Get first line of output for cleaner display
            version_line = result.stdout.strip().split('\n')[0]
            print(f"✅ {command}: {version_line}")
            return True
    except FileNotFoundError:
        pass
    print(f"❌ {command} not found")
    return False

def check_nvm_and_node():
    """Check NVM and Node.js installation"""
    # Check if NVM is available (sourced function, not executable)
    try:
        # Try to run 'nvm version' in a sourced shell
        result = subprocess.run(['bash', '-c', 'source ~/.bashrc; nvm --version 2>/dev/null || source ~/.zshrc; nvm --version 2>/dev/null'], 
                              capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            nvm_version = result.stdout.strip()
            print(f"✅ NVM: v{nvm_version}")
            
            # Check Node.js version
            node_result = subprocess.run(['node', '--version'], 
                                       capture_output=True, text=True)
            if node_result.returncode == 0:
                node_version = node_result.stdout.strip()
                if node_version.startswith('v20'):
                    print(f"✅ Node.js: {node_version}")
                    return True
                else:
                    print(f"⚠️ Node.js: {node_version} (recommend v20+)")
                    return True
        
        # Fallback: check if node exists even without NVM
        return check_command('node', '--version')
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        return check_command('node', '--version')

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found")
        return False
    
    # Check for required environment variables
    required_vars = ['GOOGLE_CLOUD_PROJECT', 'GOOGLE_CLOUD_LOCATION', 'GOOGLE_APPLICATION_CREDENTIALS']
    missing_vars = []
    
    try:
        with open(env_file, encoding='utf-8') as f:
            content = f.read()
            for var in required_vars:
                if var not in content:
                    missing_vars.append(var)
    except (OSError, IOError) as e:
        print(f"❌ Error reading .env file: {e}")
        return False
    
    if missing_vars:
        print(f"❌ .env file missing variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ .env file exists with required variables")
    return True

def check_credentials_file():
    """Check if credentials file exists"""
    credentials_file = Path('credentials/credentials.json')
    if not credentials_file.exists():
        print("❌ credentials/credentials.json not found")
        return False
    
    # Check if file is not empty
    try:
        if credentials_file.stat().st_size == 0:
            print("❌ credentials/credentials.json is empty")
            return False
    except OSError as e:
        print(f"❌ Error accessing credentials file: {e}")
        return False
    
    print("✅ credentials/credentials.json exists")
    return True

def check_gemini_cli():
    """Check Gemini CLI installation and connection"""
    # First check if gemini command exists
    try:
        result = subprocess.run(['gemini', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Gemini CLI installed")
        else:
            print("❌ Gemini CLI not found")
            return False
    except FileNotFoundError:
        print("❌ Gemini CLI not found")
        return False
    
    # Test connection (basic test)
    try:
        result = subprocess.run(['gemini', '-p', 'Hello'], 
                              input="", capture_output=True, text=True, timeout=15)
        if result.returncode == 0 and len(result.stdout.strip()) > 0:
            print("✅ Gemini CLI connection working")
            return True
        else:
            print("⚠️ Gemini CLI installed but connection test failed")
            print("   This might be due to authentication or network issues")
            return False
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("⚠️ Gemini CLI connection test timed out or failed")
        return False

def main():
    print("🔧 MCIT AI Agents Workshop Setup Verification")
    print("=" * 55)
    
    checks = []
    
    # Python environment
    print("\n🐍 Python Environment:")
    checks.append(check_python_version())
    
    # System commands
    print("\n💻 System Tools:")
    checks.append(check_command('git'))
    checks.append(check_nvm_and_node())
    checks.append(check_command('npm'))
    
    # Gemini CLI
    print("\n🤖 Gemini CLI:")
    checks.append(check_gemini_cli())
    
    # Configuration files
    print("\n📁 Configuration Files:")
    checks.append(check_env_file())
    checks.append(check_credentials_file())
    
    # Summary
    print("\n" + "=" * 55)
    total = len(checks)
    passed = sum(checks)
    
    if passed == total:
        print(f"🎉 All {total} checks passed! You're ready for the workshop.")
        print("\n🚀 Final test: Try running 'gemini chat \"Hello!\"' to confirm everything works.")
        return 0
    else:
        print(f"⚠️ {passed}/{total} checks passed. Please fix the issues above before the workshop.")
        return 1

if __name__ == '__main__':
    sys.exit(main())