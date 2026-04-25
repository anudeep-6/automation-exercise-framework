pipeline {
    agent any

    environment {
        VENV_DIR      = "venv"
        REPORTS_DIR   = "allure-results"
        ARTIFACTS_DIR = "artifacts"
        BROWSER       = "chromium"
    }

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                echo "Checked out branch: ${env.GIT_BRANCH}"
            }
        }

        stage('Install Dependencies') {
            steps {
                sh """
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e ".[dev]"
                    python -m playwright install ${BROWSER} --with-deps
                """
            }
        }

        stage('Run API Tests') {
            steps {
                sh """
                    . ${VENV_DIR}/bin/activate
                    python -m pytest tests/api/ \
                        -v \
                        --alluredir=${REPORTS_DIR} \
                        --tb=short \
                        -q
                """
            }
            post {
                always {
                    echo "API test stage complete — status: ${currentBuild.currentResult}"
                }
            }
        }

        stage('Run UI Tests') {
            steps {
                sh """
                    . ${VENV_DIR}/bin/activate
                    python -m pytest tests/ui/ \
                        -v \
                        --alluredir=${REPORTS_DIR} \
                        --tb=short \
                        --browser=${BROWSER} \
                        --headed=false \
                        -q
                """
            }
            post {
                always {
                    echo "UI test stage complete — status: ${currentBuild.currentResult}"
                }
            }
        }

        stage('Publish Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk              : '',
                    results          : [[path: "${REPORTS_DIR}"]],
                    reportBuildPolicy: 'ALWAYS',
                    report           : 'reports/allure-report'
                ])
            }
        }
    }

    post {
        always {
            echo "Pipeline finished — final status: ${currentBuild.result}"
            archiveArtifacts(
                artifacts: "${ARTIFACTS_DIR}/**/*",
                allowEmptyArchive: true
            )
        }
        failure {
            echo "Build failed. Check Allure report and archived artifacts for screenshots/traces."
        }
        success {
            echo "All tests passed."
        }
    }
}