import numpy as np
import cv2
from matplotlib import pyplot as plt
 
# 画像から輪郭を検出する関数
def contours(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                  # グレースケール化
    ret, img_binary = cv2.threshold(img_gray,                         # 二値化
                                    60, 255,                          # 二値化のための閾値60(調整要)
                                    cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(img_binary,                # 輪郭検出
                                           cv2.RETR_EXTERNAL,         # 外側の輪郭のみ抽出
                                           cv2.CHAIN_APPROX_SIMPLE)
    contours = np.vstack(contours)                                     # 輪郭情報をndarrayに変換
    x = np.mean(contours[:, 0, 0])                                  # 輪郭のx方向平均値を算出
    y = np.mean(contours[:, 0, 1])                                  # 輪郭のy方向平均値を算出
    return x, y
 
movie = cv2.VideoCapture('testmovie1.avi')                                 # 動画ファイルの読み込み
 
# 動画ファイル保存用の設定
fps = int(movie.get(cv2.CAP_PROP_FPS))                                # 動画のFPSを取得
w = int(movie.get(cv2.CAP_PROP_FRAME_WIDTH))                          # 動画の横幅を取得
h = int(movie.get(cv2.CAP_PROP_FRAME_HEIGHT))                         # 動画の縦幅を取得
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')                   # 動画保存時のfourcc設定（mp4用）
video = cv2.VideoWriter('video_out2.mp4', fourcc, fps, (w, h), True)   # 動画の仕様（ファイル名、fourcc, FPS, サイズ, カラー）
 
# ファイルからフレームを1枚ずつ取得して動画処理後に保存する
x_list = []
y_list = []
while True:
    ret, frame = movie.read()                                         # フレームを取得
 
    # フレームが取得できない場合はループを抜ける
    if not ret:
        break
 
    x, y = contours(frame)                                            # 輪郭検出から物体中心を算出
 
    frame = cv2.circle(frame, (int(x), int(y)), 30, (0, 255, 0), 3)   # 検出した位置にサークル描画
 
    video.write(frame)  # 動画を保存する
    x_list.append(x)
    y_list.append(y)
 
# 動画オブジェクト解放
movie.release()