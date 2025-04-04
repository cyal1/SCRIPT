            if self.interactive:
                print('Available devices:\n')
                devices = frida.enumerate_devices()
                devices.append(frida.get_device_manager().add_remote_device('127.0.0.1:27042'))
                for i in range(len(devices)):
                    print(f'{i}) {devices[i]}')
                self.device = devices[
                    int(Numeric('\nEnter the index of the device to use:', lbound=0, ubound=len(devices) - 1).ask())]
                android_dev = android_device(self.device.id)
                android_dev.print_dev_properties()
                self.do_use("webviews/hook_webviews", True)
