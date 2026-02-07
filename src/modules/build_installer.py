#!/usr/bin/env python3
"""
Professional JARVIS Installer Builder
Creates complete installers for macOS, Windows, and Linux
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path

class JarvisInstallerBuilder:
    def __init__(self):
        self.project_root = Path.cwd()
        self.build_dir = self.project_root / "build"
        self.dist_dir = self.project_root / "dist"
        self.installer_dir = self.project_root / "installers"
        
        # Create directories
        self.build_dir.mkdir(exist_ok=True)
        self.dist_dir.mkdir(exist_ok=True)
        self.installer_dir.mkdir(exist_ok=True)
        
        self.system = platform.system()
        print(f"Building for: {self.system}")
    
    def clean_build(self):
        """Clean previous builds"""
        print("🧹 Cleaning previous builds...")
        for dir_path in [self.build_dir, self.dist_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                dir_path.mkdir()
    
    def collect_source_files(self):
        """Collect all source files"""
        print("📦 Collecting source files...")
        
        # Source directories to include
        source_dirs = [
            "MAIN_JARVIS_SOFTWARE/src",
            "MAIN_JARVIS_SOFTWARE/data",
            "MAIN_JARVIS_SOFTWARE/config",
        ]
        
        # Main files
        main_files = ["jarvisgui.py", "jarvis.py", "launch_jarvis.py"]
        
        # Configuration files
        config_files = ["requirements.txt", "README.md", "LICENSE"]
        
        # Create source package
        source_package = self.build_dir / "jarvis_source"
        source_package.mkdir(exist_ok=True)
        
        # Copy main files
        for file in main_files:
            if Path(file).exists():
                shutil.copy2(file, source_package / file)
                print(f"  ✓ {file}")
        
        # Copy source directories
        for src_dir in source_dirs:
            if Path(src_dir).exists():
                dest_dir = source_package / Path(src_dir).name
                if dest_dir.exists():
                    shutil.rmtree(dest_dir)
                shutil.copytree(src_dir, dest_dir)
                print(f"  ✓ {src_dir}")
        
        # Copy config files
        for file in config_files:
            if Path(file).exists():
                shutil.copy2(file, source_package / file)
                print(f"  ✓ {file}")
        
        # Create launcher scripts
        self.create_launchers(source_package)
        
        return source_package
    
    def create_launchers(self, target_dir):
        """Create launcher scripts for all platforms"""
        print("🚀 Creating launcher scripts...")
        
        # macOS launcher
        mac_launcher = target_dir / "JARVIS.command"
        with open(mac_launcher, 'w') as f:
            f.write('''#!/bin/bash
cd "$(dirname "$0")"
echo "Starting JARVIS MARK I..."
python3 launch_jarvis.py
''')
        os.chmod(mac_launcher, 0o755)
        
        # Windows launcher
        win_launcher = target_dir / "JARVIS.bat"
        with open(win_launcher, 'w') as f:
            f.write('''@echo off
echo Starting JARVIS MARK I...
python launch_jarvis.py
pause
''')
        
        # Linux launcher
        linux_launcher = target_dir / "jarvis.sh"
        with open(linux_launcher, 'w') as f:
            f.write('''#!/bin/bash
cd "$(dirname "$0")"
echo "Starting JARVIS MARK I..."
python3 launch_jarvis.py
''')
        os.chmod(linux_launcher, 0o755)
        
        print("  ✓ Created launchers for all platforms")
    
    def build_executable(self):
        """Build executable using PyInstaller"""
        print("🔨 Building executable...")
        
        # PyInstaller command
        cmd = [
            "pyinstaller",
            "--name=JARVIS_MARK_I",
            "--windowed",
            "--clean",
            "--noconfirm",
            "--add-data=MAIN_JARVIS_SOFTWARE/src:src",
            "--add-data=jarvis.py:.",
            "--hidden-import=PyQt5",
            "--hidden-import=pygame",
            "--hidden-import=speech_recognition",
            "--hidden-import=pyttsx3",
            "--hidden-import=gtts",
            "--hidden-import=requests",
            "jarvisgui.py"
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print("  ✓ Executable built successfully")
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Failed to build executable: {e}")
            return False
        
        return True
    
    def create_installer(self):
        """Create platform-specific installer"""
        print(f"📦 Creating {self.system} installer...")
        
        if self.system == "Darwin":  # macOS
            self.create_mac_installer()
        elif self.system == "Windows":
            self.create_windows_installer()
        elif self.system == "Linux":
            self.create_linux_installer()
        else:
            print(f"  ⚠️  Unsupported platform: {self.system}")
            return False
        
        return True
    
    def create_mac_installer(self):
        """Create macOS .dmg installer"""
        print("  🍎 Creating macOS DMG...")
        
        # Create .app structure
        app_name = "JARVIS MARK I.app"
        app_path = self.installer_dir / app_name
        
        # Create app bundle structure
        (app_path / "Contents/MacOS").mkdir(parents=True, exist_ok=True)
        (app_path / "Contents/Resources").mkdir(parents=True, exist_ok=True)
        
        # Copy executable
        executable_src = self.dist_dir / "JARVIS_MARK_I" / "JARVIS_MARK_I"
        executable_dest = app_path / "Contents/MacOS/JARVIS"
        
        if executable_src.exists():
            shutil.copy2(executable_src, executable_dest)
            os.chmod(executable_dest, 0o755)
        
        # Create Info.plist
        plist_content = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDisplayName</key>
    <string>JARVIS MARK I</string>
    <key>CFBundleExecutable</key>
    <string>JARVIS</string>
    <key>CFBundleIdentifier</key>
    <string>com.singhindustries.jarvis</string>
    <key>CFBundleName</key>
    <string>JARVIS MARK I</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>'''
        
        with open(app_path / "Contents/Info.plist", "w") as f:
            f.write(plist_content)
        
        print(f"  ✅ Created macOS app: {app_path}")
    
    def create_windows_installer(self):
        """Create Windows .exe installer using Inno Setup"""
        print("  🪟 Creating Windows installer...")
        
        # Create NSIS script
        nsis_script = self.installer_dir / "jarvis_installer.nsi"
        nsis_content = '''!include "MUI2.nsh"

Name "JARVIS MARK I"
OutFile "JARVIS_MARK_I_Setup.exe"
InstallDir "$PROGRAMFILES\\JARVIS MARK I"
RequestExecutionLevel admin

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Section "Main"
    SetOutPath "$INSTDIR"
    
    # Copy all files
    File /r "dist\\JARVIS_MARK_I\\*"
    
    # Create shortcuts
    CreateDirectory "$SMPROGRAMS\\JARVIS MARK I"
    CreateShortcut "$SMPROGRAMS\\JARVIS MARK I\\JARVIS.lnk" "$INSTDIR\\JARVIS_MARK_I.exe"
    CreateShortcut "$DESKTOP\\JARVIS.lnk" "$INSTDIR\\JARVIS_MARK_I.exe"
    
    # Write registry
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\JARVIS" \
        "DisplayName" "JARVIS MARK I"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\JARVIS" \
        "UninstallString" '"$INSTDIR\\uninstall.exe"'
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\JARVIS" \
        "Publisher" "Singh Industries"
    
    # Create uninstaller
    WriteUninstaller "$INSTDIR\\uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\\uninstall.exe"
    RMDir /r "$INSTDIR"
    
    Delete "$SMPROGRAMS\\JARVIS MARK I\\JARVIS.lnk"
    RMDir "$SMPROGRAMS\\JARVIS MARK I"
    Delete "$DESKTOP\\JARVIS.lnk"
    
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\JARVIS"
SectionEnd
'''
        
        with open(nsis_script, "w") as f:
            f.write(nsis_content)
        
        print(f"  ✅ Created Windows installer script: {nsis_script}")
        print("  📝 To build, install NSIS and run: makensis jarvis_installer.nsi")
    
    def create_linux_installer(self):
        """Create Linux .deb package"""
        print("  🐧 Creating Linux DEB package...")
        
        # Create DEB control file
        deb_dir = self.installer_dir / "deb_package"
        deb_dir.mkdir(exist_ok=True)
        
        control_content = '''Package: jarvis-mark-i
Version: 1.0.0
Section: utils
Priority: optional
Architecture: all
Depends: python3, python3-pip, python3-pyqt5, python3-pygame
Maintainer: Singh Industries <jarvis@singhindustries.ai>
Description: JARVIS MARK I - Ultimate AI Assistant
 JARVIS MARK I is a complete AI assistant with Iron Man HUD interface,
 YouTube music integration, and advanced voice control.
'''
        
        control_file = deb_dir / "DEBIAN" / "control"
        control_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(control_file, "w") as f:
            f.write(control_content)
        
        print(f"  ✅ Created Linux DEB structure")
        print("  📝 To build: dpkg-deb --build deb_package")
    
    def create_readme(self):
        """Create README file"""
        print("📄 Creating documentation...")
        
        readme_content = '''# JARVIS MARK I - Ultimate Edition

## 🤖 Complete AI Assistant with Iron Man HUD

### Features
- ✅ Iron Man Cinematic Interface
- ✅ YouTube Music Integration
- ✅ Human-Like Voice System
- ✅ WhatsApp & App Control
- ✅ System Monitoring
- ✅ Multi-Language Support

### Installation

#### Windows
1. Run `JARVIS_MARK_I_Setup.exe`
2. Follow installation wizard
3. Launch from Start Menu or Desktop

#### macOS
1. Open `JARVIS MARK I.dmg`
2. Drag app to Applications folder
3. Launch from Applications

#### Linux
1. Install .deb package: `sudo dpkg -i jarvis-mark-i.deb`
2. Or run directly: `./jarvis.sh`

### Requirements
- Python 3.7+
- 4GB RAM minimum
- Microphone (for voice control)
- Internet connection (for AI features)

### Quick Start
1. Launch JARVIS
2. Say "Jarvis" or click the mic button
3. Try commands:
   - "What time is it?"
   - "Open browser"
   - "Play music"
   - "Send message to John"

### Support
Created by Singh Industries
Engineered by Mr. Prabhnoor Singh
Email: support@singhindustries.ai

### License
Proprietary - All rights reserved
© 2024 Singh Industries
'''
        
        readme_file = self.installer_dir / "README.txt"
        with open(readme_file, "w") as f:
            f.write(readme_content)
        
        print("  ✓ Created README.txt")
    
    def build_all(self):
        """Build complete distribution"""
        print("="*60)
        print("🚀 JARVIS MARK I - PROFESSIONAL BUILDER")
        print("="*60)
        
        # Clean
        self.clean_build()
        
        # Collect source
        source_package = self.collect_source_files()
        
        # Build executable
        if not self.build_executable():
            print("❌ Build failed!")
            return False
        
        # Create installer
        if not self.create_installer():
            print("⚠️  Installer creation skipped or failed")
        
        # Create documentation
        self.create_readme()
        
        # Summary
        print("\n" + "="*60)
        print("✅ BUILD COMPLETE!")
        print("="*60)
        print(f"\n📁 Output location: {self.installer_dir}")
        print("\n📦 Created packages:")
        print(f"  • Source package: {source_package}")
        print(f"  • Executable: {self.dist_dir}/JARVIS_MARK_I")
        
        if self.system == "Darwin":
            print(f"  • macOS App: {self.installer_dir}/JARVIS MARK I.app")
        elif self.system == "Windows":
            print(f"  • Windows installer script: {self.installer_dir}/jarvis_installer.nsi")
        
        print("\n🎉 Your software is ready for distribution!")
        print("To share: Zip the entire 'installers' folder")
        
        return True

if __name__ == "__main__":
    builder = JarvisInstallerBuilder()
    success = builder.build_all()
    sys.exit(0 if success else 1)
