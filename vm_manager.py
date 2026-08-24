import subprocess
from pathlib import Path
import psutil
import requests
from dissect.hypervisor.descriptor.vmx import VMX
from prompt_toolkit import HTML
from prompt_toolkit import print_formatted_text as print


class VMManager:
    def __init__(
        self,
        username: str,
        password: str,
        vmrest: str = "C:\\Program Files\\VMware\\VMware Workstation\\vmrest.exe",
        base: str = "http://127.0.0.1:8697",
    ):
        self.vms = []
        self.vmx_cache = {}
        self.base = base
        self.username = username
        self.password = password
        self.auth = (username, password)
        self.encrypted_vms = set()
        if not self.is_running("vmrest.exe"):
            subprocess.Popen([vmrest])

    def refresh(self):
        """Fetch all VMs from API"""
        response = requests.get(
            f"{self.base}/api/vms",
            auth=self.auth,
        )
        self.vms = response.json()
        self.vmx_cache.clear()
        return self.vms

    def is_running(self, name):
        return any(p.info["name"] == name for p in psutil.process_iter(["name"]))

    def get_vm_by_id(self, vm_id):
        """Find VM object by id"""
        for vm in self.vms:
            if vm["id"] == vm_id:
                return vm
        return None

    def get_vmx_data(self, vm_id):
        """Parse VMX file and return attributes dict by vm_id"""
        if vm_id in self.vmx_cache:
            return self.vmx_cache[vm_id]

        vm = self.get_vm_by_id(vm_id)
        if not vm:
            return {}

        try:
            vmx_file = Path(vm["path"])
            vmx = VMX.parse(vmx_file.read_text(encoding="utf-8"))
            self.vmx_cache[vm_id] = vmx.attr
            return vmx.attr
        except Exception:
            return {}

    def get_name(self, vm_id):
        """Get VM display name from VMX or use filename"""
        vm = self.get_vm_by_id(vm_id)
        if not vm:
            return vm_id
        vmx_attr = self.get_vmx_data(vm_id)
        return vmx_attr.get("displayName", Path(vm["path"]).stem)

    def get_state(self, vm_id):
        """Get VM power state"""
        response = requests.get(
            f"{self.base}/api/vms/{vm_id}/power",
            auth=self.auth,
        )

        data = response.json()

        if not response.ok:
            if data.get("Code") == 110 and vm_id not in self.encrypted_vms:
                self.encrypted_vms.add(vm_id)
                print(
                    HTML(
                        f"<ansired>ERROR: </ansired>The VM {self.get_name(vm_id)} is encrypted"
                    )
                )
            return False

        return data.get("power_state", "") == "poweredOn"

    def get_guest_os(self, vm_id):
        """Get guest OS from VMX"""
        vmx_attr = self.get_vmx_data(vm_id)
        return vmx_attr.get("guestOS", "")

    def get_running_vms(self):
        """Get list of running VM IDs"""
        return [vm["id"] for vm in self.vms if self.get_state(vm["id"])]
