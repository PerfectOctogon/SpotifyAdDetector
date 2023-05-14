import selenium.webdriver as webdriver
import time
from tkinter import *

root = Tk()
root.title("Spotify Bot")
root.iconbitmap("Ad-DetectorIcon.ico")


def initiate():
    start_program()


credentials = open("credentials.txt", 'r')
user_info = credentials.readlines()
credentials.close()
username_asker = Label(root, text = "Please enter your Spotify username")
username_field = Entry(root)
password_asker = Label(root, text = "Please enter your Spotify password")
password_field = Entry(root)

if len(user_info) == 2:
    username_field.insert(0, str(user_info[0]))
    password_field.insert(0, str(user_info[1]))

spotify_login_button = Button(root, text = "Login", command = initiate)

username_asker.grid(row = 0, column = 0)
username_field.grid(row = 1, column = 0)
password_asker.grid(row = 2, column = 0)
password_field.grid(row = 3, column = 0)
spotify_login_button.grid(row = 4, column = 0)


path = r"ChromeDriver\\chromedriver.exe"
driver = webdriver.Chrome(executable_path=path)
driver.get('https://accounts.spotify.com/en/login/?continue=https:%2F%2Fopen.spotify.com%2F%3Fl2l%3D1&_ga=2.245439821.855872034.1623341914-1592272900.1623341914')
driver.set_window_size(780, 730)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
length = len(driver.window_handles)


def login():
    user_name = driver.find_element_by_xpath('//*[@id="login-username"]')
    user_name.send_keys(username_field.get())
    password = driver.find_element_by_xpath('//*[@id="login-password"]')
    password.send_keys(password_field.get())
    next_button = driver.find_element_by_xpath('//*[@id="login-button"]')
    next_button.click()


def update_credentials():
    credentials_updater = open("credentials.txt", 'w')
    credentials_updater.writelines(username_field.get())
    credentials_updater.writelines(password_field.get())
    credentials_updater.close()


def destroy_tkinter_login_screen():
    username_asker.destroy()
    username_field.destroy()
    password_asker.destroy()
    password_field.destroy()
    spotify_login_button.destroy()


def start_program():

    login()

    update_credentials()

    destroy_tkinter_login_screen()

    continueButton.pack()


def clicked_next():
    driver.implicitly_wait(10)
    next_button = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/div[2]/button[1]')
    next_button.click()


def click_previous():
    driver.implicitly_wait(10)
    previous_button = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/div[1]/button[2]')
    previous_button.click()


def play_pause():
    driver.implicitly_wait(10)
    play_pause_btn = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/button')
    play_pause_btn.click()


def hide_or_show_spotify_chrome_window():
    print()
    if driver.get_window_position().get('x') == 1080:
        driver.set_window_position(screen_height/2, screen_width/2)
    else:
        driver.set_window_position(screen_height, screen_width * 2)


def create_music_player():
    # GUI buttons :)
    play_next_button = Button(root, text="Play next", command=clicked_next)
    play_previous_button = Button(root, text="Play previous", command=click_previous)
    play_pause_button = Button(root, text="Play/Pause", command=play_pause)
    show_chrome_button = Button(root, text="Show/ Hide Chrome Window", command=hide_or_show_spotify_chrome_window)
    play_next_button.grid(row=3, column=2)
    play_previous_button.grid(row=3, column=0)
    play_pause_button.grid(row=3, column=1)
    show_chrome_button.grid(row=4, column=1)


def skip_ad(previous_song):
    last_played = previous_song
    driver.implicitly_wait(10)
    driver.refresh()
    print("Last played song : " + last_played)
    play_this = last_played.replace("•", "by")
    play_this = "Play " + play_this
    print(play_this)
    time.sleep(10)
    driver.implicitly_wait(10)
    play_this = driver.find_element_by_css_selector("[aria-label='{}']".format(play_this))
    print(play_this)
    driver.execute_script("arguments[0].click();", play_this)
    driver.implicitly_wait(10)
    next_button = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/div[2]/button[1]')
    time.sleep(1)
    next_button.click()


def ads_watcher():

    ads_skipped = 0
    continueButton.destroy()

    text_label = Label(root, text="Looking for ads...")
    text_label1 = Label(root, text="Now Playing: ")
    text_label.grid(row=1, column=1)
    text_label1.grid(row=2, column=1)

    create_music_player()

    last_song = ""

    while True:
        for i in range(length):
            tab_name = driver.title
            if tab_name == "Spotify – Advertisement":

                ads_skipped += 1
                text_label.destroy()
                text_label = Label(root, text="Ads skipped : " + str(ads_skipped))
                text_label.grid(row = 1, column = 1)

                skip_ad(last_song)

            else:

                last_song = tab_name
                text_label1.destroy()
                text_label1 = Label(root, text = last_song[0:15] + "...")
                text_label1.grid(row = 2, column = 1)

            driver.implicitly_wait(10)
            driver.switch_to.window(driver.window_handles[i])
            root.update()


continueButton = Button(root, text = "Click after opening a playlist", command = ads_watcher)
root.mainloop()
