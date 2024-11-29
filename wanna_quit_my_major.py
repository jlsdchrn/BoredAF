from ics import Calendar
from datetime import datetime, timezone, timedelta
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Table
from rich.console import Group
from rich.text import Text
from rich.align import Align
import itertools
import shutil
import time
import sys
import os
from animated_gif import download_gif, extract_gif_frames, extract_frames_from_file
from random import randint

class Prompt:
    major_progress_bar: str = "[bold yellow]Complétion de l'arc CISD :[/bold yellow]"
    current_class_progress_bar: str = "[bold green]Progression du cours actuel :[/bold green]"
    current_class_prompt: str = "Cours actuel"
    time_left: str=  "Temps restant"
    last_class: str = "Dernier cours"
    no_class : str = "Pas cours actuellement"
    major_progress_bar_title: str = "Mission: survivre à la CISD"
    current_class_progress_bar_title: str = "Mission: ne pas m'endormir dans le cours actuel"
    detail_info_title: str = "Détails du cours"
    time_major_prompt : str = "Arc CISD"
    time_major : str = "Tu déjà perdu {} en CISD et il te reste encore {}!"

def extractCalendarData(ics_file):

    with open(ics_file, 'r') as file:
        calendar = Calendar(file.read())

    now = datetime.now(timezone.utc)
    remaining_time = timedelta()
    total_past_time = timedelta()
    current_class = None
    time_left_in_current_class = None
    last_class = None
    full_class_duration = None
    current_instance_index = None
    total_instances = None
    
    for event in sorted(calendar.events, key=lambda e: e.begin):
        event_duration = event.end - event.begin
        # If there is a class going on right now
        if event.begin <= now < event.end:
            # give the nomber of instances of the class and the current instance index
            class_instances = sorted([e for e in calendar.events if e.name == event.name], key=lambda e: e.begin)
            current_instance_index = class_instances.index(event) + 1
            total_instances = len(class_instances)

            # Update the current class and the time left in the class
            current_class = event.name
            time_left_in_current_class = event.end - now
            total_past_time += event_duration - time_left_in_current_class
            remaining_time += time_left_in_current_class
            full_class_duration = event.end - event.begin
        elif event.end <= now:
            total_past_time += event_duration
        elif event.end > now:
            remaining_time += event_duration
            last_class = event

    total_class_time = total_past_time + remaining_time

    progress_ratio = (
        total_past_time / total_class_time if total_class_time.total_seconds() > 0 else 0
    )    

    
    remaining_hours = int(remaining_time.total_seconds() // 3600)
    remaining_minutes = int((remaining_time.total_seconds() % 3600) // 60)
    past_hours = int(total_past_time.total_seconds() // 3600)
    past_minutes = int((total_past_time.total_seconds() % 3600) // 60)

    last_class_str = f"{last_class.name} on {last_class.begin.strftime('%Y-%m-%d %H:%M')} UTC" if last_class else Prompt.no_class

    return {
        'current_instance_index': current_instance_index,
        'total_instances': total_instances,
        "full_class_duration": full_class_duration,
        "time_left_in_current_class": time_left_in_current_class,
        "current_class": current_class,
        "progress_ratio": progress_ratio,
        "remaining_time": f"{remaining_hours}h {remaining_minutes}min",
        "past_time": f"{past_hours}h {past_minutes}min",
        "last_class": last_class_str,
    }

def render_ui(gif_frames, data, frame_index):
    # Major progress bar
    time_left_str = f"{data['time_left_in_current_class'].seconds // 3600}h {(data['time_left_in_current_class'].seconds % 3600) // 60}min" if data["current_class"] else ""
    
    current_class = data["current_class"] if data["current_class"] else Prompt.no_class
    current_class_duration = data["full_class_duration"].seconds if data["current_class"] else 100
    time_passed_in_current_class = data["full_class_duration"].seconds - data["time_left_in_current_class"].seconds if data["current_class"] else 0

    progress_bar = Progress(
        TextColumn(Prompt.major_progress_bar),
        BarColumn(),
        TextColumn("{task.percentage:>3.0f}%"),
    )

    # Progress bar for the current class
    current_class_progress = Progress(
        TextColumn(Prompt.current_class_progress_bar),
        BarColumn(),
        TextColumn("{task.percentage:>3.0f}%"),
    )

    progress_bar.add_task("", total=100, completed=data["progress_ratio"] * 100)
    current_class_progress.add_task("", total=current_class_duration, completed=time_passed_in_current_class)

    current_class_instance  = " | {}/{}".format(data["current_instance_index"],data["total_instances"])
    details_table = Table.grid(padding=1)
    details_table.add_column(justify="right", style="cyan", no_wrap=True)
    details_table.add_column(style="white")
    details_table.add_row(Prompt.current_class_prompt, current_class + current_class_instance)
    details_table.add_row(Prompt.time_left, time_left_str)
    details_table.add_row( Prompt.time_major_prompt, Prompt.time_major.format(data["past_time"], data["remaining_time"]))
    details_table.add_row(Prompt.last_class, data["last_class"])

    current_frame = gif_frames[frame_index % len(gif_frames)]

    # Combiner la barre de progression et les détails dans un seul groupe
    body = Group(
        Panel(progress_bar.get_renderable(), title=Prompt.major_progress_bar_title),
        Panel(current_class_progress.get_renderable(), title=Prompt.current_class_progress_bar_title),
        Panel(details_table, title=Prompt.detail_info_title, border_style="cyan"),
        Panel(Align.center(current_frame), title="GIF", border_style="green")
    )
    

    return body

gif_collection = {
    "among_us_twerk": "https://media1.tenor.com/m/jUMex_rdqPwAAAAd/among-us-twerk.gif",
    "nerd" : "https://media1.tenor.com/m/DuThn51FjPcAAAAd/nerd-emoji-nerd.gif",
    "mignon" : "https://media1.tenor.com/m/ILGqzVUwmMUAAAAd/minion-dance.gif",
    "simpson" : "https://media1.tenor.com/m/AcBSnelsh2cAAAAC/the-simpsons.gif",
    "spinning_cat" : "https://media1.tenor.com/m/EFDwfjT2GuQAAAAd/spinning-cat.gif"
}

def gif_from_collection():
        gif_list = list(gif_collection.keys())
        index = randint(0,len(gif_list)-1)
        name = gif_list[index]
        url = gif_collection[name]
        return name, url

if __name__ == "__main__":

    current_folder = os.path.dirname(os.path.abspath(__file__))
    gif_folder = current_folder+"/gif/"
    gif_list = []

    """
    If the user provides arguments, the script will use them
    """
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg == "-h" or arg == "--help":
                print("Usage: python3 wanna_quit_my_major.py [OPTIONS]")
                print("Options:")
                print("-h, --help : Display this help message")
                print("-ls, --list : List the gifs in the gif folder")
                print("-rm, --remove : Remove a gif from the gif folder. Type only the name of the gif without the extension")
                print("-def, --default : Choose a random gif from the collection")
                print("-u, --url : Specify the url of the gif")
                print("-n, --name : Specify the name of the gif")
                sys.exit()
            if arg == "-ls" or arg == "--list":
                if os.path.exists(gif_folder) and os.path.isdir(gif_folder):
                    print("List of gifs:")
                    for gif in os.listdir(gif_folder):
                        print(gif)
                sys.exit()
            if arg == "-rm" or arg == "--remove":
                file_name = sys.argv[sys.argv.index(arg) + 1]
                full_path = os.path.join(gif_folder, file_name)
                full_path += ".txt"
                if os.path.exists(full_path):
                    os.remove(full_path)
                else:
                    print("The gif does not exist")
                sys.exit()
            if arg == "-def" or arg == "--default":
                name,url = gif_from_collection()
            if arg == "-u" or arg == "--url":
                url = sys.argv[sys.argv.index(arg) + 1]
            if arg == "-n" or arg == "--name":
                name = sys.argv[sys.argv.index(arg) + 1]
    else:
        #If run without args, the script will choose a random gif from the already downloaded gifs
        if os.path.exists(gif_folder) and os.path.isdir(gif_folder):
            print("Scanning gif folder")
            print(os.listdir(gif_folder))
            for gif in os.listdir(gif_folder): 
                full_path = os.path.join(gif_folder, gif)
                if os.path.isfile(full_path):
                    # strip the file name from the extension 
                    gif_list.append(gif.split(".")[0])
        if gif_list != []:
            # Once the folder is scanned, we choose a random gif
            index = randint(0,len(gif_list)-1)
            name = gif_list[index]
            # no need for url since the gif is already downloaded
            url = ""
        else :
            #If the gif folder is empty, the script will download a gif from the internet
            name,url = gif_from_collection()
    
    save_path = gif_folder +name + ".txt"
    full_save_path = os.path.join(current_folder, save_path)

    if not os.path.exists(full_save_path):   
        # 1st step: Download the gif in a temp file
        gif_path= download_gif(url)

        # 2nd step: Extract the frames from the gif and save them in a txt file
        extract_gif_frames( gif_path, file_name=full_save_path)

    # 3rd step: Extract the frames from the txt file
    gif_frames = extract_frames_from_file(full_save_path)

    frame_index = 0

    # Enter the name of your iCalendar file
    ics_file_name = "ADECal.ics"

    current_folder = os.path.dirname(os.path.abspath(__file__))
    ics_file = os.path.join(current_folder, ics_file_name)
    
    # 4th step: Extract the data from the ics file
    data = extractCalendarData(ics_file)

    # 5th step: Render the UI
    console = Console()
    console.clear()
    frames = []
    # 6th step: Create a live object to update the UI
    with Live(render_ui(gif_frames, data, frame_index), refresh_per_second=20) as live:
        while True:
            # Avancer l'animation du GIF
            frame_index = (frame_index + 1) % len(gif_frames)
            live.update(render_ui(gif_frames, data, frame_index))

    
            if frame_index == 0:
                data = extractCalendarData(ics_file)  # Rafraîchir les données

            # Petite pause pour limiter la charge CPU (20 FPS max)
            time.sleep(0.05)
