SOURCES = {
    'comics': [
        {
            'name': 'Comicastle',
            'endpoint': '/comics/comicastle',
            'search_endpoint': '/comics/comicastle/s/<query>',
            'type': 'stream',
            'logo': 'https://comicastle.org/upload/logo/cc__logo.png',
            'link': 'https://comicastle.org/home'
        },
        {
            'name': 'ComicExtra',
            'endpoint': '/comics/comicextra',
            'search_endpoint': '/comics/comicextra/s/<query>',
            'type': 'stream',
            'logo': 'https://www.comicextra.com/images/site/front/logo.png',
            'link': 'https://www.comicextra.com'
        }
    ],
    'manga': [
        {
            'name': 'GogoManga',
            'endpoint': '/manga/gogomanga',
            'search_endpoint': '/manga/gogomanga/s/<query>',
            'type': 'stream',
            'logo': 'https://gogomanga.fun/wp-content/uploads/2021/06/LogoMakr.png',
            'link': 'https://gogomanga.fun'
        },
        {
            'name': 'MangaPill',
            'endpoint': '/manga/mangapill',
            'search_endpoint': '/manga/mangapill/s/<query>',
            'type': 'stream',
            'logo': 'https://i.ibb.co/hW5vhqT/mpill.png',
            'link': 'https://mangapill.com'
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