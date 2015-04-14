import hexchat
import time
import praw

__module_name__ = 'mxtm'
__module_author__ = 'NewellWorldOrder'
__module_version__ = '1.0'
__module_description__ = 'Links random mxtm photoshop'

r = praw.Reddit(user_agent='HexchatMXTMPhotoshopsGrabber')
limit = 0

def mxtmPrefs(word, word_eol, userdata):
    if word[1] == 'enable':
        hexchat.set_pluginpref('mxtm', 'yes')
        print('mxtm enabled')
    elif word[1] == 'disable':
        hexchat.del_pluginpref('mxtm')
        print('mxtm disabled >:')
    return hexchat.EAT_ALL

def mxtm(word, word_eol, userdata):
    status = hexchat.get_pluginpref('mxtm')
    global limit
    if limit == 0 and word[1] == '!mxtm' and status == 'yes':
        context = hexchat.get_info('channel')
        if context == '##mxtmfanclub' or context == '#Chat' or context == '#dogecoin-bots':
            link = r.get_random_submission(subreddit='mxtmphotoshopbattles')
            hexchat.command('say %s – %s' % (str(link).split(' :: ')[1], link.url))
            lastTime = time.time()
            limit = 1
            while limit == 1:
                if time.time() - lastTime >= 2:
                    limit = 0
                    break
    return hexchat.EAT_PLUGIN

hexchat.hook_command('mxtm', mxtmPrefs, help='/mxtm enable turns mxtm on. /mxtm disable turns mxtm off.')
hexchat.hook_print('Channel Message', mxtm)

def mxtm_unloaded(userdata):
    hexchat.emit_print('Notice', '', '%s v%s by %s unloaded' % (__module_name__, __module_version__, __module_author__))
    return hexchat.EAT_ALL
hexchat.emit_print('Notice', '', '%s v%s by %s loaded' % (__module_name__, __module_version__, __module_author__))
hexchat.hook_unload(mxtm_unloaded)
