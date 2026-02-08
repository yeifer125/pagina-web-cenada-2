import platform
import subprocess
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class NetInterface:
    admin_state: str
    state: str
    iface_type: str
    name: str


def run_command(command: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(command, capture_output=True, text=True, check=False)


def parse_netsh_interfaces(output: str) -> List[NetInterface]:
    interfaces: List[NetInterface] = []
    lines = [line.rstrip() for line in output.splitlines() if line.strip()]

    for line in lines:
        if line.startswith("Estado") or line.startswith("Admin") or line.startswith("---"):
            continue

        parts = line.split()
        if len(parts) < 4:
            continue

        admin_state = parts[0]
        state = parts[1]
        iface_type = parts[2]
        name = " ".join(parts[3:])
        interfaces.append(NetInterface(admin_state, state, iface_type, name))

    return interfaces


def find_hotspot_interface(interfaces: List[NetInterface]) -> Optional[NetInterface]:
    keywords = [
        "wi-fi direct",
        "hosted network",
        "mobile hotspot",
        "hotspot",
        "local area connection*",
        "conexión de área local*",
    ]

    for iface in interfaces:
        name_lower = iface.name.lower()
        if any(keyword in name_lower for keyword in keywords):
            return iface

    return None


def activar_hotspot() -> None:
    if platform.system().lower() != "windows":
        print("Este script solo funciona en Windows.")
        return

    result = run_command(["netsh", "interface", "show", "interface"])
    interfaces = parse_netsh_interfaces(result.stdout)

    if not interfaces:
        print("No se encontraron interfaces de red.")
        if result.stderr:
            print(result.stderr.strip())
        return

    hotspot_iface = find_hotspot_interface(interfaces)

    if hotspot_iface:
        print(f"Interfaz de hotspot detectada: {hotspot_iface.name}")
    else:
        print("No se detectó una interfaz de hotspot. Se listan las interfaces disponibles:")
        for iface in interfaces:
            print(f"- {iface.name} ({iface.state})")

    start = run_command(["netsh", "wlan", "start", "hostednetwork"])
    if start.returncode == 0:
        print("Hotspot activado usando netsh wlan start hostednetwork.")
        return

    print("No fue posible activar el hotspot con netsh. Intentando con PowerShell...")
    ps = run_command(["powershell", "-Command", "Start-NetMobileHotspot"])

    if ps.returncode == 0:
        print("Hotspot activado usando Start-NetMobileHotspot.")
    else:
        print("No fue posible activar el hotspot. Detalles:")
        if start.stderr:
            print(start.stderr.strip())
        if ps.stderr:
            print(ps.stderr.strip())


if __name__ == "__main__":
    activar_hotspot()
