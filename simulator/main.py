import graphics.gui as gui
import threading



def main():
    app = gui.MainApplication()
    hilo_actual = threading.current_thread()
    print(f"Hilo principal: {hilo_actual.name} (ID: {hilo_actual.ident})")
    app.mainloop()


if __name__ == '__main__':
    main()
