from app.routes import get_books, get_personal_library

cookies = {'session': 'sji4m4hll4r6c5a0j7fv18ewo8bwhvut'}
test_lib = [{"id": 123456,
            "resource_uri": "/api/v1/bookuserlist/",
            "book": {
                "name": "Test_book_name",
                "lang": "ru",
                "default_cover": "test_cover.jpg",
                "main_author": {
                    "id": 610,
                    "resource_uri": "/api/v1/authors/1/",
                    "absolute_url": "/author/test_author/",
                    "cover_name": "The Test Author!",
                },
            }
            }]
lib_result = [
        {
            'author': 'The Test Author!',
            'book_cover': 'test_cover.jpg',
            'book_name': 'Test_book_name',
        }
    ]


def test_mybook_get_books():
    assert isinstance(get_books(cookies).json(), dict)
    assert get_books(cookies).json().get('meta')


def test_mybook_get_library():
    assert get_personal_library(test_lib) == lib_result
