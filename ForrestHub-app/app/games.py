from pathlib import Path
import shutil
from flask import current_app


def copy_default_game():
    # current_app.config.get("GAMES_FOLDER_LIVE")
    # copy default game from GAMES_FOLDER to GAMES_FOLDER_LIVE
    games_folder = Path(current_app.config.get("GAMES_FOLDER"))
    games_folder_live = Path(current_app.config.get("GAMES_FOLDER_LIVE"))
    if not games_folder.exists():
        return {"status": "error", "message": "Složka s hrami neexistuje"}
    if not games_folder_live.exists():
        games_folder_live.mkdir(parents=True, exist_ok=True)

    # copy game in folder ".ukazkova-hra" to folder live folder
    default_game_folder = games_folder / ".ukazkova-hra"
    if not default_game_folder.exists():
        return {"status": "error", "message": "Vzorová hra neexistuje"}
    destination_folder = games_folder_live / "ukazkova-hra"
    shutil.copytree(
        default_game_folder,
        destination_folder,
        dirs_exist_ok=True
    )
    return {"status": "success", "message": "Ukázková hra byla úspěšně zkopírována do složky ukazkova-hra"}
