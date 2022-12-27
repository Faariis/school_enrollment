1. Create `settings_shared.py` storing non-sensitive information
2. Create `settings.py` on server
```bash
$ cat settings.py
from my_pollution.settings_shared import *

DEBUG = True

TEST_MAIL = 'anel_1002@hotmail.com'
```
