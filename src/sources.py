SOURCES = {
    'comics': [
        {
            'name': 'Comicastle',
            'endpoint': '/comics/comicastle',
            'search_endpoint': '/comics/comicastle/s/<query>',
            'type': 'stream'
        },
        {
            'name': 'ComicExtra',
            'endpoint': '/comics/comicextra',
            'search_endpoint': '/comics/comicextra/s/<query>',
            'type': 'stream'
        }
    ],
    'manga': [
        {
            'name': 'GogoManga',
            'endpoint': '/manga/gogomanga',
            'search_endpoint': '/manga/gogomanga/s/<query>',
            'type': 'stream'
        },
        {
            'name': 'MangaPill',
            'endpoint': '/manga/mangapill',
            'search_endpoint': '/manga/mangapill/s/<query>',
            'type': 'stream'
        }
    ],
    'downloaders': [
        {
            'name': 'Nyaa.si',
            'endpoint': '/downloads/nyaa',
            'search_endpoint': '/downloads/nyaa/<query>',
            'type': 'download'
        },
        {
            'name': 'Eztv',
            'endpoint': '/downloads/eztv',
            'search_endpoint': '/downloads/eztv/<query>',
            'type': 'download'
        },
        {
            'name': 'GetComics',
            'endpoint': '/downloads/getcomics',
            'search_endpoint': '/downloads/getcomics/<query>',
            'type': 'download'
        }
    ]
}