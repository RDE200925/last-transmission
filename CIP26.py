# =========================================
# LAST TRANSMISSION : EVOLVED EDITION
# =========================================

import customtkinter as ctk
import random
import time

# =========================================
# SETTINGS
# =========================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# =========================================
# WINDOW
# =========================================

app = ctk.CTk()
app.geometry("1500x850")
app.title("LAST TRANSMISSION")

# =========================================
# GAME DATA
# =========================================

ship = {
    "oxygen": 100,
    "power": 100,
    "hull": 100,
    "food": 100,
    "sanity": 100
}

crew = [
    {"name": "LENA", "trait": "Paranoid"},
    {"name": "ATLAS", "trait": "Loyal"},
    {"name": "KIRO", "trait": "Aggressive"},
    {"name": "MIRA", "trait": "Engineer"}
]

DAY = 1
GAME_OVER = False
alien_presence = 0
ai_instability = 0

# =========================================
# EVENTS
# =========================================

events = [
    ("SOLAR STORM DETECTED", "power", -15),
    ("OXYGEN LEAK DETECTED", "oxygen", -18),
    ("HULL BREACH DETECTED", "hull", -14),
    ("EMERGENCY FOOD CACHE FOUND", "food", 18),
    ("STRANGE SIGNAL DETECTED", "sanity", -10),
]

rare_events = [
    "DISTRESS SIGNAL RECEIVED FROM YOUR OWN SHIP",
    "UNKNOWN FIGURE SEEN ON SECURITY CAMERAS",
    "AI ACCESSED LOCKED SHIP SECTIONS",
    "SOMEONE WHISPERED THROUGH THE INTERCOM"
]

# =========================================
# FUNCTIONS
# =========================================

def add_log(message, color="#00ff88"):

    timestamp = time.strftime("%H:%M:%S")

    terminal.configure(state="normal")

    terminal.insert(
        "end",
        f"[{timestamp}] {message}\n",
        color
    )

    terminal.tag_config(color, foreground=color)

    terminal.see("end")

    terminal.configure(state="disabled")


def update_bars():

    oxygen_bar.set(ship["oxygen"] / 100)
    power_bar.set(ship["power"] / 100)
    hull_bar.set(ship["hull"] / 100)
    food_bar.set(ship["food"] / 100)
    sanity_bar.set(ship["sanity"] / 100)

    oxygen_label.configure(text=f"OXYGEN {ship['oxygen']}%")
    power_label.configure(text=f"POWER {ship['power']}%")
    hull_label.configure(text=f"HULL {ship['hull']}%")
    food_label.configure(text=f"FOOD {ship['food']}%")
    sanity_label.configure(text=f"SANITY {ship['sanity']}%")

    day_label.configure(text=f"DAY {DAY}")


def random_crew_event():

    member = random.choice(crew)

    events = [
        f"{member['name']} reports movement in ventilation shafts.",
        f"{member['name']} refuses to sleep.",
        f"{member['name']} claims the AI is watching.",
        f"{member['name']} found damaged equipment."
    ]

    add_log(random.choice(events), "#ffcc00")


def trigger_event():

    global alien_presence
    global ai_instability

    event = random.choice(events)

    message, stat, value = event

    ship[stat] += value

    if ship[stat] > 100:
        ship[stat] = 100

    if ship[stat] < 0:
        ship[stat] = 0

    add_log(f"WARNING: {message}", "#ff4444")

    # hidden progression systems
    alien_presence += random.randint(0, 2)
    ai_instability += random.randint(0, 2)

    # escalating horror events

    if alien_presence > 5:

        add_log(
            "MOTION DETECTED IN UNREGISTERED SHIP SECTION",
            "#ff00ff"
        )

    if alien_presence > 10:

        add_log(
            "CREW REPORT SCREAMS HEARD INSIDE WALLS",
            "#ff00ff"
        )

    if ai_instability > 7:

        add_log(
            "AI RESPONSE DELAY DETECTED",
            "#00ccff"
        )

    if ai_instability > 12:

        add_log(
            "AI: HUMAN SURVIVAL STATISTICALLY UNLIKELY",
            "#00ccff"
        )

    # rare event chance

    if random.randint(1, 100) < 8:

        add_log(
            random.choice(rare_events),
            "#ff00ff"
        )

    random_crew_event()


