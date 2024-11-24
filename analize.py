import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
import result

MIN = 100
MAX = 500

def restrictionFunc(min=None, max=None, target=None):
  if min is None and max is not None:
    return target <= max
  elif min is not None and max is None:
    return target >= min
  elif min is not None and max is not None:
    return target <= max and target >= min
  else:
    return True

def main(file):
  sounds = AudioSegment.from_file(file, 'wav')
  print(f'channel: {sounds.channels}')
  print(f'frame rate: {sounds.frame_rate}')
  print(f'duration: {sounds.duration_seconds} s')

  sig = np.array(sounds.get_array_of_samples())[::sounds.channels]
  dt = 1.0/sounds.frame_rate # サンプリング時間

  # 時間アレイを作る
  tms = 0.0 # サンプル開始時間を0にセット
  tme = sounds.duration_seconds # サンプル終了時刻
  tm = np.linspace(tms, tme, len(sig), endpoint=False) # 時間ndarrayを作成

  # DFT
  N = len(sig)
  X = np.fft.fft(sig)
  X = np.abs(X[0:N//2])

  f = np.fft.fftfreq(N, dt) # Xのindexに対応する周波数のndarrayを取得
  f = f[0:N//2] # 前半のみ取得
  # 1000以上については無視！
  f = np.array([freq for freq in f if restrictionFunc(MIN, MAX, freq)])
  X = np.array([X[idx] for idx, freq in enumerate(f) if restrictionFunc(MIN, MAX, freq)])
  N = len(X)
  print('data length is {}'.format(N))
  assert N == len(f)

  max_idxx = np.argmax(X)
  f_max = f[max_idxx]
  result.freq_array.append(f_max)
  print(f'f_max: {f_max}')
  # データをプロット
  fig, (ax01, ax02) = plt.subplots(nrows=2, figsize=(6, 8))
  plt.subplots_adjust(wspace=0.0, hspace=0.6)

  ax02.set_xlim(MIN, MAX)
  ax02.set_xlabel('frequency (Hz)')

  ax02.set_ylabel('|X|/N')
  ax02.plot(f, X / N) # 振幅スペクトル

  plt.show()

main('output.wav')
