try:
	import tools.gdlevelclient as lc
except ModuleNotFoundError:
	print('[WARNING] Running without tools.gd levelclient')
import tools.gdleveltools as lt
import tools.gui as gui
import tools.clientinput as ci
import pages
import tkinter as tk
import time


DEBUG = False


data = ''


if __name__ == '__main__':
	if not DEBUG:
		print('='*40)
		print('KILLBOT.EXE')
		print('by GunnerBones')
		print('='*40)
		print('Preparing topmost created level...')
		gs = lc.GameSave()
		data = gs.save()
		print('Level loaded! Name: ' + gs.top_level().name)
		print()
		print('WARNING!!!!! This tool will CORRUPT the level and make it super scary.')
		print('Only proceed if you wish to ruin this level, as the damage can\'t be undone.')
		print('Also note: this tool will only work if Geometry Dash is CLOSED. Open it once corrupted')
		print()
		res = input('CORRUPT THE LEVEL? (yes/no) ')
		if res.lower() == 'yes':
			print('Corrupting ' + gs.top_level().name + '... (this will take a minute or two be patient)')	
			time.sleep(0.5)
			data = lt.killbotObjects(data)
			data = lt.killbotColorChannels(data)
			gs.load(data)
			print()
			print('KILLBOT')
			view = gui.TkView()
			view.iconbitmap(lt.corePYIPath('killbot.ico'))
			view.mainloop()
		else:
			print('ok bye')

	else:
		view = gui.TkView()
		view.iconbitmap(lt.corePYIPath('killbot.ico'))
		view.mainloop()
		"""gs = lc.GameSave()
								data = gs.save()
								print(gs.top_level().name)
								print('old_level_size=' + str(lt.toolLevelSize(data)))
								data = lt.killbotObjects(data)
								data = lt.killbotColorChannels(data)
								print('new_level_size=' + str(lt.toolLevelSize(data)))
								gs.load(data)
								#lt.toolSavePattern(data, 'TEXT_CRY')
								print('Loaded')"""