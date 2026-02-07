"""
JARVIS MARK I - ULTIMATE LAUNCHER
Launches the COMPLETE Iron Man HUD Interface with all features
"""

import sys
import os
import subprocess

def print_banner():
    print("\n" + "="*70)
    print("  🤖 JARVIS MARK I - ULTIMATE CINEMATIC DESKTOP OVERLAY")
    print("  Tony Stark-Level AI Interface with Full Iron Man HUD")
    print("  Created by Singh Industries | Engineered by: Mr. Prabhnoor Singh")
    print("="*70 + "\n")
    
    print("�� LAUNCHING COMPLETE SYSTEM:")
    print("  ✓ Iron Man HUD Interface")
    print("  ✓ Arc Reactor Visualization")
    print("  ✓ Cinematic Sound Effects")
    print("  ✓ System Monitoring Overlay")
    print("  ✓ YouTube Music Integration")
    print("  ✓ Human-Like Voice System")
    print("  ✓ WhatsApp & App Control")
    print("  ✓ All Enhanced Features Active")
    print("-"*70)

def check_dependencies():
    """Check and install missing dependencies"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        "PyQt5",
        "pygame",
        "psutil",
        "numpy",
        "requests",
        "pyautogui",
        "pyperclip",
        "speechrecognition",
        "pyttsx3",
        "gtts",
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"  ✓ {package}")
        except ImportError:
            missing.append(package)
            print(f"  ✗ {package} (missing)")
    
    if missing:
        print(f"\n⚠️  Missing {len(missing)} packages")
        response = input("Install missing packages? (y/n): ").strip().lower()
        if response == 'y':
            import subprocess
            for package in missing:
                print(f"Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    return len(missing) == 0

def main():
    """Main launcher function"""
    print_banner()
    
    # Check if running from correct directory
    current_dir = os.getcwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Find jarvisgui.py
    possible_paths = [
        "jarvisgui.py",
        "MAIN_JARVIS_SOFTWARE/jarvisgui.py",
        "src/jarvisgui.py",
        "../jarvisgui.py",
    ]
    
    jarvisgui_path = None
    for path in possible_paths:
        if os.path.exists(path):
            jarvisgui_path = os.path.abspath(path)
            print(f"✅ Found JARVIS GUI at: {jarvisgui_path}")
            break
    
    if not jarvisgui_path:
        print("❌ ERROR: Could not find jarvisgui.py!")
        print("Make sure you're in the correct directory containing jarvisgui.py")
        print("Looking in:", possible_paths)
        return 1
    
    # Check dependencies
    if not check_dependencies():
        print("\n⚠️  Some dependencies are missing. JARVIS may not work correctly.")
        print("You can install them manually:")
        print("pip install PyQt5 pygame psutil numpy requests pyautogui pyperclip speechrecognition pyttsx3 gtts")
        response = input("Continue anyway? (y/n): ").strip().lower()
        if response != 'y':
            return 1
    
    # Run JARVIS GUI
    print("\n" + "="*70)
    print("🚀 LAUNCHING JARVIS ULTIMATE...")
    print("="*70 + "\n")
    
    try:
        # Add current directory to Python path
        sys.path.insert(0, os.path.dirname(jarvisgui_path))
        
        # Import and run
        print("Initializing cinematic interface...")
        from jarvisgui import JarvisUltimateApp
        
        app = JarvisUltimateApp()
        exit_code = app.run()
        
        return exit_code
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\nTrying alternative method...")
        
        # Try direct execution
        try:
            result = subprocess.run([sys.executable, jarvisgui_path], check=False)
            return result.returncode
        except Exception as e2:
            print(f"❌ Execution error: {e2}")
            return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n👋 JARVIS launch cancelled by user")
        sys.exit(0)
