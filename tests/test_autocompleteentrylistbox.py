# Copyright (c) Juliette Monsel 2019
# For license see LICENSE
from ttkwidgets.autocomplete import AutocompleteEntryListbox
from tests import BaseWidgetTest
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class TestEvent(object):
    def __init__(self, key):
        self.keysym = key


class TestAutocompleteWidgets(BaseWidgetTest):
    def test_autocompleteentrylistbox_init(self):
        widget = AutocompleteEntryListbox(self.window,
                                          completevalues=["Hello", "World", "Test"])
        widget.pack()
        self.window.update()
        widget.destroy()

        widget = AutocompleteEntryListbox(self.window, allow_other_values=True,
                                          exportselection=True, justify='center',
                                          autohidescrollbar=False)
        widget.pack()
        self.window.update()
        widget.destroy()

        widget = AutocompleteEntryListbox(self.window)
        widget.pack()
        self.window.update()
        widget.destroy()

    def test_autocompleteentrylistbox_config(self):
        widget = AutocompleteEntryListbox(self.window, width=20,
                                          font='Arial 20', padding=2,
                                          completevalues=["Hello", "World", "Test"])
        widget.pack()
        self.window.update()
        self.assertFalse(widget['allow_other_values'])
        self.assertFalse(widget['exportselection'])
        self.assertFalse(widget.entry['exportselection'])
        self.assertFalse(widget.listbox['exportselection'])
        self.assertTrue(widget['autohidescrollbar'])
        self.assertEqual(str(widget['padding'][0]), '2')
        self.assertEqual(str(widget['justify']), 'left')
        self.assertEqual(int(widget['width']), 20)
        self.assertEqual(int(widget.entry['width']), 20)
        self.assertEqual(int(widget.listbox['width']), 20)
        self.assertEqual(str(widget['font']), 'Arial 20')
        self.assertEqual(str(widget.entry['font']), 'Arial 20')
        self.assertEqual(str(widget.listbox['font']), 'Arial 20')
        self.assertEqual(widget['completevalues'], ["Hello", "World", "Test"])
        self.assertEqual(list(widget.listbox.get(0, 'end')), ["Hello", "World", "Test"])
        self.assertFalse(widget._scrollbar.winfo_ismapped())

        widget['allow_other_values'] = True
        widget['justify'] = 'center'
        widget['width'] = 23
        widget['padding'] = 5
        widget['font'] = 'Arial 10 bold'
        widget['completevalues'] = ['test']
        widget.configure({'exportselection': True}, autohidescrollbar=False)
        self.window.update()

        self.assertTrue(widget['allow_other_values'])
        self.assertTrue(widget['exportselection'])
        self.assertTrue(widget.entry['exportselection'])
        self.assertTrue(widget.listbox['exportselection'])
        self.assertFalse(widget['autohidescrollbar'])
        self.assertEqual(widget['justify'], 'center')
        self.assertEqual(str(widget['padding'][0]), '5')
        self.assertEqual(int(widget['width']), 23)
        self.assertEqual(int(widget.entry['width']), 23)
        self.assertEqual(int(widget.listbox['width']), 23)
        self.assertEqual(str(widget['font']), 'Arial 10 bold')
        self.assertEqual(str(widget.entry['font']), 'Arial 10 bold')
        self.assertEqual(str(widget.listbox['font']), 'Arial 10 bold')
        self.assertEqual(widget['completevalues'], ['test'])
        self.assertEqual(list(widget.listbox.get(0, 'end')), ['test'])
        self.assertTrue(widget._scrollbar.winfo_ismapped())

        widget['autohidescrollbar'] = True
        self.window.update()
        self.assertFalse(widget._scrollbar.winfo_ismapped())

    def test_autocompleteentrylistbox_methods(self):
        widget = AutocompleteEntryListbox(self.window,
                                          completevalues=["Hello", "World", "Test"])
        widget.pack()
        self.window.update()

        keys = widget.keys()
        for key in ['completevalues', 'allow_other_values', 'exportselection', 'justify', 'font']:
            self.assertIn(key, keys)

        # typing in entry
        widget.entry.focus_force()
        widget.entry.event_generate('<W>')
        self.assertEqual(widget.get(), 'World')
        widget.entry.focus_force()
        widget.entry.event_generate('<Control-a>')
        widget.entry.focus_force()
        widget.entry.event_generate('<Y>')
        self.assertEqual(widget.get(), '')
        widget.entry.focus_force()
        widget.entry.event_generate('<H>')
        self.assertEqual(widget.get(), 'Hello')
        widget.entry.focus_force()
        widget.entry.event_generate('<u>')
        self.assertEqual(widget.get(), 'H')

        widget['allow_other_values'] = True
        widget.entry.event_generate('<u>')
        self.assertEqual(widget.get(), 'Hu')
        widget.entry.event_generate('<BackSpace>')
        self.assertEqual(widget.get(), 'H')

        # selecting in listbox
        widget.entry.focus_force()
        widget.entry.event_generate('<Down>')
        self.window.update()
        self.assertEqual(widget.get(), 'World')
        widget.listbox.event_generate('<Down>')
        self.window.update()
        self.assertEqual(widget.get(), 'Test')
        widget.listbox.event_generate('<Down>')
        self.window.update()
        self.assertEqual(widget.get(), 'Hello')
        widget.listbox.event_generate('<Up>')
        self.window.update()
        self.assertEqual(widget.get(), 'Test')
        widget.listbox.focus_force()
        widget.listbox.event_generate('<h>')
        self.window.update()
        self.assertEqual(widget.get(), 'Hello')
        widget.entry.focus_force()
        widget.entry.event_generate('<Up>')
        self.window.update()
        self.assertEqual(widget.get(), 'Test')

        # tab and selected text in entry
        widget.entry.delete(0, 'end')
        widget.entry.focus_force()
        widget.entry.event_generate('<W>')
        self.window.update()
        self.assertTrue(widget.entry.selection_present())
        self.window.update()
        widget.entry.focus_force()
        widget.entry.event_generate('<Tab>')
        self.window.update()
        self.assertFalse(widget.entry.selection_present())
        widget.entry.event_generate('<W>')
        self.assertEqual(widget.get(), 'WorldW')

        # right arrow navigation
        widget.entry.delete(0, 'end')
        widget.entry.focus_force()
        widget.entry.event_generate('<W>')
        self.window.update()
        self.assertTrue(widget.entry.selection_present())
        self.window.update()
        widget.entry.focus_force()
        widget.entry.event_generate('<Right>')
        self.window.update()
        self.assertFalse(widget.entry.selection_present())
        self.assertEqual(widget.entry.index('insert'), widget.entry.index('end'))
        widget.entry.focus_force()
        widget.entry.event_generate('<Left>')
        widget.entry.event_generate('<Left>')
        widget.entry.event_generate('<Left>')
        self.window.update()
        self.assertEqual(widget.entry.index('insert'), widget.entry.index('end') - 3)
        widget.entry.focus_force()
        widget.entry.event_generate('<Right>')
        self.window.update()
        self.assertEqual(widget.entry.index('insert'), widget.entry.index('end') - 2)
