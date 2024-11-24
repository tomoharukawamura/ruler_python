import serial
import time as wait
import re
import result
import analize
import record

# ステップ数を取得する
# serialに通信を送る。叩いてないときはNone、叩いたときは数値が返ってくる、調律終了時にfinish_loopが返ってくる
# 録音準備が整ったらardinoに合図を送る
def main():
  ser = serial.Serial('COM4', 9600)
  ser.readline()

  voice_num = 0
  while True:
    message = ser.readline().replace(b'\r\n', b'')
    if message == b'finish_tuning':
      break
    if message != b'None':
      target_step = int(messge)
      result.result_array.append(target_step)
      # ソレノイドを叩いていいよのサイン
      ser.write('start_to_record!'.encode())
      record.main('./output{}.wav'.format(voice_num))
      voice_num += 1
  result.print_array()
  # 解析
  for i in range(voice_num):
    analize.main('./output{}.wav'.format(i))
  print(result.freq_array)

main()