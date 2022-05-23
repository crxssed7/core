SOURCES = {
    'comics': [
        {
            'name': 'GetComics',
            'endpoint': '/comics/getcomics',
            'search_endpoint': '/comics/getcomics/<query>',
            'type': 'download'
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
    'torrents': [
        {
            'name': 'Nyaa.si',
            'endpoint': '/torrents/nyaa',
            'search_endpoint': '/torrents/nyaa/<query>',
            'type': 'download'
        },
        {
            'name': 'Eztv',
            'endpoint': '/torrents/eztv',
            'search_endpoint': '/torrents/eztv/<query>',
            'type': 'download'
        }
    ]
}