__author__='GG [github.com/ggetsov/]'
__version__='1.0.4'
__license__='Apache 2'
__copyright__='Copyright 2021, Dreamflame Inc.'
import sublime
import sublime_plugin
import os.path
import sys
import win32clipboard as w32c
import copy
name																						=os.path.basename(os.path.abspath(os.path.dirname(__file__)))
name																						=name.replace('.sublime-package','')
settings_file																		='%s.sublime-settings'%name

def plugin_loaded():
	load_settings()


# for ST2 - manual call to plugin_loaded()
if(sys.version_info<(3,)):
	plugin_loaded()




def load_settings():
	global settings,settings_file
	settings=sublime.load_settings(settings_file)
def save_settings():
	global settings,settings_file
	sublime.save_settings(settings_file)
	# print("save settings: ",settings)
def get_setting(k,d=None):
	global settings
	try:
		settings
	except NameError:
		load_settings()
	return settings.get(k,d)
def set_setting(k,d=None):
	global settings
	# print("set setting: ",settings)
	try:
		settings
	except NameError:
		load_settings()
	settings.set(k,d)


class PastePlusCommand(sublime_plugin.TextCommand):
	def run(self,edit):
		data=sublime.get_clipboard() or None
		if(data is None):
			t=w32c.CF_HDROP
			w32c.OpenClipboard()
			if(w32c.IsClipboardFormatAvailable(t)):
				fns=w32c.GetClipboardData(t)
				w32c.CloseClipboard()
				data=", ".join(('"'+str(f)+'"') for f in fns)
			if(data is not None):
				soa=self.view.sel()
				sna=[]
				nbp=len(data)
				for s in soa:
					self.view.replace(edit,s,data)
					sna.append(copy.deepcopy(s))
				self.view.sel().clear()
				for s in sna:
					maxp=min(s.a,s.b)
					self.view.sel().add(sublime.Region(maxp+nbp,maxp+nbp))
				soa=None
				sna=None
		else:
			win=sublime.active_window()
			win.run_command("paste")


class PastePlusQueryContextListener(sublime_plugin.EventListener):
	def on_query_context(self,view,key,operator,operand,match_all):
		if((key=='pasteplus.replace_default_paste_shortcut') and (operator==0) and (operand==True)):
			if(not view.window()):
				return
			return get_setting('replace_default_paste_shortcut',False)

