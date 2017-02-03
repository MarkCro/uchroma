import asyncio
import logging

from evdev.uinput import UInput

from uchroma.input import InputQueue


class MacroDevice(object):

    def __init__(self, driver):

        if driver.input_manager is None:
            raise ValueError('This device does not support input events')

        self._driver = driver
        self._logger = logging.getLogger('uchroma.macro')

        self._macro_keys = driver.hardware.macro_keys

        self._uinput = UInput.from_device(driver.input_manager.input_devices[0], \
            name='UChroma Virtual Macro Device %d' % driver.device_index)
        self._queue = InputQueue(driver)

        self._task = None
        self._running = False


    @asyncio.coroutine
    def _listen(self):
        while self._running:
            event = yield from self._queue.get_events()
            self._logger.info('event: %s', event)
            if event.scancode in self._macro_keys['numeric']: 
                self._logger.info('macro')


    def start(self):
        if self._running:
            return

        self._queue.attach()
        self._driver.input_manager.grab(True)

        self._task = asyncio.ensure_future(self._listen())
        self._running = True


    def stop(self):
        if not self._running:
            return

        self._running = False

        self._task.cancel()

        self._driver.input_manager.grab(False)
        self._queue.detach()

