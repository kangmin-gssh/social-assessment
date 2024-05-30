import os
import re
import psutil
import subprocess
import flet as ft
from flet_timer.flet_timer import Timer

# Constantizing power modes
PERFORMANCE = 'performance'
BALANCED = 'balanced'
POWER_SAVER = 'power-saver'

DEFAULT = 'default' # user setting

trigger_process_names = {
    PERFORMANCE: [],
    BALANCED: [],
    POWER_SAVER: []
}

power_mode = DEFAULT
power_mode_prev = power_mode
trigger_processes = {PERFORMANCE: [], BALANCED: [], POWER_SAVER: []}

brightness = int(''.join(re.findall(r'[0-9]', subprocess.run('gdbus call --session --dest org.gnome.SettingsDaemon.Power --object-path /org/gnome/SettingsDaemon/Power --method org.freedesktop.DBus.Properties.Get org.gnome.SettingsDaemon.Power.Screen Brightness', stdout=subprocess.PIPE, shell=True, text=True).stdout.strip())))

def notify(mode, trigger):
    os.system('notify-send %s %s' % (mode, trigger))

def change_power_mode():
    global power_mode, power_mode_prev, trigger_processes
    for key in trigger_processes.keys(): trigger_processes[key].clear()
    
    for proc in psutil.process_iter():
        if proc.name() in trigger_process_names[PERFORMANCE]:
            power_mode = PERFORMANCE
            trigger_processes[PERFORMANCE].append(proc.name())
            continue

        elif proc.name() in trigger_process_names[BALANCED] and power_mode != PERFORMANCE:
            power_mode = BALANCED
            trigger_processes[BALANCED].append(proc.name())
            continue

        elif proc.name() in trigger_process_names[POWER_SAVER] and power_mode not in [PERFORMANCE, BALANCED]:
            power_mode = POWER_SAVER
            trigger_processes[POWER_SAVER].append(proc.name())
            continue
    print(trigger_processes)
    print(trigger_process_names)

    if not any(list(trigger_processes.values())): power_mode = DEFAULT

    os.system('powerprofilesctl set %s' % ('balanced' if power_mode == DEFAULT else power_mode))
    if power_mode != power_mode_prev:
        msg = [None, None]
        if power_mode == DEFAULT:
            msg = ['"전원 모드가 균형으로 변경되었습니다."', '"트리거 프로그램이 없습니다."']
        elif power_mode == PERFORMANCE:
            msg[0] = '"전원 모드가 성능으로 변경되었습니다."'
        elif power_mode == BALANCED:
            msg[0] = '"전원 모드가 균형으로 변경되었습니다."',
        elif power_mode == POWER_SAVER:
            msg[0] = '"전원 모드가 전기 절약으로 변경되었습니다."'

        if power_mode != DEFAULT:
            msg[1] = f'"다음 프로그램에 의해: {trigger_processes[power_mode][0]}"'
            if len(trigger_processes[power_mode]) > 1:
                msg[1] = msg[1][:-1] + f' 외 {len(trigger_processes[power_mode])-1}개"'

        print(msg)
        notify(msg[0], msg[1])

    power_mode_prev = power_mode

def process_names(raw: str):
    return [word.strip() for word in raw.split(',')]

def main(page: ft.Page):
    page.window_width = 800
    page.window_height = 600
    page.title = 'Power Management Utilities'
    page.fonts = {
        'Regular': './assets/Pretendard-Regular.ttf',
        'Medium': './assets/Pretendard-Medium.ttf',
        'Semibold': './assets/Pretendard-Semibold.ttf',
        'Mono': './assets/UbuntuMono-R.ttf'
    }
    page.theme = ft.Theme(font_family='Regular')

    normal_text_style = ft.TextStyle(font_family='Regular', size=15)
    highlight_text_style = ft.TextStyle(font_family='Medium', size=17, weight=ft.FontWeight.W_500)
    mono_text_style = ft.TextStyle(font_family='Mono', size=15)

    performance_tf = ft.TextField(
        text_style=mono_text_style, border=ft.InputBorder.OUTLINE,
        width=300, height=45, content_padding=ft.padding.only(left=5))
    balanced_tf = ft.TextField(
        text_style=mono_text_style, border=ft.InputBorder.OUTLINE,
        width=300, height=45, content_padding=ft.padding.only(left=5))
    save_tf = ft.TextField(
        text_style=mono_text_style, border=ft.InputBorder.OUTLINE,
        width=300, height=45, content_padding=ft.padding.only(left=5))
    
    def refresh_brightness(e):
        global brightness
        nonlocal slider, slider_label
        print(slider.value)
        brightness = int(slider.value)
        slider_label.value = f'{brightness}%'
        page.update()

        # only for GNOME; gdbus dependency
        os.system(f'gdbus call --session --dest org.gnome.SettingsDaemon.Power --object-path /org/gnome/SettingsDaemon/Power --method org.freedesktop.DBus.Properties.Set org.gnome.SettingsDaemon.Power.Screen Brightness "<int32 {brightness}>"')

    slider = ft.Slider(value=brightness, min=0, max=100, width=300, on_change=refresh_brightness)
    slider_label = ft.Text(f'{slider.value}%')
    
    def change_trigger(e: ft.ControlEvent):
        global trigger_process_names
        trigger_process_names[PERFORMANCE] = process_names(performance_tf.value)
        trigger_process_names[BALANCED] = process_names(balanced_tf.value)
        trigger_process_names[POWER_SAVER] = process_names(save_tf.value)


    page.add(
        Timer('timer', interval_s=2, callback=change_power_mode),
        ft.Text('다음 프로그램 실행 중 전력 모드 조정', style=highlight_text_style),
        ft.Text('각 프로그램의 프로세스 이름을 콤마(,)로 구분하여 입력해 주시기 바랍니다.'),
        ft.Text('성능', style=normal_text_style),
        performance_tf,
        ft.Text('균형', style=normal_text_style),
        balanced_tf,
        ft.Text('전기 절약', style=normal_text_style),
        save_tf,
        ft.TextButton('적용', on_click=change_trigger),

        ft.Text('밝기 조절', style=highlight_text_style),
        slider,
        ft.Container(padding=ft.padding.only(left=10), content=slider_label),
    )

ft.app(main)