def next_day():

    global DAY

    if GAME_OVER:
        return

    DAY += 1

    ship["oxygen"] -= random.randint(5, 10)
    ship["power"] -= random.randint(4, 8)
    ship["food"] -= random.randint(3, 7)
    ship["sanity"] -= random.randint(2, 6)

    trigger_event()

    update_bars()

    check_game_over()


def repair():

    system = random.choice([
        "oxygen",
        "power",
        "hull"
    ])

    amount = random.randint(10, 20)

    ship[system] += amount

    if ship[system] > 100:
        ship[system] = 100

    add_log(
        f"SYSTEM REPAIR SUCCESSFUL → {system.upper()} +{amount}%",
        "#00ccff"
    )

    update_bars()


def search_ship():

    locations = [
        "ENGINEERING",
        "MEDBAY",
        "VENTILATION",
        "CARGO HOLD",
        "REACTOR CORE"
    ]

    location = random.choice(locations)

    add_log(f"SEARCHING {location}...", "#aaaaaa")

    result = random.choice([
        "food",
        "oxygen",
        "power",
        "nothing",
        "strange"
    ])

    if result == "nothing":

        add_log(
            "NOTHING USEFUL FOUND",
            "#aaaaaa"
        )

    elif result == "strange":

        add_log(
            "UNKNOWN BIOLOGICAL MATERIAL DISCOVERED",
            "#ff00ff"
        )

        ship["sanity"] -= 8

    else:

        amount = random.randint(10, 20)

        ship[result] += amount

        if ship[result] > 100:
            ship[result] = 100

        add_log(
            f"SUPPLIES RECOVERED → {result.upper()} +{amount}%",
            "#00ff88"
        )

    update_bars()


def rest():

    ship["sanity"] += 12

    if ship["sanity"] > 100:
        ship["sanity"] = 100

    add_log(
        "CREW ENTERED TEMPORARY REST CYCLE",
        "#22c55e"
    )

    update_bars()


def distress_signal():

    global GAME_OVER

    add_log(
        "TRANSMITTING DISTRESS SIGNAL...",
        "#ffcc00"
    )

    chance = random.randint(1, 100)

    if chance > 92:

        add_log(
            "INCOMING TRANSMISSION DETECTED",
            "#00ff88"
        )

        add_log(
            "RESCUE SHIP APPROACHING",
            "#00ff88"
        )

        title.configure(
            text="RESCUE CONFIRMED",
            text_color="#00ff88"
        )

        GAME_OVER = True

    else:

        add_log(
            "NO RESPONSE RECEIVED",
            "#ff4444"
        )

        ship["power"] -= 10

        update_bars()

        check_game_over()


def check_game_over():

    global GAME_OVER

    for stat in ship:

        if ship[stat] <= 0:

            GAME_OVER = True

            title.configure(
                text="SIGNAL LOST",
                text_color="#ff3333"
            )

            add_log(
                f"CRITICAL FAILURE → {stat.upper()} DEPLETED",
                "#ff0000"
            )

            add_log(
                "THE SHIP VANISHES INTO THE VOID",
                "#ff0000"
            )

            break

# =========================================
# MAIN UI
# =========================================

main = ctk.CTkFrame(app, fg_color="#050816")
main.pack(fill="both", expand=True)

# =========================================
# LEFT PANEL
# =========================================

left = ctk.CTkFrame(
    main,
    width=320,
    fg_color="#0f172a",
    corner_radius=0
)

left.pack(side="left", fill="y")

# =========================================
# TITLE
# =========================================

title = ctk.CTkLabel(
    left,
    text="LAST\nTRANSMISSION",
    font=("Arial Black", 32),
    text_color="#00e5ff"
)

title.pack(pady=(30, 10))

