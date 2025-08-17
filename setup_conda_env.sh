#!/bin/bash
# Anaconda 환경 설정 스크립트

echo "🐍 Personal Logging Platform - Anaconda 환경 설정"
echo "=================================================="

# 1. Conda 설치 확인
echo "📋 1단계: Conda 설치 상태 확인"
if command -v conda &> /dev/null; then
    echo "✅ Conda 설치됨: $(conda --version)"
    echo "📍 Conda 경로: $(which conda)"
else
    echo "❌ Conda가 설치되지 않았습니다."
    echo "💡 Anaconda/Miniconda 설치가 필요합니다."
    echo "   다운로드: https://www.anaconda.com/products/distribution"
    exit 1
fi

# 2. 현재 환경 확인
echo ""
echo "📋 2단계: 현재 환경 상태"
conda info --envs

# 3. 프로젝트용 가상환경 생성
echo ""
echo "📋 3단계: 가상환경 생성"
ENV_NAME="personal-logging"
PYTHON_VERSION="3.9"

if conda env list | grep -q "$ENV_NAME"; then
    echo "⚠️  환경 '$ENV_NAME'이 이미 존재합니다."
    read -p "기존 환경을 삭제하고 새로 만들까요? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  기존 환경 삭제 중..."
        conda env remove -n "$ENV_NAME" -y
        echo "✅ 환경 삭제 완료"
    else
        echo "📦 기존 환경을 사용합니다."
        conda activate "$ENV_NAME"
        exit 0
    fi
fi

echo "🔨 새 환경 '$ENV_NAME' 생성 중... (Python $PYTHON_VERSION)"
conda create -n "$ENV_NAME" python="$PYTHON_VERSION" -y

# 4. 환경 활성화
echo ""
echo "📋 4단계: 환경 활성화"
conda activate "$ENV_NAME"

# 5. 필요한 패키지 설치 (미래를 위한 준비)
echo ""
echo "📋 5단계: 기본 패키지 설치"
echo "🔧 pip 업그레이드..."
pip install --upgrade pip

echo "📦 유용한 패키지들 설치..."
pip install jupyter ipython

# 6. 환경 정보 출력
echo ""
echo "📋 6단계: 환경 설정 완료"
echo "✅ 가상환경 '$ENV_NAME' 생성 완료!"
echo ""
echo "🎯 사용 방법:"
echo "  활성화: conda activate $ENV_NAME"
echo "  비활성화: conda deactivate"
echo "  환경 삭제: conda env remove -n $ENV_NAME"
echo ""
echo "📁 프로젝트 디렉토리로 이동:"
echo "  cd /Users/admin/Documents/GitHub/personal-logging-platform/browser-collector/src"
echo ""
echo "🚀 실행 명령어:"
echo "  python main.py"
echo ""

# 7. 환경 활성화 상태 확인
echo "📊 현재 Python 환경 정보:"
which python
python --version
pip list | head -10

echo ""
echo "🎉 환경 설정이 완료되었습니다!"
