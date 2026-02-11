#!/usr/bin/env python3
# coding=utf-8
# i3blocks Spotify状态脚本：支持点击切歌/暂停，异常兜底输出，无语法错误

import dbus
import os
import sys

def main():
    try:
        # 连接DBus会话总线，获取Spotify对象
        bus = dbus.SessionBus()
        spotify = bus.get_object(
            "org.mpris.MediaPlayer2.spotify",
            "/org/mpris/MediaPlayer2"
        )

        # 处理i3blocks鼠标点击事件（1=上一曲，2=播放/暂停，3=下一曲）
        block_button = os.environ.get('BLOCK_BUTTON')
        if block_button:
            control_iface = dbus.Interface(spotify, 'org.mpris.MediaPlayer2.Player')
            if block_button == '1':
                control_iface.Previous()
            elif block_button == '2':
                control_iface.PlayPause()
            elif block_button == '3':
                control_iface.Next()

        # 获取Spotify播放元数据（歌手、标题）
        props_iface = dbus.Interface(spotify, 'org.freedesktop.DBus.Properties')
        metadata = props_iface.Get('org.mpris.MediaPlayer2.Player', 'Metadata')

        # 容错处理：判断关键字段是否存在，避免KeyError/IndexError
        artists = metadata.get('xesam:artist', [])
        title = metadata.get('xesam:title', '未知标题')
        # 取第一个歌手，无歌手则显示“未知歌手”
        artist = artists[0] if artists else '未知歌手'

        # 拼接输出（i3blocks标准输出），确保UTF-8编码
        output = f"{artist} - {title}"
        print(output.encode('utf-8').decode('utf-8'))

    except dbus.exceptions.DBusException:
        # 兜底输出：Spotify未启动/未连接时，显示提示文本
        print("Spotify 未运行 ")
    except (KeyError, IndexError):
        # 兜底输出：元数据缺失字段/歌手列表为空时
        print("无播放内容 ")
    except Exception as e:
        # 捕获所有其他异常，避免脚本终止（可选：打印错误信息用于调试）
        # print(f"Error: {str(e)}")
        print("播放状态未知 ")
    finally:
        # 确保脚本正常退出，无残留进程
        sys.exit(0)

if __name__ == "__main__":
    main()
