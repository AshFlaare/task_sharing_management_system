pipeline {
    agent any

    environment {
        CMD = 'C:\\Windows\\System32\\cmd.exe'
        PM2_CMD = 'C:\\Users\\ashflaare\\AppData\\Roaming\\npm\\pm2.cmd'
        PYTHON_EXE = 'C:\\Program Files\\Python313\\python.exe'
        TARGET_DIR = 'C:\\Users\\ashflaare\\Desktop\\study\\4_c\\devops\\project_serv'
    }

    triggers { 
        githubPush() 
    }

    stages {
        stage('Start Backend Server') {
            steps {
                bat """
                    cd "${TARGET_DIR}"

                    :: Удаляем старый процесс Django
                    call "${PM2_CMD}" delete django || echo No existing Django process

                    :: Запускаем Django на 127.0.0.1:8000
                    call "${PM2_CMD}" start "${PYTHON_EXE}" --name django -- manage.py runserver 127.0.0.1:8000
                """
            }
        }

        stage('Start Frontend Server') {
            steps {
                bat """
                    cd "${TARGET_DIR}\\client"

                    :: Удаляем старый процесс Vue
                    call "${PM2_CMD}" delete vue || echo No existing Vue process

                    :: Запускаем Vue через PM2 в фоне
                    call "${PM2_CMD}" start "${CMD}" --name vue -- /c "cd ${TARGET_DIR}\\client && npm run dev"

                    echo Frontend started in background via PM2
                """
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    try {
                        bat """
                            cd "${TARGET_DIR}"
                            "${PYTHON_EXE}" application\\integrationtests.py
                        """
                        echo "Tests passed! Keeping servers running."
                    } catch (err) {
                        echo "Tests failed! Stopping servers..."
                        // Убираем процессы PM2, если тесты не прошли
                        bat """
                            "${PM2_CMD}" delete django || echo No Django process to delete
                            "${PM2_CMD}" delete vue || echo No Vue process to delete
                        """
                        error("Integration tests failed. Servers stopped.")
                    }
                }
            }
        }
        stage('Merge fix into main') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                withCredentials([
                    usernamePassword(credentialsId: 'github-creds', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN'),
                    string(credentialsId: 'github-email', variable: 'GIT_EMAIL')
                ]) {
                    bat """
                        cd "${TARGET_DIR}"
                        git config user.name "%GIT_USER%"
                        git config user.email "%GIT_EMAIL%"
                        
                        git checkout main

                        git pull --rebase https://%GIT_USER%:%GIT_TOKEN%@github.com/AshFlaare/task_sharing_management_system.git main

                        git merge fix
                        git push https://%GIT_USER%:%GIT_TOKEN%@github.com/AshFlaare/task_sharing_management_system.git main
                    """
                }
            }
        }

    }

    post {
        success {
            echo "Backend and Frontend are running via PM2!"
            echo "Backend: http://127.0.0.1:8000/"
            echo "Frontend: http://127.0.0.1:5173/"
        }
    }
}
