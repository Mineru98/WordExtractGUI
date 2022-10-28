# WordExtractGUI

## build

```cmd
pyinstaller -D -F --add-data "{PYTHON_LIB_DIR}\Lib\site-packages\konlpy\;.\konlpy" --add-data "{PYTHON_LIB_DIR}\Lib\site-packages\konlpy\java\;.\konlpy\java" --add-data "{PYTHON_LIB_DIR}\Lib\site-packages\konlpy\data\tagset\*;.\konlpy\data\tagset" --add-data "{PYTHON_LIB_DIR}\Lib\site-packages\wordcloud\;.\wordcloud\" --add-data "{PYTHON_LIB_DIR}\Lib\site-packages\PIL\;.\PIL\" app.py
pyinstaller -w -D -F --add-data "{PYTHON_LIB_DIR}\Lib\site-packages\konlpy\;.\konlpy" --add-data "{PYTHON_LIB_DIR}\Lib\site-packages\konlpy\java\;.\konlpy\java" --add-data "{PYTHON_LIB_DIR}\Lib\site-packages\konlpy\data\tagset\*;.\konlpy\data\tagset" --add-data "{PYTHON_LIB_DIR}\Lib\site-packages\wordcloud\;.\wordcloud\" --add-data "{PYTHON_LIB_DIR}\Lib\site-packages\PIL\;.\PIL\" app.py
```

## LoadMap

-   [ ] 여러개의 링크를 지원한다.
-   [ ] 여러개의 링크를 엑셀 형태로 업로드 할 수 있도록 한다.
-   [ ] 파일 저장시 이름 변경
-   [ ] 이미지 파일 크기 변경
-   [ ] 추출 시 지정한 최소 빈도수만큼에 해당되는 단어만 추출하도록 한다.
