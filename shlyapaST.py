from pibody import Button, Buzzer, LEDTower, display
from time import sleep
import random

button = Button("A")
buzzer = Buzzer("D")
tower = LEDTower()

TOTAL_STUDENTS = 12
MAX_PER_TEAM = 3

TEAM_COLOR = {
    1: (255, 0, 0),
    2: (255, 128, 0),
    3: (0, 0, 255),
    4: (0, 255, 0)
}

TEAM_NAME = {
    1: "Upside Down",
    2: "Starcourt Mall",
    3: "Hawkins Lab",
    4: "The Gate"
}

team_count = {1: 0, 2: 0, 3: 0, 4: 0}
assigned = 0

def available_teams():
    return [team for team, count in team_count.items() if count < MAX_PER_TEAM]

def show_team(team):


    display.fill_rect(10, 32, 230, 48, 0)
    display.text("CHOSEN TEAM:", 10, 10, font=display.font_bold)
    r, g, b = TEAM_COLOR[team]
    display.text(TEAM_NAME[team], 10, 10 + 32, font=display.font_bold, fg=display.color(r, g, b))
    tower.fill((r, g, b))
    tower.write()
    buzzer.make_sound(1200, 0.5, 0.1)

def show_assigned():
    text = str(assigned) + " of " + str(TOTAL_STUDENTS)
    display.text(text, 10, 300)

def show_all_teams():
    for i in range(4):
        r, g, b = TEAM_COLOR[i + 1]
        text = TEAM_NAME[i + 1] + " " + str(team_count[i + 1]) + " of " + (str(MAX_PER_TEAM))
        display.text(text, 240 - len(text) * 8, 310 - (16 * 4) + i * 16, fg=display.color(r, g, b))

def choose_team():
    global assigned
    global team_count
    team = random.choice(available_teams())
    team_count[team] += 1
    assigned += 1
    return team

show_all_teams()
show_assigned()
while True:
    if assigned >= TOTAL_STUDENTS:
        display.fill(0)
        display.text("ALL TEAMS ARE", 10, 10, font=display.font_bold, fg=display.color(255, 0, 0))
        display.text("READY!", 10, 10 + 32, font=display.font_bold, fg=display.color(255, 0, 0))
        buzzer.beep()
        break

    if button.value():
        team = choose_team()
        while button.value():
            sleep(0.1)

        show_team(team)
        show_assigned()
        show_all_teams()

        sleep(1)