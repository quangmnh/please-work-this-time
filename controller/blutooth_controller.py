import pexpect
import bluetooth


class BluetoothController():
    __connected_device = None
    __tscan = 10

    def __init__(self, tscan=10) -> None:
        self.__tscan = tscan

    def connect_device(self, name, mac_address):
        try:
            child = pexpect.spawn("bluetoothctl")
            child.expect("bluetooth")
            child.sendline("connect " + mac_address)
            child.expect("successful")
            child.close()
            self.__connected_device = {"name": name,
                                       "mac": mac_address}
            return 0
        except pexpect.ExceptionPexpect:
            return None

    def get_paired_device(self):
        return self.__connected_device

    def disconnect_device(self, mac_address):
        try:
            child = pexpect.spawn("bluetoothctl")
            child.expect("bluetooth")
            child.sendline("disconnect " + mac_address)
            child.expect("Successful")
            child.close()
            self.__connected_device = None
            return 0
        except pexpect.ExceptionPexpect:
            return None

    def bluetooth_scan(self):
        # child = pexpect.spawn('bluetoothctl')
        # child.sendline('scan on')
        devices = bluetooth.discover_devices(
            duration=self.__tscan, lookup_names=True)
        lst_devices = []
        for device in devices:
            lst_devices.append({
                "mac": device[0],
                "name": device[1]
            })
        return lst_devices
