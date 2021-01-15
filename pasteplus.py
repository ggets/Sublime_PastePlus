__author__='GG [github.com/ggetsov/]'
__version__='1.0.2'
__license__='Apache 2'
__copyright__='Copyright 2021, Dreamflame Inc.'
import sublime
import sublime_plugin
import win32clipboard as w32c
import copy

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

