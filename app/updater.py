import urllib.request
import json
import os
import sys
import subprocess
from tkinter import messagebox

class Updater:
    def __init__(self):
        self.current_version = "1.0.0"
        self.github_api = "https://api.github.com/repos/Mytools1988/MY_TODO/releases/latest"
        self.update_url = None

    def check_for_updates(self):
        """Prüft auf neue Versionen"""
        try:
            with urllib.request.urlopen(self.github_api) as response:
                data = json.loads(response.read().decode())
                latest_version = data['tag_name'].replace('v', '')
                
                if self._compare_versions(latest_version, self.current_version) > 0:
                    self.update_url = data['assets'][0]['browser_download_url']
                    return True, latest_version
            
            return False, self.current_version
            
        except Exception as e:
            print(f"Fehler beim Update-Check: {e}")
            return False, self.current_version

    def download_and_install_update(self):
        """Lädt das Update herunter und installiert es"""
        try:
            if not self.update_url:
                return False
                
            # Download
            installer_path = os.path.join(os.getenv('TEMP'), 'mytodo-setup.exe')
            urllib.request.urlretrieve(self.update_url, installer_path)
            
            # Starte Installer
            if messagebox.askyesno(
                "Update bereit",
                "Das Update wurde heruntergeladen. Jetzt installieren?"
            ):
                subprocess.Popen([installer_path])
                sys.exit()
                
            return True
            
        except Exception as e:
            print(f"Fehler beim Update-Download: {e}")
            return False

    def _compare_versions(self, v1, v2):
        """Vergleicht zwei Versionsnummern"""
        v1_parts = [int(x) for x in v1.split('.')]
        v2_parts = [int(x) for x in v2.split('.')]
        
        for i in range(max(len(v1_parts), len(v2_parts))):
            v1_part = v1_parts[i] if i < len(v1_parts) else 0
            v2_part = v2_parts[i] if i < len(v2_parts) else 0
            
            if v1_part > v2_part:
                return 1
            elif v1_part < v2_part:
                return -1
                
        return 0 