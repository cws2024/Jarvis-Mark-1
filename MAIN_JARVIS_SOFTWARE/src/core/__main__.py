#!/usr/bin/env python3
"""
JARVIS MARK I - Main Entry Point
Created by Singh Industries
Engineered by Mr. Prabhnoor Singh
"""

import sys
import os

def main():
    print("\n" + "="*70)
    print("  🤖 JARVIS MARK I - ENHANCED ULTIMATE EDITION")
    print("  Created by Singh Industries")
    print("  Designed & Engineered by: Mr. Prabhnoor Singh")
    print("="*70 + "\n")
    
    try:
        # Import jarvis module
        from core.jarvis import JarvisMarkIEnhanced
        
        # Create JARVIS instance
        jarvis = JarvisMarkIEnhanced()
        
        # Start JARVIS
        jarvis.run()
        
    except KeyboardInterrupt:
        print("\n\nJARVIS shutting down... Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting JARVIS: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
