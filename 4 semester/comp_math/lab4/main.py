from __future__ import annotations


def main() -> None:
    try:
        from program_part.gui_app import main as gui_main
    except ModuleNotFoundError as error:
        missing_module = getattr(error, "name", "")
        if missing_module == "tkinter":
            print("В интерпретаторе Python отсутствует tkinter.")
            return
        if missing_module.startswith("matplotlib"):
            print("Для графического интерфейса требуется библиотека matplotlib.")
            return
        raise

    gui_main()


if __name__ == "__main__":
    main()
