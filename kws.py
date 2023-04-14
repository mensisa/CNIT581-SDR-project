import argparse
import tkinter as tk
from threading import Thread

import pvporcupine
from pvrecorder import PvRecorder

KEYWORDS = ["stop device"]


class PorcupineThread(Thread):
    def __init__(self, access_key, device_index, keyword_var):
        super().__init__()

        self._access_key = access_key
        self._device_index = device_index
        self._keyword_var = keyword_var

        self._is_ready = False
        self._stop = False
        self._is_stopped = False

    def run(self):
        ppn = None
        recorder = None

        try:
            ppn = \
                pvporcupine.create(access_key=self._access_key, keyword_paths=self._keyword_var)

            recorder = PvRecorder(device_index=self._device_index, frame_length=ppn.frame_length)
            recorder.start()

            self._is_ready = True

            while not self._stop:
                pcm = recorder.read()
                keyword_index = ppn.process(pcm)
                if keyword_index == 0:
                    print("drone stopped")
        finally:
            if recorder is not None:
                recorder.delete()

            if ppn is not None:
                ppn.delete()

        self._is_stopped = True

    def is_ready(self):
        return self._is_ready

    def stop(self):
        self._stop = True

    def is_stopped(self):
        return self._is_stopped


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--access_key',
                        help='AccessKey obtained from Picovoice Console (https://console.picovoice.ai/)',
                        default='tHwfakI2LOhb/1l09yRCc22zakbkuNTZSb5RTmxsjC5NZdPk6jaWnQ==')

    parser.add_argument('--audio_device_index', help='Index of input audio device.', type=int, default=-1)

    args = parser.parse_args()

    window = tk.Tk()
    window.title('Porcupine Demo')
    window.minsize(width=300, height=200)

    keyword_var = tk.StringVar(window)

    for x in KEYWORDS:
        tk.Radiobutton(window, text=x, variable=keyword_var, value=x, indicatoron=False).pack(fill=tk.X, ipady=5)

    porcupine_thread = PorcupineThread(access_key=args.access_key,
                                       device_index=args.audio_device_index,
                                       keyword_var=['./model/stop-device_en_linux_v2_2_0.ppn'])

    def on_close():
        porcupine_thread.stop()
        while not porcupine_thread.is_stopped():
            pass
        window.destroy()

    window.protocol('WM_DELETE_WINDOW', on_close)

    porcupine_thread.start()
    while porcupine_thread.is_ready():
        pass

    window.mainloop()


if __name__ == '__main__':
    main()


# def get_next_audio_frame():
#     pass

# def start_keyword_detection():
#     while True:
#         audio_frame = get_next_audio_frame()
#         keyword_index = porcupine.process(audio_frame)
#         switch
#         if keyword_index == 0:
#             print(f'"{keywords[keyword_index]} detected"')
#         elif keyword_index == 1:
#             print(f'"{keywords[keyword_index]} detected"')
#             break
#         elif keyword_index == 2:
#             print(f'"{keywords[keyword_index]} detected"')
#         elif keyword_index == 3:
#             print(f'"{keywords[keyword_index]} detected"')
#         elif keyword_index == 4:
#             print(f'"{keywords[keyword_index]} detected"')
#         elif keyword_index == 5:
#             print(f'"{keywords[keyword_index]} detected"')
#         elif keyword_index == 6:
#             print(f'"{keywords[keyword_index]} detected"')
#         elif keyword_index == 7:
#             print(f'"{keywords[keyword_index]} detected"')

#     porcupine.delete()
#     print("exiting...")

