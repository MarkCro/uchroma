import hidapi

from uchroma.device_base import BaseCommand
from uchroma.keyboard import UChromaKeyboard
from uchroma.models import Hardware
from uchroma.util import scale_brightness


class UChromaLaptop(UChromaKeyboard):
    """
    Commands required for Blade laptops
    """

    # commands
    class Command(BaseCommand):
        """
        Enumeration of standard commands not handled elsewhere
        """
        SET_BRIGHTNESS = (0x0e, 0x04, 0x02)
        GET_BRIGHTNESS = (0x0e, 0x84, 0x02)


    def __init__(self, model: Hardware, devinfo: hidapi.DeviceInfo, input_devices=None):
        super(UChromaLaptop, self).__init__(model, devinfo, input_devices)


    def _set_brightness(self, level: float):
        return self.run_command(UChromaLaptop.Command.SET_BRIGHTNESS, 0x01, scale_brightness(level))


    def _get_brightness(self) -> float:
        value = self.run_with_result(UChromaLaptop.Command.GET_BRIGHTNESS)
        if value is None:
            return 0.0
        return scale_brightness(int(value[1]), True)

