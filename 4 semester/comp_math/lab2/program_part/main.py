from __future__ import annotations

def main() -> None:
    try:
        from program_part.gui_app import main as gui_main
    except ModuleNotFoundError as error:
        missing_module = getattr(error, "name", "")
        if missing_module == "tkinter":
            print("в интерпретаторе нет tkinter")
            
            return
        raise

    gui_main()


if __name__ == "__main__":
    main()
