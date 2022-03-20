from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np
from time import sleep


class SystemVolumeSetter():
    def __init__(self):
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_,
                                               CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))
        self.sysVolumeRange = self.volume.GetVolumeRange()

    def setSystemVolume(self, volume: float, volumeRange=[0, 100]):
        # sysVolume = self.convertVolemeRange(volume, volumeRange,
        #                                     [self.sysVolumeRange[0], self.sysVolumeRange[1]])

        sysVolume = np.interp(volume, volumeRange, [
                              self.sysVolumeRange[0], self.sysVolumeRange[1]])
        self.volume.SetMasterVolumeLevel(sysVolume, None)

    @staticmethod
    def __convertVolemeRange(volume, volumeRange=[0, 100], sysVolRange=[-65, 0]) -> float:
        sV, eV = volumeRange
        sysSV, sysEV = sysVolRange

        diffR, sysDiffer = eV-sV, sysEV-sysSV

        if(volume < sV):
            volume = sV
        elif(volume > eV):
            volume = eV
        volume -= sV
        unit = 100.0/(eV-sV)

        perSentVolume = volume*unit
        perUnitVol = sysDiffer/100

        print('Per =', perSentVolume,
              'Unit =', perUnitVol)
        print('S =', sysSV, ' E =', sysEV)

        return float(sysSV+(perSentVolume*perUnitVol))

    def __loopThrough(self):
        for i in range(-65, 0, 1):
            self.volume.SetMasterVolumeLevel(i, None)
            print(i)
            sleep(1)
