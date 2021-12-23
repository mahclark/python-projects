import win32gui
import win32ui
from ctypes import windll
from PIL import Image

def get_lonely_screen_id():
    lonely_screen_ids = []
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            if win32gui.GetWindowText(hwnd).find("LonelyScreen") != -1:
                lonely_screen_ids.append(hwnd)

    win32gui.EnumWindows(winEnumHandler, None)

    biggest = None
    area = -1
    for hwnd in lonely_screen_ids:
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y

        if w*h > area:
            area = w*h
            biggest = hwnd

    return biggest

def get_colour_at(x, y, hwnd):
    dc = win32gui.GetWindowDC(hwnd)
    col = int(win32gui.GetPixel(dc, x, y))
    return (col & 0xff), ((col >> 8) & 0xff), ((col >> 16) & 0xff)

def set_colour_at(x, y, hwnd, col):
    dc = win32gui.GetWindowDC(hwnd)
    col = int(win32gui.SetPixel(dc, x, y, (col[0]<<16) + (col[1]<<8) + col[2]))
    return (col & 0xff), ((col >> 8) & 0xff), ((col >> 16) & 0xff)

def get_phone_rect(hwnd):

    x = None
    y = None
    width = None
    height = None

    lonely_rect = win32gui.GetWindowRect(hwnd)
    s_width = lonely_rect[2] - lonely_rect[0]
    s_height = lonely_rect[3] - lonely_rect[1]
    middle = int(s_width/2)

    print(middle)

    adjacent_black = 0
    for i_y in range(10,s_height):
        if get_colour_at(middle, i_y, hwnd) == (0,0,0):
            adjacent_black += 1
        elif adjacent_black >= 16:
            y = i_y
            break
        else:
            adjacent_black = 0

    adjacent_black = 0
    for i_y in range(s_height - 1, 0, -1):
        if get_colour_at(middle, i_y, hwnd) == (0,0,0):
            adjacent_black += 1
        elif adjacent_black >= 9:
            height = i_y + 1 - y
            break
        else:
            adjacent_black = 0

    for i_x in range(8, s_width):
        if get_colour_at(i_x, y, hwnd) != (0,0,0):
            x = i_x
            break

    for i_x in range(x, s_width):
        # print(i_x, '\t', get_colour_at(i_x, y, hwnd))
        if get_colour_at(i_x, y, hwnd) == (0,0,0) or i_x == s_width - x:
            width = i_x - x
            break

    rect = (x, y, width, height)
    print(rect)
    assert None not in rect
    return rect

def save_img(hwnd):
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    # Change the line below depending on whether you want the whole window
    # or just the client area. 
    #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    print(result)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        #PrintWindow Succeeded
        im.save("test.png")