import os
import time

from pypresence.presence import Presence

from vm_manager import VMManager

VMWARE_PATH = os.getenv(
    "VMWARE_PATH", "C:\\Program Files\\VMware\\VMware Workstation\\"
)
USERNAME = os.getenv("VMREST_USERNAME")
PASSWORD = os.getenv("VMREST_PASSWORD")
if USERNAME is None or PASSWORD is None:
    raise RuntimeError("VMREST_USERNAME or VMREST_PASSWORD is not set")
VMREST_PATH = VMWARE_PATH + "vmrest.exe"

LOGOS = {
    "win98": "win9x",
    "win95": "win9x",
    "dos": "dos",
    "winxppro-64": "winxp",
    "winxppro": "winxp",
}
NAMES = {
    "win98": "Windows 98",
    "win95": "Windows 95",
    "dos": "MS-DOS",
    "winxppro": "Windows XP Professional",
    "winxppro-64": "Windows XP Professional 64-bit",
}
CLIENT_ID = "1540314849827881010"

rpc = Presence(CLIENT_ID)
rpc.connect()
vm_mgr = VMManager(username=USERNAME, password=PASSWORD, vmrest=str(VMREST_PATH))

try:
    while True:
        vm_mgr.refresh()
        running_ids = vm_mgr.get_running_vms()

        if running_ids:
            active_vm_id = running_ids[0]
            display_name = vm_mgr.get_name(active_vm_id)
            state = "Running " + display_name
            if len(running_ids) > 1:
                state += f" • {len(running_ids) - 1} VMs running"

            guest_os = vm_mgr.get_guest_os(active_vm_id)
            rpc.update(
                state=state,
                small_image=LOGOS.get(guest_os),
                small_text=NAMES.get(guest_os, display_name),
            )
        else:
            rpc.update(state="No VMs running")

        time.sleep(3)
except KeyboardInterrupt:
    rpc.clear()
    rpc.close()
