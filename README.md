# WordExtractGUI

## build

```cmd
pyinstaller -D -F --add-data "{PYTHON_LIB_DIR}\Lib\site-packages\konlpy\;.\konlpy" --add-data "{PYTHON_LIB_DIR}\Lib\site-packages\konlpy\java\;.\konlpy\java" --add-data "{PYTHON_LIB_DIR}\Lib\site-packages\konlpy\data\tagset\*;.\konlpy\data\tagset" --add-data "{PYTHON_LIB_DIR}\Lib\site-packages\wordcloud\;.\wordcloud\" --add-data "{PYTHON_LIB_DIR}\Lib\site-packages\PIL\;.\PIL\" app.py
pyinstaller -w -D -F --add-data "{PYTHON_LIB_DIR}\Lib\site-packages\konlpy\;.\konlpy" --add-data "{PYTHON_LIB_DIR}\Lib\site-packages\konlpy\java\;.\konlpy\java" --add-data "{PYTHON_LIB_DIR}\Lib\site-packages\konlpy\data\tagset\*;.\konlpy\data\tagset" --add-data "{PYTHON_LIB_DIR}\Lib\site-packages\wordcloud\;.\wordcloud\" --add-data "{PYTHON_LIB_DIR}\Lib\site-packages\PIL\;.\PIL\" app.py
```
