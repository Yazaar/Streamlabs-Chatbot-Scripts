import os, zipfile, sys, time

os.chdir("..")
url = sys.argv[1]

try:
    import urllib

    urllib.urlretrieve(url, "PyInstaller.zip")
    with zipfile.ZipFile("PyInstaller.zip", 'r') as f:
        f.extractall()
    os.remove("PyInstaller.zip")
except Exception:
    try:
        import urllib.request

        urllib.request.urlretrieve(url, "PyInstaller.zip")
        with zipfile.ZipFile("PyInstaller.zip", 'r') as f:
            f.extractall()
        os.remove("PyInstaller.zip")
    except Exception:
        print('Failed to use PyInstaller.py (Failed to execute "urllib.urlretrieve()" and "urllib.request.urlretrieve()")')