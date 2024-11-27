# Weather Widget

심플한 날씨 위젯 애플리케이션입니다. 항상 화면 위에 떠있는 형태로 현재 날씨 정보를 보여줍니다.

## 기능
- 실시간 날씨 정보 표시
- 항상 위에 표시
- 드래그로 위치 이동
- 종료 버튼
- 5분마다 자동 업데이트
- 마지막 위치 기억

## 설치 방법

### 개발 환경 설정
1. Python 3.12 이상 설치 필요
2. 프로젝트 클론 후 install.bat 실행
```bash
git clone <repository-url>
cd weather-widget
install.bat
```

### OpenWeatherMap API 키 설정
1. [OpenWeatherMap](https://openweathermap.org/) 가입
2. API 키 발급
3. `.env` 파일에 API 키 입력:
```
WEATHER_API_KEY=your_api_key_here
```

## 실행 방법

### 개발 모드
```bash
run.bat
```

### 실행 파일 생성
```bash
build.bat
```
생성된 실행 파일은 `dist` 폴더에서 찾을 수 있습니다.

## 프로젝트 구조
```
weather_widget/
├── main.py           # 메인 프로그램
├── .env             # 환경 변수 설정
├── install.bat      # 설치 스크립트
├── run.bat          # 실행 스크립트
├── build.bat        # 빌드 스크립트
└── requirements.txt  # 의존성 목록
```

## 사용된 기술
- Python 3.12
- PySide6
- OpenWeatherMap API
- python-dotenv
- PyInstaller

## 주의사항
- API 키를 안전하게 보관하세요
- 첫 실행시 Windows 보안 경고가 표시될 수 있습니다
- 인터넷 연결이 필요합니다

## 문제 해결
1. "API 키가 설정되지 않았습니다" 에러
   - `.env` 파일이 올바르게 설정되어 있는지 확인
   - API 키가 유효한지 확인

2. "날씨 정보 로딩 실패" 메시지
   - 인터넷 연결 확인
   - API 키 유효성 확인

## 라이선스
MIT License

## 기여 방법
1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request

## 작성자
makepluscode

## 업데이트 내역
- 2024.11.27: 최초 버전 배포