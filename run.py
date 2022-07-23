from Torrent.Torrent import Torrent

try:

    with Torrent() as bot:
        bot.muvi()
        print('next run')
        bot.tv()
        # bot.top100_tv()

except Exception as e:
    if 'in PATH' in str(e):
        print(
            'You are trying to run the bot from terminal \n'
            'Please add to PATH your Selenium Drivers \n'
            'Windows: \n'
            '     set PATH=%PATH%;C:path-to-your-folder \n \n'
            'Linux: \n'
            '     PATH=$PATH:/path/toyour/folder/ \n'
        )

    else:
        # for other exceptions
        raise
