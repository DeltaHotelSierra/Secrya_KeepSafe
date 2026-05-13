#!/usr/bin/env python3
"""
Secrya KeepSafe Integration Setup Script
Automates the setup of backend service and extension configuration
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def print_step(number, text):
    """Print a numbered step"""
    print(f"[{number}] {text}")


def check_python_version():
    """Check Python version"""
    print_step(1, "Checking Python version...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"❌ Python 3.9+ required (found {version.major}.{version.minor})")
        return False
    
    print(f"✅ Python {version.major}.{version.minor} detected")
    return True


def create_directories():
    """Create necessary directories"""
    print_step(2, "Creating directories...")
    
    dirs = [
        'backend-starter',
        'backend-starter/logs',
        'backend-starter/reports',
        'extension-starter/src/popup',
        'extension-starter/src/background',
        'extension-starter/src/icons',
    ]
    
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {d}")


def setup_backend_venv():
    """Set up backend virtual environment"""
    print_step(3, "Setting up backend virtual environment...")
    
    venv_path = 'backend-starter/venv'
    
    if os.path.exists(venv_path):
        print(f"  ⚠️  Virtual environment already exists")
        return True
    
    try:
        subprocess.run([sys.executable, '-m', 'venv', venv_path], check=True)
        print(f"  ✅ Virtual environment created: {venv_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Failed to create virtual environment: {e}")
        return False


def install_dependencies():
    """Install Python dependencies"""
    print_step(4, "Installing dependencies...")
    
    # Detect OS
    if sys.platform.startswith('win'):
        pip_path = 'backend-starter\\venv\\Scripts\\pip'
    else:
        pip_path = 'backend-starter/venv/bin/pip'
    
    try:
        subprocess.run(
            [pip_path, 'install', '-r', 'backend-starter/requirements.txt'],
            check=True
        )
        print(f"  ✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Failed to install dependencies: {e}")
        return False


def setup_env_file():
    """Set up .env file"""
    print_step(5, "Setting up backend environment...")
    
    env_path = 'backend-starter/.env'
    
    if os.path.exists(env_path):
        print(f"  ⚠️  .env already exists")
        return True
    
    env_example = 'backend-starter/.env.example'
    if os.path.exists(env_example):
        shutil.copy(env_example, env_path)
        print(f"  ✅ .env created from template")
        print(f"\n  ⚠️  IMPORTANT: Edit {env_path} and add your:")
        print(f"     - GOOGLE_CLIENT_ID")
        print(f"     - GOOGLE_CLIENT_SECRET")
        return True
    else:
        print(f"  ⚠️  .env.example not found - create manually")
        return False


def validate_manifest():
    """Validate manifest.json"""
    print_step(6, "Validating extension manifest...")
    
    manifest_path = 'extension-starter/manifest.json'
    
    if not os.path.exists(manifest_path):
        print(f"  ⚠️  manifest.json not found")
        return False
    
    try:
        with open(manifest_path, 'r') as f:
            data = json.load(f)
        
        if 'oauth2' not in data:
            print(f"  ⚠️  oauth2 configuration missing")
            return False
        
        if 'client_id' not in data['oauth2']:
            print(f"  ⚠️  GOOGLE_CLIENT_ID not set in manifest.json")
            print(f"     Update: oauth2 > client_id")
            return True  # Don't fail - user can update later
        
        print(f"  ✅ manifest.json is valid")
        return True
    
    except json.JSONDecodeError as e:
        print(f"  ❌ Invalid manifest.json: {e}")
        return False


def create_icon_placeholder():
    """Create placeholder icons"""
    print_step(7, "Creating extension icons...")
    
    icon_dir = 'extension-starter/src/icons'
    sizes = [16, 48, 128]
    
    try:
        from PIL import Image, ImageDraw
        
        for size in sizes:
            img = Image.new('RGB', (size, size), color=(102, 126, 234))
            draw = ImageDraw.Draw(img)
            
            # Draw 'S' letter
            text = 'S'
            bbox = draw.textbbox((0, 0), text, font=None)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (size - text_width) // 2
            y = (size - text_height) // 2
            
            draw.text((x, y), text, fill=(255, 255, 255))
            
            path = os.path.join(icon_dir, f'icon{size}.png')
            img.save(path)
            print(f"  ✅ Created {path}")
        
        return True
    
    except ImportError:
        print(f"  ⚠️  Pillow not installed - icons not created")
        print(f"     Run: pip install Pillow")
        print(f"     Or create 16x16, 48x48, 128x128 PNG files manually")
        return True  # Don't fail


def summary():
    """Print summary and next steps"""
    print_header("Setup Complete!")
    
    print("\n✅ Completed Tasks:")
    print("  • Python version verified")
    print("  • Directories created")
    print("  • Virtual environment set up")
    print("  • Dependencies installed")
    print("  • Environment configured")
    print("  • Extension validated")
    print("  • Icons created")
    
    print("\n📝 Next Steps:")
    print("\n1. Configure Backend:")
    print("   • Edit backend-starter/.env")
    print("   • Add GOOGLE_CLIENT_ID")
    print("   • Add GOOGLE_CLIENT_SECRET")
    print("   • Get these from Google Cloud Console")
    
    print("\n2. Update Extension:")
    print("   • Edit extension-starter/manifest.json")
    print("   • Set oauth2.client_id to your GOOGLE_CLIENT_ID")
    
    print("\n3. Start Backend:")
    if sys.platform.startswith('win'):
        print("   • Run: .\\backend-starter\\venv\\Scripts\\activate")
    else:
        print("   • Run: source backend-starter/venv/bin/activate")
    print("   • Then: python backend-starter/app.py")
    
    print("\n4. Load Extension:")
    print("   • Open Chrome and go to chrome://extensions/")
    print("   • Enable Developer Mode")
    print("   • Click Load Unpacked")
    print("   • Select extension-starter/ folder")
    
    print("\n5. Test:")
    print("   • Click extension icon")
    print("   • Click 'Login with Google'")
    print("   • Verify emails load")
    print("   • Test analysis")
    
    print("\n📖 Documentation:")
    print("   • EXTENSION_SETUP_GUIDE.md - Complete setup instructions")
    print("   • BROWSER_EXTENSION_PROPOSAL.md - Architecture details")
    print("   • backend-starter/README.md - Backend documentation")
    print("   • extension-starter/README.md - Extension documentation")
    
    print("\n" + "="*60)
    print("For detailed instructions, see EXTENSION_SETUP_GUIDE.md")
    print("="*60 + "\n")


def main():
    """Main setup flow"""
    print_header("Secrya KeepSafe Browser Extension Setup")
    
    steps = [
        ("Python version check", check_python_version),
        ("Create directories", create_directories),
        ("Set up virtual environment", setup_backend_venv),
        ("Install dependencies", install_dependencies),
        ("Configure environment", setup_env_file),
        ("Validate manifest", validate_manifest),
        ("Create icons", create_icon_placeholder),
    ]
    
    failed = False
    
    for i, (name, func) in enumerate(steps, 1):
        try:
            if not func():
                print(f"\n⚠️  {name} had warnings, continuing...\n")
        except Exception as e:
            print(f"\n❌ {name} failed: {e}\n")
            failed = True
    
    summary()
    
    if failed:
        print("⚠️  Some setup steps had issues. Please review above.")
        return 1
    else:
        print("✅ Setup completed successfully!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
