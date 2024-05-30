# Power Management Utility (for GNOME)
GNOME 데스크탑 환경에서 사용할 수 있는 간단한 전력 관리 유틸리티입니다.

## How to run 📄
1. Code > Download ZIP 버튼을 클릭하여 소스 코드 .zip 파일을 내려받은 후, 적절한 위치에 압축을 풉니다.

2. 폴더 안에서 `main.py`를 실행합니다.

## Included Features 📌

지정한 특정 프로그램이 실행 중인 동안 자동으로 전력 모드와 밝기를 조절합니다.  
예를 들어, GIMP`(gimp)`, Visual Studio Code`(code)` 등의 높은 성능이 요구되는 프로그램을 구동하는 중에는 자동으로 전원 모드를 바꿔주고, 평상시에는 저전력 모드로 사용할 수 있습니다.

시간대에 따라 밝기 수준을 조절할 수 있습니다. 어두운 ~~기숙사~~ 환경에서 밝기가 자동으로 최저로 낮춰지도록 할 수 있습니다. (추가 예정)

## Dependencies 🔗

Linux GNOME 데스크톱 환경에서만 동작 가능하며(Windows 지원 계획 중), 다음 python 외장 모듈 및 apt 패키지가 요구됩니다.

- pip: `flet` (≥0.22.0)
- apt: `notify-send`

## Others
이 프로젝트는 통합사회 탄소 중립 실천 수행평가 결과물의 일부로서 개발되었습니다.  
[gss.hs.kr](https://school.gyo6.net/gsshs)