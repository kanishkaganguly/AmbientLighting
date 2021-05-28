#!/home/kganguly/Documents/Projects/AmbientLights/venv/bin/python3
from lighting import Bulby
import npyscreen
import curses
import time

bulb_manager = Bulby()


class BulbStateCheckbox(npyscreen.CheckBox):
    def __init__(self, parent, *args, **keywords):
        super(BulbStateCheckbox, self).__init__(parent, *args, **keywords)
        self.value = bulb_manager.get_bulb_state()

    def whenToggled(self):
        if self.value:
            bulb_manager.start_bulb()
        else:
            bulb_manager.stop_bulb()


class BulbBrightnessSlider(npyscreen.TitleSliderPercent):
    def __init__(self, parent, *args, **keywords):
        super(BulbBrightnessSlider, self).__init__(parent, *args, **keywords)
        self.value = bulb_manager.get_bulb_brightness()
        self.add_handlers({'d': self.set_brightness})

    def set_brightness(self, key_press):
        bulb_manager.set_bulb_brightness(int(self.get_value()))


class ControllerForm(npyscreen.Form):
    def create(self):
        self.bulb_name = self.add(npyscreen.TitleFixedText, name="Bulb Name",
                                  value=f"{bulb_manager.get_bulb_name()}", relx=2, rely=1)
        self.bulb_state = self.add(
            BulbStateCheckbox, name="Set Bulb State", relx=2, rely=3)
        self.bulb_brightness = self.add(
            BulbBrightnessSlider, name="Set Brightness", step=5, label=True, relx=2, rely=5)

    def afterEditing(self):
        self.parentApp.setNextForm(None)


class LoadingScreen(npyscreen.Form):
    def create(self):
        loading_key = 's'
        loading_msg = 'Press {} to start loading bulb \n Press escape key to quit'.format(
            loading_key)

        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.exit_application
        self.add_handlers({loading_key: self.spawn_notify_popup})
        self.add(npyscreen.FixedText, value=loading_msg)

    def spawn_notify_popup(self, key_press):
        message_to_display = 'Now loading bulb...'
        npyscreen.notify(message_to_display, title='Loading')
        init_success = bulb_manager.init_bulb()
        time.sleep(2)
        if init_success:
            control = self.parentApp.addForm(
                "FORM_CONTROLLER", ControllerForm, name="Bulb Controller UI")
            self.parentApp.changeForms("FORM_CONTROLLER")
        else:
            message_to_display = 'Could not connect to bulb...'
            npyscreen.notify(message_to_display,
                             title='Connection Error')
            time.sleep(1)
            self.exit_application

    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False


class BulbApp(npyscreen.NPSAppManaged):
    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        loading = self.addForm(
            "MAIN", LoadingScreen, name="Loading Bulb")

    def changeForms(self, fm_name):
        self.switchForm(fm_name)
        self.resetHistory()


def main():
    tui = BulbApp()
    tui.run()


def bulb_test():
    init_success = bulb_manager.init_bulb()
    print("Initialized: {}".format(init_success))
    bulb_manager.start_bulb()
    print("Name: {}".format(bulb_manager.get_bulb_name()))
    print("Brightness: {}".format(bulb_manager.get_bulb_brightness()))
    bulb_manager.set_bulb_brightness(20)
    print("Brightness: {}".format(bulb_manager.get_bulb_brightness()))


if __name__ == "__main__":
    # bulb_test()
    main()