subtitle = ctk.CTkLabel(
    left,
    text="SURVIVE THE UNKNOWN",
    font=("Consolas", 14),
    text_color="#94a3b8"
)

subtitle.pack()

# =========================================
# DAY LABEL
# =========================================

day_label = ctk.CTkLabel(
    left,
    text="DAY 1",
    font=("Arial Black", 28),
    text_color="#facc15"
)

day_label.pack(pady=25)

# =========================================
# STATUS BARS
# =========================================

status_frame = ctk.CTkFrame(
    left,
    fg_color="#111827"
)

status_frame.pack(
    padx=15,
    pady=10,
    fill="x"
)

def create_bar(name, color):

    label = ctk.CTkLabel(
        status_frame,
        text=name,
        font=("Consolas", 14, "bold")
    )

    label.pack(anchor="w", padx=10, pady=(8, 2))

    bar = ctk.CTkProgressBar(
        status_frame,
        progress_color=color,
        height=16
    )

    bar.set(1)

    bar.pack(fill="x", padx=10, pady=(0, 8))

    return label, bar

oxygen_label, oxygen_bar = create_bar("OXYGEN", "#38bdf8")
power_label, power_bar = create_bar("POWER", "#facc15")
hull_label, hull_bar = create_bar("HULL", "#ef4444")
food_label, food_bar = create_bar("FOOD", "#f97316")
sanity_label, sanity_bar = create_bar("SANITY", "#ff00ff")

# =========================================
# RIGHT PANEL
# =========================================

right = ctk.CTkFrame(
    main,
    fg_color="#020617",
    corner_radius=0
)

right.pack(side="right", fill="both", expand=True)

# =========================================
# TERMINAL HEADER
# =========================================

header = ctk.CTkFrame(
    right,
    height=60,
    fg_color="#111827"
)

header.pack(fill="x", padx=20, pady=(20, 0))

header_label = ctk.CTkLabel(
    header,
    text="SHIP TERMINAL // EREBUS-7",
    font=("Consolas", 20, "bold"),
    text_color="#00ff88"
)

header_label.pack(side="left", padx=20, pady=15)

# =========================================
# TERMINAL
# =========================================

terminal_frame = ctk.CTkFrame(
    right,
    fg_color="#000000"
)

terminal_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

terminal = ctk.CTkTextbox(
    terminal_frame,
    fg_color="#000000",
    text_color="#00ff88",
    font=("Consolas", 16)
)

terminal.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

terminal.configure(state="disabled")

# =========================================
# TASKBAR
# =========================================

taskbar = ctk.CTkFrame(
    app,
    height=90,
    fg_color="#0b1120",
    corner_radius=0
)

taskbar.pack(side="bottom", fill="x")

def make_button(text, color, hover, command):

    btn = ctk.CTkButton(
        taskbar,
        text=text,
        width=220,
        height=55,
        fg_color=color,
        hover_color=hover,
        corner_radius=18,
        font=("Arial Bold", 15),
        command=command
    )

    btn.pack(side="left", padx=12, pady=15)

# =========================================
# BUTTONS
# =========================================

make_button(
    "REPAIR",
    "#0891b2",
    "#0e7490",
    repair
)

make_button(
    "SEARCH",
    "#7c3aed",
    "#6d28d9",
    search_ship
)

make_button(
    "REST",
    "#16a34a",
    "#15803d",
    rest
)

make_button(
    "DISTRESS SIGNAL",
    "#dc2626",
    "#b91c1c",
    distress_signal
)

make_button(
    "NEXT DAY",
    "#f59e0b",
    "#d97706",
    next_day
)

# =========================================
# STARTUP LOGS
# =========================================

startup = [
    "INITIALIZING SHIP SYSTEMS...",
    "CREW NETWORK OFFLINE",
    "BACKUP POWER ACTIVATED",
    "UNKNOWN SIGNAL DETECTED",
    "MISSION STATUS: SURVIVE"
]

for msg in startup:
    add_log(msg)

update_bars()

# =========================================
# RUN
# =========================================

app.mainloop()
