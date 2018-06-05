import WeatherInfo
import time
import pygame

Yellow = (255, 255, 0)
Red = (255, 0, 0)
LightBlue = (190, 190, 255)
Green = (0, 255, 0)
Black = (0, 0, 0)
White = (255, 255, 255)

screenWidth = 480
screenHeight = 320
fill = 1
loop = 0
last_ip = ip = ''
should_request = False
weather_data = None

move = screenWidth

pygame.init()
# window = pygame.display.set_mode((screenWidth, screenHeight))  # 不全屏

window = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)  # 全屏


def draw_line(x0, y0, x1, y1):
    pygame.draw.line(window, pygame.Color(255, 255, 255), (x0, y0), (x1, y1), fill)
    return


def draw_frame():
    draw_line(0, 50, screenWidth, 50)
    draw_line(0, 160, screenWidth, 160)
    draw_line(0, 290, screenWidth, 290)
    draw_line(240, 50, 240, 160)
    draw_line(120, 160, 120, 290)
    draw_line(240, 160, 240, 290)
    draw_line(360, 160, 360, 290)


def draw_text(text, x, y, size):
    size = int(size)
    font = pygame.font.Font('gkai00mp.ttf', size, bold=1)
    text_surface = font.render(text, 1, pygame.Color(255, 255, 255))
    window.blit(text_surface, (x, y))
    return


def draw_weather_icon(image_num, x0, y0):
    image_path = "pictures/" + image_num + ".png"
    background = pygame.image.load(image_path)
    background.convert_alpha()
    window.blit(background, (x0, y0))
    return


def update_time():
    local_date = time.localtime()
    cur_time = time.strftime("%H:%M:%S", local_date)  # 时间
    date = time.strftime("%Y-%m-%d", local_date)  # 日期
    week = time.strftime("%A", local_date)  # 星期
    draw_text(cur_time, 0, 2.5, 50)
    draw_text(date, 220, 2.5, 25)
    draw_text(week, 220, 22.5, 25)


def update_weather():
    result = None
    json_data = WeatherInfo.weather_info()
    print(json_data)

    if json_data is None or json_data['status'] != '0':
        print("error")
    else:
        result = json_data['result']
        print(result.get("updatetime"))

    return result


def draw_weather(data, move_step):
    # 获取当前天气状况
    city = data.get('city')
    weather = data.get('weather')
    temp = data.get('temp')
    temp_high = data.get('temphigh')
    temp_low = data.get('templow')
    img_num = data.get('img')
    humidity = data.get('humidity')
    pressure = data.get('pressure')
    wind_speed = data.get('windspeed')
    wind_direct = data.get('winddirect')
    wind_power = data.get('windpower')
    update_time = data.get('updatetime')
    aqi = data.get('aqi')
    friendly_info = data.get('index')

    # 获取今天，明天，后天，大后天天气
    daily = data.get('daily')
    day_one = daily[1]  # 今天
    day_two = daily[2]  # 明天
    day_three = daily[3]  # 后天
    day_four = daily[4]  # 大后天

    draw_text(city, 370, 2.5, 46)
    draw_weather_icon(data.get('img'), 30, 65)
    draw_text(weather, 35, 110, 26)

    draw_text(temp + "℃", 115, 58, 36)
    draw_text(temp_low + "℃~" + temp_high + "℃", 104, 100, 22)
    draw_text("风速：" + wind_power, 100, 125, 22)
    draw_text("紫外线：" + friendly_info[2].get('ivalue'), 270, 75, 32)
    draw_text("空气质量：" + aqi.get('quality'), 280, 125, 22)

    draw_text(day_one.get('date'), 10, 175, 20)
    draw_text(day_two.get('date'), 130, 175, 20)
    draw_text(day_three.get('date'), 250, 175, 20)
    draw_text(day_four.get('date'), 370, 175, 20)
    draw_weather_icon(day_one.get('day').get('img'), 15, 205)
    draw_weather_icon(day_two.get('day').get('img'), 135, 205)
    draw_weather_icon(day_three.get('day').get('img'), 255, 205)
    draw_weather_icon(day_four.get('day').get('img'), 375, 205)

    draw_text(day_one.get('day').get('weather'), 60, 215, 20)
    draw_text(day_one.get('night').get('templow') + "~" + day_one.get('day').get('temphigh') + "℃",
              22, 245, 22)
    draw_text(day_two.get('day').get('weather'), 180, 215, 20)
    draw_text(day_two.get('night').get('templow') + "~" + day_two.get('day').get('temphigh') + "℃",
              142, 245, 22)
    draw_text(day_three.get('day').get('weather'), 300, 215, 20)
    draw_text(day_three.get('night').get('templow') + "~" + day_three.get('day').get('temphigh') + "℃",
              262, 245, 22)
    draw_text(day_four.get('day').get('weather'), 420, 215, 20)
    draw_text(day_four.get('night').get('templow') + "~" + day_four.get('day').get('temphigh') + "℃",
              382, 245, 22)

    draw_text(friendly_info[2].get('detail'), move_step, 295, 20)


if __name__ == '__main__':

    while True:

        window.fill(pygame.Color(0, 0, 0))
        draw_frame()
        update_time()

        if loop % 10800 == 0:
            weather_data = update_weather()
            loop += 1

        if move <= -400:
            move = screenWidth
        else:
            move = move - 1

        draw_weather(weather_data, move)

        # time.sleep(1 / 60)
        pygame.display.update()

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         exit()
