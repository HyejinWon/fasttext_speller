# fasttext_speller

## Korean speller using FastText
이 코드는 한국어 오타 탐지 및 교정이 가능한 코드입니다.
FastText vector를 사용합니다.

본 코드는 KS완성형 범위를 벗어나는 단어에 한해서만 오타 교정이 가능합니다.

만약 학습된 벡터에서 결과값을 찾기 어렵다면 'not change'라는 결과를 내보냅니다.

------------
## 코드 돌리는 방법

```python
python3 spellCheckerMain.py --w2v_path='./pre-trained 된 벡터파일 주소'
--file_path='./오타 교정하고싶은 파일' 
--write_path='./결과나올 파일 path' 
--jamo_path='./자소분해된 파일이 없으면 자동으로 생성됩니다.'
--mode='jamo or word' #자소분해해서 할것인지 아니면 어절단위로 할것인지 선택합니다.
```

이렇게 입력을 주시고 돌리면 됩니다!  

