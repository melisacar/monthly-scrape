import locale

def test_default_encoding():
    encoding = locale.getpreferredencoding()

    assert encoding is not None, "Sistem varsayılan kodlaması belirlenemedi"

    print("Sistem varsayılan kodlaması:", encoding)