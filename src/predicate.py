from libqtile.window import _Window

def is_skype_main(window):
    """ @type window: _Window """
    return 'dmitry.golovchen - Skype' in window.info()['name']

def is_skype_dialog(window):
    """ @type window: _Window """
    return '- Skype' in window.info()['name']
